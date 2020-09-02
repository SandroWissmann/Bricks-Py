"""Representation of an RGBColor."""

from __future__ import annotations
from typing import Tuple


class RGBColor:
    """
    Representation of an RGBColor.

    Attributes
    ----------
    r : int 
        Red part of color
    g : int 
        Green part of color
    b : int 
        Blue part of color
    a : int 
        Alpha part of color

    Methods
    -------
    lighter(self, factor: float = 0.3) -> RGBColor:
        Returns the RGBColor slightly lighter.
    darker(self, factor: float = 0.3) -> RGBColor:
        Returns the RGBColor slightly darker.
    grayscale(self) -> RGBColor:
        Returns the color as grayscale.
    as_tuple(self) -> Tuple[int, int, int, int]:
        Returns color as tuple for convenient use.
    """

    def __init__(self, r: int, g: int, b: int, a: int = 0xFF):
        """Takes rgba values. Raises ValueError iff out of range 0 - 0xFF"""
        self._r = _check_args(r)
        self._g = _check_args(g)
        self._b = _check_args(b)
        self._a = _check_args(a)

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> int:
        return self._a

    def lighter(self, factor: float = 0.3) -> RGBColor:
        """
        Returns the RGBColor slightly lighter. Can be adjusted with factor
        """
        return RGBColor(
            r=_calc_lighter_part(self._r, factor),
            g=_calc_lighter_part(self._g, factor),
            b=_calc_lighter_part(self._b, factor),
        )

    def darker(self, factor: float = 0.3) -> RGBColor:
        """
        Returns the RGBColor slightly darker. Can be adjusted with factor
        """
        return RGBColor(
            r=_calc_darker_part(self._r, factor),
            g=_calc_darker_part(self._g, factor),
            b=_calc_darker_part(self._b, factor),
        )

    def grayscale(self) -> RGBColor:
        """
        Returns the color as grayscale.
        """
        return RGBColor(
            r=int(self._r * 0.2126),
            g=int(self._g * 0.7152),
            b=int(self._b * 0.0722),
        )

    def as_tuple(self) -> Tuple[int, int, int, int]:
        """
        Returns color as tuple for convenient use
        """
        return self._r, self._g, self._b, self._a


def _check_args(value: int) -> int:
    if value < 0x00 or value > 0xFF:
        raise ValueError(
            "int RGBColor::checkArgs(int value)\n"
            "Value must be >= 0x00 and <= 0xFF\n"
            "Value: %s\n" % (value)
        )
    return value


def _calc_lighter_part(part: int, factor: float) -> int:
    return int(_clamp(0x00, part + (0xFF - part) * factor, 0xFF))


def _calc_darker_part(part: int, factor: float) -> int:
    return int(_clamp(0x00, part * (1.0 - factor), 0xFF))


def _clamp(minimum: float, x: float, maximum: float) -> float:
    return max(minimum, min(x, maximum))
