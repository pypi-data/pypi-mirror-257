# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH <support@kunbus.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Manage PiCtory integration."""

from enum import Enum
from gettext import translation
from glob import glob
from json import dump, load
from logging import getLogger
from os import R_OK, W_OK, X_OK, access, remove as remove_file
from os.path import basename, dirname, exists, join
from re import compile
from typing import Dict, List, Tuple
from uuid import uuid4

log = getLogger(__name__)

# Load translation of this python module
_ = translation(
    "pictory_manager",
    join(dirname(__file__), "locale"),
    fallback=True,
).gettext


class PiCtoryCommand(Enum):
    INFO = ""
    INSTALL = "install"
    UNINSTALL = "uninstall"


class PiCtoryManager:
    """
    Install / Uninstall PiCtory modules of a virtual Device.

    In addition to this script, there is a folder 'modules'. The module image
    (module_id.png), the module RAP file (moduleid_timestamp_major_minor.rap)
    and a meta.json are stored in the folder.

    The 'meta.json' file contains a list of module objects, which contain the
    properties: 'id', 'title', 'tooltip' each as a string and a property
    'action_rules', which includes a list of strings, which action rules
    should be integrated for the module.

    This is the naming schema of a RAP file:

    |--- module key ---|
    xxxxxx_yyyymmdd_a_b.rap
       |	  |		| |
       |	  |		| |-- version number part 2
       |	  |		|---- version number part 1
       |	  |---------- creation timestamp
       |----------------- module id / name
    """

    re_rap_file_name = compile(
        r"(?P<module_id>.+)_(?P<timestamp>\d+)_(?P<major>\d+)_(?P<minor>\d+)(\.rap)?"
    )

    def __init__(self, install_source: str, install_root: str, use_kunbus_files=False):
        """
        Install custom RAP files to the *-custom.json files of PiCtory.

        This class is responsible for the installation / uninstallation of its
        own RAP devices. The files from "install_source" are processed and
        installed in the target system in the appropriate places.

        :param install_source: directory with rap, image und meta.json file to install
        :param install_root: path to pictory installation folder
        """
        self.action_rules_file = join(
            install_root,
            "resources",
            "data",
            "rap",
            "actionRules.json" if use_kunbus_files else "actionRules-custom.json",
        )
        self.kunbus_catalog_file = join(install_root, "resources", "data", "catalog.json")
        self.catalog_file = join(
            install_root,
            "resources",
            "data",
            "catalog.json" if use_kunbus_files else "catalog-custom.json",
        )
        self.module_image_dir = join(install_root, "resources", "images", "devices")
        self.install_source = install_source
        self.rap_dir = join(install_root, "resources", "data", "rap")
        self.use_kunbus_files = use_kunbus_files

        self.modules_meta = []
        self._load_modules_meta()

    def _add_action_rule(self, add_module_key: str, add_actions: list) -> int:
        """
        Add this module_key (id and version) to action rules.

        The transferred actions are registered for the specified module key
        (composed of ID and version number). If one of the passed actions
        already exists for the module ID, the module key is added to the
        "deviceTypes" list, the action.

        :param add_module_key: Module-ID and version information
        :param add_actions: A list with actions to activate for the module
        """
        module_regex_match = self.re_rap_file_name.fullmatch(add_module_key)
        module_id = module_regex_match.group("module_id")
        added_rules = 0

        if exists(self.action_rules_file):
            with open(self.action_rules_file) as fh:
                action_rules = load(fh)  # type: list
        else:
            action_rules = []

        for add_action in add_actions:
            rule_exists = False

            for i in range(len(action_rules) - 1, -1, -1):
                action_rule = action_rules[i]  # type: dict
                if action_rule.get("rule", "") != add_action:
                    # Skip, this is not the add_action we are looking for
                    continue

                module_keys = action_rule.get("deviceTypes", [])  # type: list

                # Check for existing module_key in this action
                if add_module_key in module_keys:
                    rule_exists = True
                    log.debug(
                        f"Acton rule '{add_action}' for module '{add_module_key}' already exist"
                    )
                    break

                # Check for module id in module keys of this action
                for module_key in module_keys:
                    module_regex_match = self.re_rap_file_name.fullmatch(module_key)
                    if module_id == module_regex_match.group("module_id"):
                        # This includes action rules for this module, so add here
                        module_keys.append(add_module_key)
                        added_rules += 1
                        rule_exists = True
                        log.debug(
                            f"Found '{add_action}' rule with other module versions, added '{add_module_key}'"
                        )
                        break

            if not rule_exists:
                # At this point, we could not find existing rules
                action_rules.append(
                    {
                        "deviceTypes": [add_module_key],
                        "rule": add_action,
                        "active": True,
                    }
                )
                log.debug(f"Created new '{add_action}' rule entry for '{add_module_key}'")
                added_rules += 1

        if added_rules:
            with open(self.action_rules_file, "w") as fh:
                dump(action_rules, fh, indent=2)
                log.debug(f"Saved action rules file to '{self.action_rules_file}'")

        return added_rules

    def _add_to_catalog(
        self, dir_title: str, dev_key: str, dev_title: str, dev_tooltip: str
    ) -> None:
        """
        Add a new PiCtory module to the catalog custom file.

        This function searches for the folder specified with "dir_title". If
        this is not found, a new folder with the name from "dir_title" and a
        generated key will be created. The new device will be added to the
        children. If the "dir_title" already exists, the module will be added
        to the existing directory.

        Hint: The search is case-insensitive.

        Devices are always added, even if the "dev_key" already exists. If this
        is to be prevented, the function "_remove_from_catalog" must be used
        beforehand.

        :param dir_title: Shown title in PiCtory device catalog
        :param dev_key: Unique device key
        :param dev_title: Shown title of device in PiCtory device directory
        :param dev_tooltip: Tooltip for the device on mouse hover
        """
        if exists(self.catalog_file):
            with open(self.catalog_file) as fh:
                lst_catalog = load(fh)  # type: list
        else:
            lst_catalog = []

        device_group = {}
        for search_group in lst_catalog:
            if search_group.get("title", "").lower() == dir_title.lower():
                device_group = search_group

        if not device_group:
            # Directory does not exist, greate a new directory entry in catalog
            device_group["key"] = self._get_kunbus_folder_key(dir_title) or f"k_{uuid4()}"
            device_group["title"] = dir_title
            device_group["folder"] = True
            device_group["children"] = []
            lst_catalog.append(device_group)

        if "children" not in device_group:
            device_group["children"] = []
        device_group["children"].append(
            {
                "key": dev_key,
                "title": dev_title,
                "tooltip": dev_tooltip,
                "icon": "##GSD_ICON_PATHNAME##",
            }
        )

        # Save the catalog file with new module
        with open(self.catalog_file, "w") as fh:
            dump(lst_catalog, fh, indent=2)
            log.debug(f"Saved catalog file to '{self.catalog_file}'")

    def _get_kunbus_folder_key(self, title: str) -> str:
        """
        Search in KUNBUS catalog file for directory title to get its key.

        To add a device to existing KUNBUS directories we need the key of the
        directory object, to create a directory with the same key. This
        function will search the directory key by name.

        Hint: The search is case-insensitive.

        :param title: Directory title to get key
        """
        with open(self.kunbus_catalog_file) as fh:
            kunbus_katalog = load(fh)  # type: list

        for directory in kunbus_katalog:
            if directory.get("title", "") and directory["title"].lower() == title.lower():
                return directory.get("key")

        return ""

    def _load_modules_meta(self):
        modules_meta_file = join(self.install_source, "meta.json")
        with open(modules_meta_file) as fh:
            self.modules_meta = load(fh)

        for module in self.modules_meta:
            log.info("Managing the '{title}' module: {id}".format(**module))

    def _remove_action_rules(self, module_id: str) -> int:
        """
        Remove all versions and all actions of module from action rules file.

        All actions of the passed module ID will be deleted. This also
        includes all versions of the module. If "deviceTypes" no longer
        exists, the entire entry will be removed from the list.

        :param module_id: Module ID to remove actions from
        """
        if not exists(self.action_rules_file):
            # Can not remove anything, if the file does not exist
            return 0

        deleted_rules = 0
        with open(self.action_rules_file) as fh:
            action_rules = load(fh)  # type: list

        for index_action_rule in range(len(action_rules) - 1, -1, -1):
            action_rule = action_rules[index_action_rule]  # type: dict

            # All registered module versions to this action rule
            module_keys = action_rule.get("deviceTypes", [])  # type: list

            for index_module_key in range(len(module_keys) - 1, -1, -1):
                # Remove all module_keys, containing module_id
                module_key = module_keys[index_module_key]  # type: str
                module_regex_match = self.re_rap_file_name.fullmatch(module_key)
                if module_regex_match.group("module_id") == module_id:
                    module_keys.remove(module_key)
                    log.debug(f"Removed '{module_key}' from action rule")

                # Remove complete action rule if no module_key is left
                if not module_keys:
                    action_rules.remove(action_rule)
                    deleted_rules += 1
                    log.info(
                        "Removed '{0}' action rule '{1}'"
                        "".format(module_id, action_rule.get("rule", ""))
                    )

        if not self.use_kunbus_files and len(action_rules) == 0:
            # An empty action rules array will raise an error popup in PiCtory.
            # Always remove the custom action rules file, if containing an empty array.
            remove_file(self.action_rules_file)
        elif deleted_rules:
            # Save the action rules file after removing rules
            with open(self.action_rules_file, "w") as fh:
                dump(action_rules, fh, indent=2)
                log.debug(f"Saved action rules file to '{self.action_rules_file}'")

        return deleted_rules

    def _remove_from_catalog(self, module_id: str, remove_dir=True) -> int:
        """
        Remove all versions in all directories of the given module.

        The specified module ID is removed from all folders in the catalog
        file. If a folder no longer has children, it will also be removed from
        the catalog.

        :param module_id: Module id to remove
        :returns: Number of entries deleted
        """
        if not exists(self.catalog_file):
            # Can not remove anything, if the file does not exist
            return 0

        with open(self.catalog_file) as fh:
            lst_catalog = load(fh)  # type: list

        def remove_item(children: list) -> int:
            """Recursive remove module."""
            int_deleted = 0
            for i in range(len(children) - 1, -1, -1):
                child = children[i]
                if child.get("folder", False):
                    # This is a PiCtory folder with other items
                    int_deleted += remove_item(child.get("children", []))
                    if len(child.get("children", [])) == 0:
                        # Remove empty directory entries
                        children.remove(child)

                else:
                    module_key = child.get("key", "")
                    module_regex_match = self.re_rap_file_name.fullmatch(module_key)
                    if module_regex_match and module_regex_match.group("module_id") == module_id:
                        children.remove(child)
                        int_deleted += 1
                        log.info(f"Removed '{module_key}' from catalog")

            return int_deleted

        # Search the complete catalog including sub folders for the module id
        deleted_items = remove_item(lst_catalog)

        if not self.use_kunbus_files and len(lst_catalog) == 0:
            # An empty catalog array will raise an error popup in PiCtory.
            # Always remove the custom catalog file, if containing an empty array.
            remove_file(self.catalog_file)
        elif deleted_items:
            # Save the catalog file after removing modules
            with open(self.catalog_file, "w") as fh:
                dump(lst_catalog, fh, indent=2)
                log.debug(f"Saved catalog file to '{self.catalog_file}'")

        return deleted_items

    def get_rap_modules(self, root_dir: str) -> Dict[str, List[Tuple[int, int, int]]]:
        """
        Collect all installed modules and their versions.

        All files are processed according to file name rule and included in a
        dictionary object. The key is the module ID and the value is a list
        of all available versions, sorted in descending order (latest version
        at index 0).
        """
        dict_modules = {}
        for file in glob(join(root_dir, "*.rap")):
            file = basename(file)
            file_regex_match = self.re_rap_file_name.fullmatch(file)
            if not file_regex_match:
                # File name does not match for a RAP file
                continue

            module_id = file_regex_match.group("module_id")
            if module_id not in dict_modules:
                dict_modules[module_id] = []
            dict_modules[module_id].append(
                (
                    int(file_regex_match.group("timestamp")),
                    int(file_regex_match.group("major")),
                    int(file_regex_match.group("minor")),
                )
            )

            # Sort the newest version to index 0
            dict_modules[module_id].sort(reverse=True)

        return dict_modules

    def cli_check_rap(self) -> None:
        """Information about the modules as CLI output."""
        # Modules, which this program can install
        modules_to_install = self.get_rap_modules(self.install_source)

        # Modules already installed on the Revolution Pi
        modules_installed = self.get_rap_modules(self.rap_dir)

        for module in self.modules_meta:
            log.debug("Check RAP files for module id '{id}'".format(**module))
            module_id = module.get("id")

            if module_id not in modules_installed:
                print(_("The module '{title}' is NOT yet installed").format(**module))
            elif modules_to_install[module_id][0] == modules_installed[module_id][0]:
                print(
                    _("The module '{title}' is installed in the same version: {0} {1}.{2}").format(
                        *modules_to_install[module_id][0], **module
                    )
                )
            else:
                included_version = modules_to_install[module_id][0]
                installed_version = modules_installed[module_id][0]
                version_string = _("older") if installed_version < included_version else _("newer")

                print(
                    _(
                        "The installed version of '{id}' is {0} than the installable version."
                    ).format(version_string, **module)
                )
                print(
                    _("    Installed: {0} {1}.{2} | Installable: {3} {4}.{5}").format(
                        *installed_version, *included_version
                    )
                )

    def check_environment(self) -> bool:
        """Check PiCtory root directory and meta data."""
        return_code = True
        if exists(self.catalog_file):
            if not access(self.catalog_file, R_OK | W_OK):
                log.error("Permission denied to read and write catalog file")
                return_code = False
        else:
            if not access(dirname(self.catalog_file), R_OK | W_OK | X_OK):
                log.error("Permission denied to create new custom catalog file")
                return_code = False
        if not access(self.rap_dir, R_OK | W_OK):
            log.error("Permission denied to read and wirte in RAP directory")
            return_code = False
        if exists(self.action_rules_file):
            if not access(self.action_rules_file, R_OK | W_OK):
                log.error("Permission denied to read and write action-rules file")
                return_code = False
        else:
            if not access(dirname(self.action_rules_file), R_OK | W_OK | X_OK):
                log.error("Permission denied to create new custom action-rules file")
                return_code = False
        if not access(self.module_image_dir, R_OK | W_OK):
            log.error("Permission denied to read and wirte in device-image  directory")
            return_code = False

        # Check meta data and added rap files
        modules_to_install = self.get_rap_modules(self.install_source)
        for module in self.modules_meta:
            log.debug("Testing files for '{id}'".format(**module))
            module_id = module.get("id")

            if module_id not in modules_to_install:
                # Defined modules in meta file does not exist as rap file
                log.error(f"Can not find installable RAP file for '{module_id}'")
                return_code = False

            if not exists(join(self.install_source, f"{module_id}.png")):
                # Missing module picture
                log.error(f"Can not find module image for '{module_id}'")
                return_code = False

        return return_code

    def install_modules(self) -> None:
        """
        Install module on the system.

        The RAP file and the module image are copied to the system. When
        adding the module to the 'catalog.json', all old versions of the
        module are removed from the catalog beforehand and only the current
        version is added again. In the action rules, this version is added
        in addition to the previous versions. PiCtory still needs this for old
        versions included in existing configurations.
        """

        def create_file_copy(source: str, destination: str) -> None:
            """
            Create a new destination file and write source bytes.

            No copy commands can be used by the operating system. In some
            cases, this application and the source data are packed and the
            operating system could not access the source files. The target
            file is created in the operating system and the data of the source
            is written into it.
            """
            fh_source = open(source, "rb")
            fh_destination = open(destination, "wb")
            with fh_source, fh_destination:
                fh_destination.write(fh_source.read())

        modules_to_install = self.get_rap_modules(self.install_source)

        for module in self.modules_meta:
            log.debug("Installing {id}".format(**module))
            module_id = module.get("id")

            # Create a new image file copy
            image_name = f"{module_id}.png"
            create_file_copy(
                join(self.install_source, image_name),
                join(self.module_image_dir, image_name),
            )
            log.info(f"Installed module picture '{image_name}'")

            # Create a new rap file copy
            module_key = "{id}_{0}_{1}_{2}".format(*modules_to_install[module_id][0], **module)
            rap_name = module_key + ".rap"
            create_file_copy(
                join(self.install_source, rap_name),
                join(self.rap_dir, rap_name),
            )
            log.info(f"Installed module rap file '{rap_name}'")

            # Before inserting this version, we remove all other entries of this module
            self._remove_from_catalog(module_id)

            # Now insert just that version, which we can install
            self._add_to_catalog(
                module.get("dir_title"),
                module_key,
                module.get("title"),
                module.get("tooltip", ""),
            )

            # Apply action rules
            self._add_action_rule(module_key, module.get("action_rules", []))

    def uninstall_modules(self, remove=False) -> None:
        """
        Remove the module from PiCtory catalog.

        All RAP files must remain on the system, as PiCtory no longer works if
        the user has a RAP file in a configuration that is no longer available
        as a file in the system. The removal is only implemented by deleting
        it from the catalog.

        The 'remove' parameter can be used to force the deletion of the RAP
        files and the removal of the action rules. All versions of the module
        are deleted from the system.

        :param remove: Also remove the RAP files and action rules
        """
        if remove:
            log.warning("Removing RAP files from system")

        for module in self.modules_meta:
            log.debug("Uninstalling {id}".format(**module))
            module_id = module.get("id")

            # Remove all versions of this module from catalog
            self._remove_from_catalog(module_id)

            if remove:
                # Remove ALL action rules
                self._remove_action_rules(module_id)

                # Remove ALL versions of rap files
                for file in glob(join(self.rap_dir, f"{module_id}_*_*_*.rap")):
                    log.warning(f"Delete rap file '{file}'")
                    remove_file(file)

                # Remove module picture
                for file in glob(join(self.module_image_dir, f"{module_id}.png")):
                    log.warning(f"Delete image file '{file}'")
                    remove_file(file)
