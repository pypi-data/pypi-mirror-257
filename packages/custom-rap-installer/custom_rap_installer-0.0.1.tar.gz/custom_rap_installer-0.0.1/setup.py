# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH <support@kunbus.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Setup-script for Custom RAP Installer."""

from setuptools import find_namespace_packages, setup

from src.custom_rap_installer.__about__ import __version__

with open("README.md") as fh:
    # Load long description from readme file
    long_description = fh.read()

setup(
    name="custom_rap_installer",
    version=__version__,
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">= 3.7",
    install_requires=[
        # todo: Set Dependencies of this project
    ],
    entry_points={},
    platforms=["revolution pi"],
    url="https://revolutionpi.com/",
    license="GPL-2.0-or-later",
    license_files=["LICENSES/*"],
    author="Sven Sager",
    author_email="s.sager@kunbus.com",
    maintainer="KUNBUS GmbH",
    maintainer_email="support@kunbus.com",
    description="Install custom RAP files for use in PiCtory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["revpi", "revolution pi", "pictory"],
    classifiers=[
        # A list of all classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        # todo: Change this after beta to "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
