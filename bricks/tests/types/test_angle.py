from bricks.source.types.angle import Angle
from bricks.source.types.angle import Quadrant
from bricks.source.types.angle import _calc_quadrant
from bricks.source.types.angle import _is_in_quadrant_I
from bricks.source.types.angle import _is_in_quadrant_II
from bricks.source.types.angle import _is_in_quadrant_III
from bricks.source.types.angle import _is_in_quadrant_IV
from bricks.source.types.angle import _calc_angle_if_out_of_rangle

from pytest import approx
from numpy import deg2rad


class TestAngle:
    def test_init(self):
        obj = Angle()
        assert obj.value == 0.0
        assert obj.quadrant == Quadrant.I
        assert obj.quadrant_angle == 0.0

    def test_value(self):
        obj = Angle(deg2rad(30.0))
        assert obj.value == deg2rad(30.0)

        obj.value = deg2rad(65.0)
        assert obj.value == deg2rad(65.0)

    def test_quadrant_angle(self):
        obj = Angle(deg2rad(30.0))

        assert obj.value == deg2rad(30.0)
        assert obj.quadrant_angle == deg2rad(30.0)

        obj.quadrant_angle = deg2rad(60.0)

        assert obj.value == deg2rad(60.0)
        assert obj.quadrant_angle == deg2rad(60.0)

    def test_quadrant(self):
        obj = Angle(deg2rad(30.0))
        assert obj.quadrant == Quadrant.I

        obj.quadrant = Quadrant.III
        assert obj.quadrant == Quadrant.III


def test_calc_quadrant_true():
    assert _calc_quadrant(deg2rad(0.0)) == Quadrant.I
    assert _calc_quadrant(deg2rad(45.0)) == Quadrant.I
    assert _calc_quadrant(deg2rad(90.0)) == Quadrant.I
    assert _calc_quadrant(deg2rad(90.1)) == Quadrant.II
    assert _calc_quadrant(deg2rad(135.0)) == Quadrant.II
    assert _calc_quadrant(deg2rad(180.0)) == Quadrant.II
    assert _calc_quadrant(deg2rad(180.1)) == Quadrant.III
    assert _calc_quadrant(deg2rad(225.0)) == Quadrant.III
    assert _calc_quadrant(deg2rad(270.0)) == Quadrant.III
    assert _calc_quadrant(deg2rad(270.1)) == Quadrant.IV
    assert _calc_quadrant(deg2rad(315.0)) == Quadrant.IV
    assert _calc_quadrant(deg2rad(360.0)) == Quadrant.IV


def test_is_in_quarant_I_true():
    assert _is_in_quadrant_I(deg2rad(0.0)) == True
    assert _is_in_quadrant_I(deg2rad(45.0)) == True
    assert _is_in_quadrant_I(deg2rad(90.0)) == True


def test_is_in_quarant_I_false():
    assert _is_in_quadrant_I(deg2rad(90.1)) == False
    assert _is_in_quadrant_I(deg2rad(135.0)) == False
    assert _is_in_quadrant_I(deg2rad(180.0)) == False
    assert _is_in_quadrant_I(deg2rad(180.1)) == False
    assert _is_in_quadrant_I(deg2rad(225.0)) == False
    assert _is_in_quadrant_I(deg2rad(270.0)) == False
    assert _is_in_quadrant_I(deg2rad(270.1)) == False
    assert _is_in_quadrant_I(deg2rad(315.0)) == False
    assert _is_in_quadrant_I(deg2rad(360.0)) == False


def test_is_in_quarant_II_true():
    assert _is_in_quadrant_II(deg2rad(90.1)) == True
    assert _is_in_quadrant_II(deg2rad(135.0)) == True
    assert _is_in_quadrant_II(deg2rad(180.0)) == True


def test_is_in_quarant_II_false():
    assert _is_in_quadrant_II(deg2rad(0.0)) == False
    assert _is_in_quadrant_II(deg2rad(45.0)) == False
    assert _is_in_quadrant_II(deg2rad(90.0)) == False
    assert _is_in_quadrant_II(deg2rad(180.1)) == False
    assert _is_in_quadrant_II(deg2rad(225.0)) == False
    assert _is_in_quadrant_II(deg2rad(270.0)) == False
    assert _is_in_quadrant_II(deg2rad(270.1)) == False
    assert _is_in_quadrant_II(deg2rad(315.0)) == False
    assert _is_in_quadrant_II(deg2rad(360.0)) == False


def test_is_in_quarant_III_true():
    assert _is_in_quadrant_III(deg2rad(180.1)) == True
    assert _is_in_quadrant_III(deg2rad(225.0)) == True
    assert _is_in_quadrant_III(deg2rad(270.0)) == True


def test_is_in_quarant_III_false():
    assert _is_in_quadrant_III(deg2rad(0.0)) == False
    assert _is_in_quadrant_III(deg2rad(45.0)) == False
    assert _is_in_quadrant_III(deg2rad(90.0)) == False
    assert _is_in_quadrant_III(deg2rad(90.1)) == False
    assert _is_in_quadrant_III(deg2rad(135.0)) == False
    assert _is_in_quadrant_III(deg2rad(180.0)) == False
    assert _is_in_quadrant_III(deg2rad(270.1)) == False
    assert _is_in_quadrant_III(deg2rad(315.0)) == False
    assert _is_in_quadrant_III(deg2rad(360.0)) == False


def test_is_in_quarant_IV_true():
    assert _is_in_quadrant_IV(deg2rad(270.1)) == True
    assert _is_in_quadrant_IV(deg2rad(315.0)) == True
    assert _is_in_quadrant_IV(deg2rad(360.0)) == True


def test_is_in_quarant_IV_false():
    assert _is_in_quadrant_IV(deg2rad(0.0)) == False
    assert _is_in_quadrant_IV(deg2rad(45.0)) == False
    assert _is_in_quadrant_IV(deg2rad(90.0)) == False
    assert _is_in_quadrant_IV(deg2rad(90.1)) == False
    assert _is_in_quadrant_IV(deg2rad(135.0)) == False
    assert _is_in_quadrant_IV(deg2rad(180.0)) == False
    assert _is_in_quadrant_IV(deg2rad(180.1)) == False
    assert _is_in_quadrant_IV(deg2rad(225.0)) == False
    assert _is_in_quadrant_IV(deg2rad(270.0)) == False


def test_calc_angle_if_out_of_range():
    assert _calc_angle_if_out_of_rangle(deg2rad(0.0)) == approx(deg2rad(0.0))
    assert _calc_angle_if_out_of_rangle(deg2rad(360.0)) == approx(
        deg2rad(360.0)
    )
    assert _calc_angle_if_out_of_rangle(deg2rad(360.1)) == approx(deg2rad(0.1))
    assert _calc_angle_if_out_of_rangle(deg2rad(540.0)) == approx(
        deg2rad(180.0)
    )

    assert _calc_angle_if_out_of_rangle(deg2rad(-0.1)) == approx(
        deg2rad(359.9)
    )
    assert _calc_angle_if_out_of_rangle(deg2rad(-360.0)) == approx(
        deg2rad(0.0)
    )
    assert _calc_angle_if_out_of_rangle(deg2rad(-540.0)) == approx(
        deg2rad(180.0)
    )

