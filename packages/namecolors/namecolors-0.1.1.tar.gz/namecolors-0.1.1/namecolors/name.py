import json
import os
from typing import TypeAlias, Literal

data_path = os.path.dirname(__file__)

ColorDB: TypeAlias = Literal[
    "default",
    "bestOf",
    "wikipedia",
    "french",
    "spanish",
    "german",
    "ridgway",
    "risograph",
    "basic",
    "chineseTraditional",
    "html",
    "japaneseTraditional",
    "leCorbusier",
    "nbsIscc",
    "ntc",
    "osxcrayons",
    "ral",
    "sanzoWadaI",
    "thesaurus",
    "werner",
    "windows",
    "x11",
    "xkcd",
]


def hex_to_name(hex: str, color_db: ColorDB = "default") -> str | None:
    """Converts a hexadecimal color representation to its corresponding color name.

    Args:
        hex (str): The hexadecimal color representation.
        color_db (ColorDB, optional): The color database to use. Defaults to "default".

    Returns:
        str | None: The corresponding color name if found, otherwise None.
    """
    with open(f"{data_path}\\data\\{color_db}.json", "r") as f:
        color_name = json.load(f)

    for color in color_name["colors"]:
        if color["hex"] == hex.lower():
            return color["name"]
    return None


def rgb_to_name(rgb: tuple[int, int, int], color_db: ColorDB = "default") -> str | None:
    """Converts an RGB color representation to its corresponding color name.

    Args:
        rgb (tuple[int, int, int]): The RGB color representation as a tuple of integers (R, G, B).
        color_db (ColorDB, optional): The color database to use. Defaults to "default".

    Returns:
        str | None: The corresponding color name if found, otherwise None.
    """

    with open(f"{data_path}\\data\\{color_db}.json", "r") as f:
        color_name = json.load(f)

    for color in color_name["colors"]:
        if (color["rgb"]["r"], color["rgb"]["g"], color["rgb"]["b"]) == rgb:
            return color["name"]
    return None


def hsl_to_name(hsl: tuple[int, int, int], color_db: ColorDB = "default") -> str | None:
    """Converts an HSL color representation to its corresponding color name.

    Args:
        hsl (tuple[int, int, int]): The HSL color representation as a tuple of integers (H, S, L).
        color_db (ColorDB, optional): The color database to use. Defaults to "default".

    Returns:
        str | None: The corresponding color name if found, otherwise None.
    """
    with open(f"{data_path}\\data\\{color_db}.json", "r") as f:
        color_name = json.load(f)

    for color in color_name["colors"]:
        if (color["hsl"]["h"], color["hsl"]["s"], color["hsl"]["l"]) == hsl:
            return color["name"]
    return None


def lab_to_name(lab: tuple[int, int, int], color_db: ColorDB = "default") -> str | None:
    """Converts a LAB color representation to its corresponding color name.

    Args:
        lab (tuple[int, int, int]): The LAB color representation as a tuple of integers (L, A, B).
        color_db (ColorDB, optional): The color database to use. Defaults to "default".

    Returns:
        str | None: The corresponding color name if found, otherwise None.
    """
    with open(f"{data_path}\\data\\{color_db}.json", "r") as f:
        color_name = json.load(f)

    for color in color_name["colors"]:
        if (color["lab"]["l"], color["lab"]["a"], color["lab"]["b"]) == lab:
            return color["name"]
    return None
