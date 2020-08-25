from __future__ import annotations


class RGBColor:
    def __init__(self, r: int, g: int, b: int, a: int = 0xFF):
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

    def lighter(self, factor: float):
        return RGBColor(
            r=calc_lighter_part(self._r, factor),
            g=calc_lighter_part(self._g, factor),
            b=calc_lighter_part(self._b, factor),
        )

    def darker(self, factor: float):
        return RGBColor(
            r=calc_darker_part(self._r, factor),
            g=calc_darker_part(self._g, factor),
            b=calc_darker_part(self._b, factor),
        )

    def grayscale(self) -> RGBColor:
        return RGBColor(
            r=self._r * 0.2126, g=self._g * 0.7152, b=self._b * 0.0722
        )


def _check_args(value: int) -> int:
    if value < 0x00 or value > 0xFF:
        raise ValueError(
            "int RGBColor::checkArgs(int value)\n"
            "Value must be >= 0x00 and <= 0xFF\n"
            "Value: %s\n" % (value)
        )
    return value


def calc_lighter_part(part: int, factor: float) -> int:
    return _clamp(0x00, part + (0xFF - part) * factor, 0xFF)


def calc_darker_part(part: int, factor: float) -> int:
    return _clamp(0x00, part * (1.0 - factor), 0xFF)


def _clamp(minimum, x, maximum) -> float:
    return max(minimum, min(x, maximum))
