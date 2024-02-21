"""Utility functions shared between Project and Effect."""

# Copyright 2023 Glenn Boysko <gboysko@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from itertools import takewhile
from struct import unpack


def initialize_raw_data(raw, default_size):
    """
    Initialize the raw data, depending on its type.

    :param raw: A byte object representing the entire file contents. May be None.
    :param default_size: If raw is None, the size of the created bytearray.

    """

    if raw is None:
        return bytearray(default_size)
    if isinstance(raw, bytes):
        return bytearray(raw)
    if isinstance(raw, bytearray):
        return raw

    raise TypeError(f"Invalid type: {raw}")


def convert_byte_to_int(binary_data):
    """Convert a byte to an integer"""

    return unpack("B", binary_data)[0]


def convert_binary_to_int(binary_data):
    """Convert a binary data array into an integer"""

    # If the length is greater than 4, complain...
    if len(binary_data) > 4:
        raise ValueError(
            "Unexpected: Trying to convert more than 4 bytes to an integer."
        )

    return unpack("i", binary_data)[0]


def convert_binary_to_ascii(binary_data):
    """Convert a binary data array into an ascii string"""

    # Loop through the binary data array until the first NULL character
    ascii_characters = (
        chr(int(byte)) for byte in takewhile(lambda x: x != 0, binary_data)
    )

    return "".join(ascii_characters)


def construct_bitmask_value(bit_is_on, bit_position):
    """Convert bitmask value for a bit at a particular position."""

    # If the bit_is_on is False, then return 0
    if not bit_is_on:
        return 0

    return 1 << bit_position
