# SPDX-FileCopyrightText: 2024-present gunungpw <gunungpambudiw@gmail.com>
#
# SPDX-License-Identifier: MIT

from .name import (
    rgb_to_name,
    hex_to_name,
    hsl_to_name,
    lab_to_name,
)

from .colors import NamedColor
from .data import get_data

__all__ = [
    "NamedColor",
    "rgb_to_name",
    "hex_to_name",
    "hsl_to_name",
    "lab_to_name",
]

get_data.download_json_data()
