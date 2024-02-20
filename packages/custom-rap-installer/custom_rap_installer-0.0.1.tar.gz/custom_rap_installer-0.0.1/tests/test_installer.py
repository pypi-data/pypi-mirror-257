# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Package: custom_rap_installer."""

from os.path import dirname
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest
from custom_rap_installer import PiCtoryManager


class Environment:
    """Temporary test environment."""

    def __init__(self) -> None:
        # Use temporary directory as pictory root
        self.install_root = TemporaryDirectory(prefix="custom_rap_installer_")

        # Set directories for testing
        self.path_source = Path(dirname(__file__)).joinpath("modules")
        self.path_root = Path(self.install_root.name)
        self.path_data = self.path_root.joinpath("resources", "data")
        self.path_rap = self.path_data.joinpath("rap")
        self.path_images = self.path_root.joinpath("resources", "images", "devices")

        # Create all directories
        self.path_rap.mkdir(parents=True, exist_ok=True)
        self.path_images.mkdir(parents=True, exist_ok=True)

        # Set files for testing the content
        self.file_catalog_kunbus = self.path_data.joinpath("catalog.json")
        self.file_catalog_custom = self.path_data.joinpath("catalog-custom.json")
        self.file_actionrules_kunbus = self.path_rap.joinpath("actionRules.json")
        self.file_actionrules_custom = self.path_rap.joinpath("actionRules-custom.json")

    def cleanup(self) -> None:
        self.install_root.cleanup()


@pytest.fixture
def temp_environment() -> Generator[Environment, None, None]:
    """Get temporary test environment."""
    env = Environment()
    yield env
    env.cleanup()


def test_environment(temp_environment: Environment) -> None:
    """Check environment for the library to work."""
    pictory_manager = PiCtoryManager(
        str(temp_environment.path_source),
        str(temp_environment.path_root),
    )

    assert pictory_manager.check_environment()
