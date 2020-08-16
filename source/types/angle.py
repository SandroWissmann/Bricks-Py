from enum import IntEnum
from numpy import deg2rad


class Quadrant(IntEnum):
    I = 0
    II = 1
    III = 2
    IV = 3


class Angle:
    def __init__(self, angle: float = 0.0):
        self.quadrant = _calc_quadrant(angle)
        self.quadrant_angle = _angle_to_quadrant_angle(angle, self.quadrant)

    @property
    def value(self) -> float:
        return _quadrant_angle_to_angle(self.quadrant_angle, self.quadrant)

    @value.setter
    def value(self, value: float):
        value = _calc_angle_if_out_of_rangle(value)
        self.quadrant = _calc_quadrant(value)
        self.quadrant_angle = _angle_to_quadrant_angle(value, self.quadrant)

    @property
    def quadrant_angle(self) -> float:
        return self._quadrant_angle

    @quadrant_angle.setter
    def quadrant_angle(self, quadrant_angle: float) -> float:
        if quadrant_angle < deg2rad(0.0) or quadrant_angle > deg2rad(90.0):
            print(
                "class Angle: def set_quadrant_angle(self, quadrant_angle):\n"
                "Out of Range 0.0_deg to 90.0_deg\n"
                "suplied anngle:%s\n" % quadrant_angle
            )
            quadrant_angle = _clamp(
                deg2rad(0.0), quadrant_angle, deg2rad(90.0)
            )
        self._quadrant_angle = quadrant_angle

    def mirror_horizontal(self):
        if self.quadrant == Quadrant.I:
            self.quadrant = Quadrant.IV
        elif self.quadrant == Quadrant.II:
            self.quadrant = Quadrant.III
        elif self.quadrant == Quadrant.III:
            self.quadrant = Quadrant.II
        elif self.quadrant == Quadrant.IV:
            self.quadrant = Quadrant.I
        self.quadrant_angle = _mirror_quadrant_angle(self.quadrant_angle)


def _clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def _mirror_quadrant_angle(quadrant_angle: float) -> float:
    return deg2rad(90.0) - quadrant_angle


def _calc_quadrant(angle: float) -> float:
    assert deg2rad(0.0) <= angle <= deg2rad(360.0)

    if _is_in_quadrant_I(angle):
        return Quadrant.I
    if _is_in_quadrant_II(angle):
        return Quadrant.II
    if _is_in_quadrant_III(angle):
        return Quadrant.III
    if _is_in_quadrant_IV(angle):
        return Quadrant.IV


def _is_in_quadrant_I(angle: float) -> float:
    return deg2rad(0.0) <= angle <= deg2rad(90.0)


def _is_in_quadrant_II(angle: float) -> float:
    return deg2rad(90.0) < angle <= deg2rad(180.0)


def _is_in_quadrant_III(angle: float) -> float:
    return deg2rad(180.0) < angle <= deg2rad(270.0)


def _is_in_quadrant_IV(angle: float) -> float:
    return deg2rad(270.0) < angle <= deg2rad(360.0)


def _angle_to_quadrant_angle(angle: float, quadrant: Quadrant) -> float:
    return angle - deg2rad(90.0) * quadrant


def _quadrant_angle_to_angle(quadrant_angle: float, quadrant: Quadrant):
    return quadrant_angle + deg2rad(90.0) * quadrant


def _calc_angle_if_out_of_rangle(angle: float) -> float:
    while angle < deg2rad(0.0):
        angle += deg2rad(360)
    while angle > deg2rad(360.0):
        angle -= deg2rad(360.0)
    return angle
