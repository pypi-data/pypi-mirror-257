"""Zoom R16 effects file library"""

# Copyright 2023 Glenn Boysko <gboysko@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .utils import (
    construct_bitmask_value,
    convert_binary_to_ascii,
    convert_binary_to_int,
    convert_byte_to_int,
    initialize_raw_data,
)

# Constants

# The size of the EFFECT file, in bytes
EFFECT_FILE_SIZE = 39032

# The patch number for SEND CHORUS is a 4-byte integer
SEND_CHORUS_PATCH_NUM_OFFSET = 0x58
SEND_CHORUS_PATCH_NUM_LENGTH = 4

# The patch number for SEND REVERB is a 4-byte integer
SEND_REVERB_PATCH_NUM_OFFSET = 0x5C
SEND_REVERB_PATCH_NUM_LENGTH = 4

# SEND EFFECT BITMASK is a single byte that has two mask bits:
# At position 0, if bit is 1 then SEND CHORUS is OFF, otherwise it is ON
# At position 1, if bit is 1 then SEND REVERB is OFF, otherwise it is ON
SEND_EFFECT_BITMASK_OFFSET = 0x62
SEND_EFFECT_BITMASK_LENGTH = 1
SEND_CHORUS_BIT_POS = 0
SEND_REVERB_BIT_POS = 1
SEND_EFFECT_BIT_ON = 0

# The patch name for SEND CHORUS is an 8-character string
SEND_CHORUS_PATCH_NAME_OFFSET = 0xE8
SEND_CHORUS_PATCH_NAME_LENGTH = 8

# The patch name for SEND REVERB is an 8-character string
SEND_REVERB_PATCH_NAME_OFFSET = 0x106
SEND_REVERB_PATCH_NAME_LENGTH = 8

# The location and length of the header for an Effect file
HEADER_TEXT = "ZOOM R-16  EFFECT DATA VER0001"
HEADER_OFFSET = 0
HEADER_LENGTH = 47

# Define the list of CHORUS/DELAY patch names (corresponds positionally
# to patch number)
CHORUS_PATCH_NAMES = [
    "Vocal",
    "GtChorus",
    "Doubling",
    "Echo",
    "Delay3/4",
    "Delay3/2",
    "FastCho",
    "DeepCho",
    "ShortDLY",
    "DeepDBL",
    "SoloLead",
    "WarmyDly",
    "EnhanCho",
    "Detune",
    "Natural",
    "Whole",
    "Delay2/3",
    "Delay1/4",
]

# Define the list of REVERB patch names (corresponds positionally
# to patch number)
REVERB_PATCH_NAMES = [
    "TightHal",
    "BrgtRoom",
    "SoftHall",
    "LargeHal",
    "SmallHal",
    "LiveHous",
    "TrStudio",
    "DarkRoom",
    "VcxRev",
    "Tunnel",
    "BigRoom",
    "PowerSt",
    "BritHall",
    "BudoKan",
    "Ballade",
    "SecBrass",
    "ShortPla",
    "RealPlat",
    "Dome",
    "VinSprin",
    "ClearSpr",
    "Dokan",
]


def load(fp):
    """
    Convert fp (a .read()-supporting file-like object representing the
    content of a efxdata.zdt file as bytes) to a zoomrlib.Effect
    object.

    :param fp: a file-like object with the content of efxdata.zdt as
    byte.
    """
    return Effect(raw=fp.read())


def dump(obj, fp):
    """
    Write obj (a zoomrlib.Effect object) into fp (a .read()-supporting
    file-like object).

    :param obj: a zoomrlib.Effect object.
    :type obj: zoomrlib.Effect

    :param fp: a file-like object with the content of efxdata.zdt as
    byte.
    """
    if not isinstance(obj, Effect):
        raise TypeError(f"Invalid obj type: {type(obj)}")
    return fp.write(obj.raw)


