# Copyright 2019-2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Library to read and write a Zoom R16 project file."""

import io
from importlib import metadata

from . import project
from .effect import Effect
from .project import MUTE, PLAY, REC, Project

__productname__ = __name__
__version__ = metadata.version(__productname__)


# pylint: disable=redefined-builtin
def open(filename, mode="r", **kwargs):
    """
    Open a zoom project file as bytes. The returned object can be
    directly given to `load()` or `dump()`.

    :param mode: reading "r" mode or writing "w" mode.
    :type mode: str

    It's a wrapper around `io.open()` which ensure that `io.open()` is
    used with binary mode.
    """
    if not isinstance(mode, str):
        raise TypeError(f"Invalid mode: {mode}")
    if mode not in ("r", "w"):
        raise ValueError(f"Invalid mode: {mode}. Choose between 'r' or 'w'.")
    # pylint: disable=unspecified-encoding
    return io.open(filename, mode + "b", **kwargs)
