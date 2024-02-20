# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 KUNBUS GmbH
# SPDX-License-Identifier: GPL-2.0-or-later
"""Test module import."""


def test_import() -> None:
    """Test the import of the module."""
    import custom_rap_installer

    assert type(custom_rap_installer.__version__) is str