class Effect:
    """Effect for a Zoom R16 Project"""

    def __init__(self, raw=None):
        """A Zoom R16 effect file.

        :param raw: A byte object representing the entire effect file
        content.
        :type raw: byte
        """

        # Initialize our raw data
        self.raw = initialize_raw_data(raw, EFFECT_FILE_SIZE)

        # Was it omitted?
        if raw is None:
            self._set_default()

    @property
    def header(self):
        """Return header of the effect file."""
        return (
            self.raw[HEADER_OFFSET : HEADER_OFFSET + HEADER_LENGTH]
            .decode(encoding="ascii")
            .strip()
        )

    @property
    def valid_header(self):
        """Whether the current Effect instance has a valid header"""

        return self.header == HEADER_TEXT

    @property
    def send_reverb_on(self):
        """Whether the SEND REVERB effect is on or not."""

        # First, determine whether the bit is set (tells whether it is ON or OFF)
        bitmask = convert_byte_to_int(
            self.raw[
                SEND_EFFECT_BITMASK_OFFSET : SEND_EFFECT_BITMASK_OFFSET
                + SEND_EFFECT_BITMASK_LENGTH
            ]
        )
        reverb_on = bitmask & (1 << SEND_REVERB_BIT_POS) == SEND_EFFECT_BIT_ON

        return reverb_on

    @send_reverb_on.setter
    def send_reverb_on(self, value):
        """Sets whether the SEND REVERB effect is on or not."""

        # Get the current value of the SEND CHORUS effect
        chorus_on = self.send_chorus_on

        # Construct the correct bitmask involves taking the supplied setting
        # for REVERB and adding it to the bitmask value for the other SEND EFFECT
        # (namely, CHORUS). In both cases, a value of `1` indicates that the
        # effect is OFF, hence we negate the value.
        bitmask = construct_bitmask_value(
            not value, SEND_REVERB_BIT_POS
        ) + construct_bitmask_value(not chorus_on, SEND_CHORUS_BIT_POS)

        # Store the bitmask value back
        self.raw[
            SEND_EFFECT_BITMASK_OFFSET : SEND_EFFECT_BITMASK_OFFSET
            + SEND_EFFECT_BITMASK_LENGTH
        ] = bitmask.to_bytes(SEND_EFFECT_BITMASK_LENGTH, "little")

    @property
    def send_reverb_patch_num(self):
        """What the current SEND REVERB patch number is (or None, if not set)."""

        # Is the SEND REVERB off? If so, return None
        if not self.send_reverb_on:
            return None

        # Get the reverb patch number
        reverb_num = convert_binary_to_int(
            self.raw[
                SEND_REVERB_PATCH_NUM_OFFSET : SEND_REVERB_PATCH_NUM_OFFSET
                + SEND_REVERB_PATCH_NUM_LENGTH
            ]
        )

        return reverb_num

    @property
    def send_reverb_patch_name(self):
        """What the current SEND REVERB patch name is (or None, if not set)."""

        # Is the SEND REVERB off? If so, return None
        if not self.send_reverb_on:
            return None

        # Get the chorus patch name
        reverb_name = convert_binary_to_ascii(
            self.raw[
                SEND_REVERB_PATCH_NAME_OFFSET : SEND_REVERB_PATCH_NAME_OFFSET
                + SEND_REVERB_PATCH_NAME_LENGTH
            ]
        ).strip()

        return reverb_name

    def set_send_reverb_patch(self, *, patch_num=None, patch_name=None):
        """Set the SEND REVERB patch using either the number or name."""

        # If both the name and number are None, then return with an error
        if patch_num is None and patch_name is None:
            raise ValueError("Both SEND REVERB patch name and number are None")

        # Are they both set?
        if not patch_num is None and not patch_name is None:
            # Is the patch number not an integer or the patch name not a string?
            if not isinstance(patch_num, int) or not isinstance(
                patch_name, str
            ):
                raise TypeError(
                    "Either the SEND REVERB patch name is not a string "
                    "or the patch number is not an integer"
                )

            # Is the patch number out of the valid range?
            if patch_num < 0 or patch_num >= len(REVERB_PATCH_NAMES):
                raise ValueError(
                    "The patch number is either less than 0 or greater than "
                    "the maximum valid patch number "
                    f"[{len(REVERB_PATCH_NAMES) - 1}]: {patch_num}"
                )

            # Find the correct patch name for the specified patch number
            expected_name = REVERB_PATCH_NAMES[patch_num]

            # Does the name NOT match what it provided?
            if expected_name != patch_name:
                raise ValueError(
                    f"The patch name supplied [{patch_name}] does not match "
                    f"the one associated with the number [{patch_num}]: "
                    f"expected '{expected_name}'"
                )

            # Set the name (normalizing to its appropriate length)
            norm_patch_name = patch_name.ljust(SEND_REVERB_PATCH_NAME_LENGTH)
            bvalue = norm_patch_name.encode(encoding="ascii")
            self.raw[
                SEND_REVERB_PATCH_NAME_OFFSET : SEND_REVERB_PATCH_NAME_OFFSET
                + SEND_REVERB_PATCH_NAME_LENGTH
            ] = bvalue

            # Set the number
            self.raw[
                SEND_REVERB_PATCH_NUM_OFFSET : SEND_REVERB_PATCH_NUM_OFFSET
                + SEND_REVERB_PATCH_NUM_LENGTH
            ] = patch_num.to_bytes(
                SEND_REVERB_PATCH_NUM_LENGTH, byteorder="little"
            )

    @property
    def send_chorus_on(self):
        """Whether the SEND CHORUS effect is on or not."""

        # First, determine whether the bit is set (tells whether it is ON or OFF)
        bitmask = convert_byte_to_int(
            self.raw[
                SEND_EFFECT_BITMASK_OFFSET : SEND_EFFECT_BITMASK_OFFSET
                + SEND_EFFECT_BITMASK_LENGTH
            ]
        )
        chorus_on = bitmask & (1 << SEND_CHORUS_BIT_POS) == SEND_EFFECT_BIT_ON

        return chorus_on

    @send_chorus_on.setter
    def send_chorus_on(self, value):
        """Sets whether the SEND CHORUS effect is on or not."""

        # Get the current value of the SEND REVERB effect
        reverb_on = self.send_reverb_on

        # Construct the correct bitmask involves taking the supplied setting
        # for CHORUS and adding it to the bitmask value for the other SEND EFFECT
        # (namely, REVERB). In both cases, a value of `1` indicates that the
        # effect is OFF, hence we negate the value.
        bitmask = construct_bitmask_value(
            not value, SEND_CHORUS_BIT_POS
        ) + construct_bitmask_value(not reverb_on, SEND_REVERB_BIT_POS)

        # Store the bitmask value back
        self.raw[
            SEND_EFFECT_BITMASK_OFFSET : SEND_EFFECT_BITMASK_OFFSET
            + SEND_EFFECT_BITMASK_LENGTH
        ] = bitmask.to_bytes(SEND_EFFECT_BITMASK_LENGTH, "little")

    @property
    def send_chorus_patch_num(self):
        """What the current SEND CHORUS patch number is (or None, if not set)."""

        # Is the SEND CHORUS off? If so, return None
        if not self.send_chorus_on:
            return None

        # Get the chorus patch number
        chorus_num = convert_binary_to_int(
            self.raw[
                SEND_CHORUS_PATCH_NUM_OFFSET : SEND_CHORUS_PATCH_NUM_OFFSET
                + SEND_CHORUS_PATCH_NUM_LENGTH
            ]
        )

        return chorus_num

    @property
    def send_chorus_patch_name(self):
        """What the current SEND CHORUS patch name is (or None, if not set)."""

        # Is the SEND CHORUS off? If so, return None
        if not self.send_chorus_on:
            return None

        # Get the chorus patch name
        chorus_name = convert_binary_to_ascii(
            self.raw[
                SEND_CHORUS_PATCH_NAME_OFFSET : SEND_CHORUS_PATCH_NAME_OFFSET
                + SEND_CHORUS_PATCH_NAME_LENGTH
            ]
        ).strip()

        return chorus_name

    def set_send_chorus_patch(self, *, patch_num=None, patch_name=None):
        """Set the SEND CHORUS patch using either the number or name."""

        # If both the name and number are None, then return with an error
        if patch_num is None and patch_name is None:
            raise ValueError("Both SEND CHORUS patch name and number are None")

        # Are they both set?
        if not patch_num is None and not patch_name is None:
            # Is the patch number not an integer or the patch name not a string?
            if not isinstance(patch_num, int) or not isinstance(
                patch_name, str
            ):
                raise TypeError(
                    "Either the SEND CHORUS patch name is not a string "
                    "or the patch number is not an integer"
                )

            # Is the patch number out of the valid range?
            if patch_num < 0 or patch_num >= len(CHORUS_PATCH_NAMES):
                raise ValueError(
                    "The patch number is either less than 0 or greater than "
                    "the maximum valid patch number "
                    f"[{len(CHORUS_PATCH_NAMES) - 1}]: {patch_num}"
                )

            # Find the correct patch name for the specified patch number
            expected_name = CHORUS_PATCH_NAMES[patch_num]

            # Does the name NOT match what it provided?
            if expected_name != patch_name:
                raise ValueError(
                    f"The patch name supplied [{patch_name}] does not match "
                    f"the one associated with the number [{patch_num}]: "
                    f" expected '{expected_name}'"
                )

            # Set the name (normalizing to its appropriate length)
            norm_patch_name = patch_name.ljust(SEND_CHORUS_PATCH_NAME_LENGTH)
            bvalue = norm_patch_name.encode(encoding="ascii")
            self.raw[
                SEND_CHORUS_PATCH_NAME_OFFSET : SEND_CHORUS_PATCH_NAME_OFFSET
                + SEND_CHORUS_PATCH_NAME_LENGTH
            ] = bvalue

            # Set the number
            self.raw[
                SEND_CHORUS_PATCH_NUM_OFFSET : SEND_CHORUS_PATCH_NUM_OFFSET
                + SEND_CHORUS_PATCH_NUM_LENGTH
            ] = patch_num.to_bytes(
                SEND_CHORUS_PATCH_NUM_LENGTH, byteorder="little"
            )

    def _set_default(self):
        """Set default value to the effect."""
        self.raw[
            HEADER_OFFSET : HEADER_OFFSET + HEADER_LENGTH
        ] = HEADER_TEXT.ljust(HEADER_LENGTH).encode(encoding="ascii")
