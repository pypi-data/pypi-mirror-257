# -*- coding: utf-8 -*-

"""Top-level package for Vagon CLI"""

import click

from vagoncli import commands


__author__ = """Vagon, Inc."""
__email__ = 'info@vagon.io'
__version__ = '0.0.1'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    \b
    __     ___    ____  ___  _   _   ____ _____ ____  _____    _    __  __ ____
    \ \   / / \  / ___|/ _ \| \ | | / ___|_   _|  _ \| ____|  / \  |  \/  / ___|
     \ \ / / _ \| |  _| | | |  \| | \___ \ | | | |_) |  _|   / _ \ | |\/| \___ \\
      \ V / ___ \ |_| | |_| | |\  |  ___) || | |  _ <| |___ / ___ \| |  | |___) |
       \_/_/   \_\____|\___/|_| \_| |____/ |_| |_| \_\_____/_/   \_\_|  |_|____/

    Vagon CLI for managing Vagon Streams resources.

    \b
    Simple flow:
    - `vagon-cli configure` to save the Vagon Streams API Key and Secret
    - `vagon-cli deploy [OPTIONS]` to deploy a Vagon Stream Vendor Application

    e.g. `vagon-cli deploy --zip-file app.zip --app-id 123 --exec app.exe --app-version v1.0-initial-build`

    Use --help on any command for more information."""
    pass


# Add commands
cli.add_command(commands.configure)
cli.add_command(commands.deploy)