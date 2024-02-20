# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Package: custom_rap_installer."""
from logging import getLogger

from .__about__ import __author__, __copyright__, __license__, __version__
from .pictorymanager import PiCtoryCommand, PiCtoryManager

log = getLogger(__name__)


def main(
    command: PiCtoryCommand,
    install_source: str,
    install_root: str = "/var/www/revpi/pictory",
    remove=False,
    use_kunbus_files=False,
) -> int:
    """
    Main entry point to install or remove a PiCtory Device.

    This module installs PiCtory Devices. If PiCtoryCommand.INFO is specified,
    the current installation status is displayed. By default, new modules and
    actions are installed in the catalog-custom.json and
    actionRules-custom.json. With PiCtoryCommand.UNINSTALL only the entries are
    removed from the catalog-custom.json, this ensures that an existing PiCtory
    configuration with the modules remains valid. All files can also be deleted
    via the "remove=True" flag.

    Old PiCtory versions before 2.3.0 only process the KUNBUS catalog files.
    New modules can be installed there via use_kunbus_files, but would be
    hidden again by an update of PiCtory.

    :param command: PiCtoryCommand instance
    :param install_source: path which rap, image und meta.json file to install
    :param install_root: Alternative path to PiCtory installation
    :param remove: If True, all files will be removed
    :param use_kunbus_files: Add modules to KUNBUS catalog
    """
    log.debug(f"PiCtory sub command '{command}'")

    pictory_manager = PiCtoryManager(install_source, install_root, use_kunbus_files)

    if not pictory_manager.check_environment():
        log.error("Can not access all needed files and directories of PiCtory")
        return 1

    if command is PiCtoryCommand.INFO:
        pictory_manager.cli_check_rap()

    elif command is PiCtoryCommand.INSTALL:
        pictory_manager.install_modules()

    elif command is PiCtoryCommand.UNINSTALL:
        pictory_manager.uninstall_modules(remove)

    else:
        log.error(f"Unknown pictory command '{command}', use PiCtoryCommand class.")
        return 1

    return 0
