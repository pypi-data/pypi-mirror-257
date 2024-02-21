import os
import json
import hmac
import hashlib
import time
import requests
import click

BASE_URL = "https://api.vagon.io"


@click.command()
def configure():
    """Configure the Vagon Streams API Key and Secret for the CLI.

    Usage: `vagon-cli configure` and fill in the prompts to save the credentials.

    The credentials are saved at ~/.vagon/credentials."""
    # Define the credentials file path
    credentials_file = os.path.expanduser("~/.vagon/credentials")

    # Check if the credentials file already exists
    if not os.path.exists(credentials_file):
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(credentials_file), exist_ok=True)

        # Prompt the user for the Vagon Streams API Key and Secret
        api_key = click.prompt(
            "Please enter your Vagon Streams API Key", type=str)
        api_secret = click.prompt(
            "Please enter your Vagon Streams API Secret", type=str
        )

        # Save the credentials in a dictionary
        credentials = {"default": {
            "api_key": api_key, "api_secret": api_secret}}

        # Write the credentials to the file in JSON format
        with open(credentials_file, "w") as file:
            json.dump(credentials, file, indent=4)

        click.echo("Credentials saved successfully.")
    else:
        click.echo(
            "Credentials file already exists. Please manually update it if necessary."
        )


@click.command()
@click.option(
    "--zip-file",
    "-z",
    "app_archive",
    help="Application Zip File [required]",
    required=True,
)
@click.option(
    "--app-id", "-i", "app_id", help="Streams Application ID [required]",
    type=int, required=True
)
@click.option(
    "--exec", "-e", "executable", help="Application Main Executable File (.exe) [required]",
    required=True
)
@click.option(
    "--app-version", "-v", "app_version", help="Name of the Application Version [required]",
    required=True
)
def deploy(app_archive, app_id, executable, app_version):
    """Deploy a New Version to an Existing Application.

    Uploaded application file will be deployed as a new version to the specified Application.
    """

    # Get Credentials
    api_key, api_secret = get_credentials()
    if not api_key or not api_secret:
        return

    if not os.path.exists(app_archive):
        click.echo(f"File {app_archive} does not exist.")
        return

    file_size = os.path.getsize(app_archive)
    file_name = os.path.basename(app_archive)

    # create Vendor Application Executable
    response = create_vendor_application_executable(
        api_key, api_secret, file_name, file_size, app_id, executable
    )
    if response.status_code != 200:
        click.echo(f"Failed with status code: {response.status_code}")
        if response.text:
            click.echo(f"Response: {response.text}")
        return

    vendor_executuable_id = response.json().get("id")
    upload_urls = response.json().get("upload_urls")
    file_upload_id = response.json().get("file_upload_id")
    chunk_size = int(response.json().get("chunk_size")) * 2**20

    if not file_upload_id:
        upload_object(upload_urls, app_archive)
        response = finalize_vendor_application_executable(
            api_key, api_secret, vendor_executuable_id, executable, app_version
        )
    else:
        parts = upload_multipart_object(upload_urls, app_archive, chunk_size)
        response = finalize_multipart_vendor_application_executable(
            api_key, api_secret, vendor_executuable_id, executable, app_version, parts
        )

    if response.status_code != 200:
        click.echo(f"Failed with status code: {response.status_code}")
        if response.text:
            click.echo(f"Response: {response.text}")


def get_credentials():
    credentials_file = os.path.expanduser("~/.vagon/credentials")
    if not os.path.exists(credentials_file):
        click.echo(
            "Credentials file does not exist. Please run 'vagon-cli configure' to create it."
        )
        return None, None

    with open(credentials_file, "r") as file:
        credentials = json.load(file)
        default_credentials = credentials.get("default")
        if not default_credentials:
            click.echo(
                "No default credentials found in the credentials file. Please run 'vagon-cli configure' to create them."
            )
            return
        api_key = default_credentials.get("api_key")
        api_secret = default_credentials.get("api_secret")
        return api_key, api_secret


def create_vendor_application_executable(
    api_key, api_secret, file_name, file_size, vendor_app_id, executable
):
    path = "/app-stream-management/cli/executables"
    url = BASE_URL + path

    data = {
        "file_name": file_name,
        "file_size": file_size,
        "vendor_application_id": vendor_app_id,
        "executable_list": [executable],
    }

    time = current_milli_time()
    signature = get_hmac(api_key, api_secret, path,
                         time, "POST", json.dumps(data))
    authorization = f"HMAC {api_key}:{signature}:mysupernonce:{time}"
    # send the request
    headers = {"Authorization": authorization,
               "Content-Type": "application/json"}

    # create the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def get_hmac(api_key, api_secret, path, time, method, body):
    payload = f"{api_key}{method}{path}{time}mysupernonce{body}"
    return hmac.new(api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def current_milli_time():
    return round(time.time() * 1000)


def upload_object(upload_urls, file_name):
    click.echo("Uploading object...")
    click.echo(f"0% complete")
    response = requests.put(upload_urls[0], data=open(file_name, "rb"))
    if response.status_code == 200:
        click.echo(f"100% complete")
        click.echo("Upload complete.")
        return True
    else:
        click.echo("Upload failed.")
        return False


def upload_multipart_object(upload_urls, file_name, chunk_size):
    click.echo("Uploading object...")
    click.echo(f"0% complete")
    with open(file_name, "rb") as f:
        part_number = 1
        parts = []
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            response = requests.put(upload_urls[part_number - 1], data=chunk)
            if response.status_code == 200:
                click.echo(f"{int((part_number / len(upload_urls)) * 100)}% complete")
            else:
                click.echo("Upload failed.")
                raise Exception("Multipart Upload failed.")
            parts.append({"part_number": part_number,
                         "etag": response.headers["ETag"]})
            part_number += 1
        click.echo("100% complete")
        click.echo("Upload complete.")
        return parts


def finalize_vendor_application_executable(
    api_key, api_secret, vendor_executable_id, executable_name, app_version
):
    path = f"/app-stream-management/cli/executables/{vendor_executable_id}/complete"
    url = BASE_URL + path

    data = {"executable_name": executable_name, "version_name": app_version}

    time = current_milli_time()
    signature = get_hmac(api_key, api_secret, path,
                         time, "POST", json.dumps(data))
    authorization = f"HMAC {api_key}:{signature}:mysupernonce:{time}"
    # send the request

    headers = {"Authorization": authorization,
               "Content-Type": "application/json"}

    # create the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def finalize_multipart_vendor_application_executable(
    api_key, api_secret, vendor_executable_id, executable_name, app_version, parts
):
    path = f"/app-stream-management/cli/executables/{vendor_executable_id}/complete"
    url = BASE_URL + path

    data = {
        "executable_name": executable_name,
        "version_name": app_version,
        "parts": parts,
    }

    time = current_milli_time()
    signature = get_hmac(api_key, api_secret, path,
                         time, "POST", json.dumps(data))
    authorization = f"HMAC {api_key}:{signature}:mysupernonce:{time}"
    # send the request

    headers = {"Authorization": authorization,
               "Content-Type": "application/json"}

    # create the request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response
