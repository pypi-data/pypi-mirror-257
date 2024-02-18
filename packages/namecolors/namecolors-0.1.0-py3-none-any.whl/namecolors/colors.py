# color.py

from . import name


class NamedColor:
    """
    Represents a color with a name from a specified color database.

    Attributes:
        system: The color system ('RGB', 'HSL', 'LAB').
        coordinate: The coordinates representing the color.
        value_hex: The hexadecimal representation of the color value.
    """

    def __init__(self, input: tuple[str, int, int, int]) -> None:
        """
        Initializes a NamedColor instance.

        Args:
            input: A tuple containing the color system and its coordinates.
        """
        self.system, *self.coordinate = input
        self.value_hex: str | None = None
        if self.system.upper() in ("RGB", "HSL", "LAB"):
            if self.system == "RGB":
                self.value_hex = rgb_to_hex(self.coordinate)
            elif self.system == "HSL":
                self.value_hex = rgb_to_hex(self.coordinate)
            elif self.system == "LAB":
                self.value_hex = rgb_to_hex(self.coordinate)
            else:
                raise NotImplementedError

    @property
    def hex(self) -> str | None:
        """
        Gets the hexadecimal representation of the color value.

        Returns:
            str | None: The hexadecimal color value or None if not available.
        """
        return self.value_hex

    @property
    def name(self) -> str | None:
        """
        Gets the name of the color based on its hexadecimal representation.

        Returns:
            str: The name of the color if found, otherwise a message indicating
            that the name is not found.
        """
        if self.value_hex is None:
            return f"{self.value_hex} name is not found"
        return name.hex_to_name(self.value_hex)

    def __str__(self) -> str:
        """
        Returns a string representation of the NamedColor instance.

        Returns:
            str: A string representation of the NamedColor.
        """
        return f"{self.system}, {self.coordinate}"


def rgb_to_hex(rgb) -> str | None:
    return "#{:02x}{:02x}{:02x}".format(*rgb)
