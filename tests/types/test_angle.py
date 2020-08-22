from source.types.angle import Angle
from source.types.angle import Quadrant
from source.types.angle import _calc_quadrant
from source.types.angle import _is_in_quadrant_I
from source.types.angle import _is_in_quadrant_II
from source.types.angle import _is_in_quadrant_III
from source.types.angle import _is_in_quadrant_IV
from source.types.angle import _calc_angle_if_out_of_rangle

import pytest
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

    @pytest.mark.parametrize(
        "quadrant_before, quadrant_after, angle_before, angle_after",
        [
            (Quadrant.I, Quadrant.IV, 30.0, 330.0),
            (Quadrant.II, Quadrant.III, 120.0, 240.0),
            (Quadrant.III, Quadrant.II, 240.0, 120.0),
            (Quadrant.IV, Quadrant.I, 330.0, 30.0),
        ],
    )
    def test_mirror_horizontal(
        self,
        quadrant_before: Quadrant,
        quadrant_after: Quadrant,
        angle_before: float,
        angle_after: float,
    ):
        obj = Angle(deg2rad(angle_before))
        assert obj.quadrant == quadrant_before

        obj.mirror_horizontal()
        assert obj.quadrant == quadrant_after
        assert obj.value == approx(deg2rad(angle_after))

    @pytest.mark.parametrize(
        "quadrant_before, quadrant_after, angle_before, angle_after",
        [
            (Quadrant.I, Quadrant.II, 30.0, 150.0),
            (Quadrant.II, Quadrant.I, 150.0, 30.0),
            (Quadrant.III, Quadrant.IV, 210.0, 330.0),
            (Quadrant.IV, Quadrant.III, 330.0, 210.0),
        ],
    )
    def test_mirror_vertical(
        self,
        quadrant_before: Quadrant,
        quadrant_after: Quadrant,
        angle_before: float,
        angle_after: float,
    ):
        obj = Angle(deg2rad(angle_before))
        assert obj.quadrant == quadrant_before

        obj.mirror_vertical()
        assert obj.quadrant == quadrant_after
        assert obj.value == approx(deg2rad(angle_after))


@pytest.mark.parametrize(
    "angle, quadrant",
    [
        (0.0, Quadrant.I),
        (45.0, Quadrant.I),
        (90.0, Quadrant.I),
        (90.1, Quadrant.II),
        (135.0, Quadrant.II),
        (180.0, Quadrant.II),
        (180.1, Quadrant.III),
        (225.0, Quadrant.III),
        (270.0, Quadrant.III),
        (270.1, Quadrant.IV),
        (315.0, Quadrant.IV),
        (360.0, Quadrant.IV),
    ],
)
def test_calc_quadrant_true(angle, quadrant):
    assert _calc_quadrant(deg2rad(angle)) == quadrant


@pytest.mark.parametrize(
    "angle, result",
    [
        (0.0, True),
        (45.0, True),
        (90.0, True),
        (90.1, False),
        (135.0, False),
        (180.0, False),
        (180.1, False),
        (225.0, False),
        (270.0, False),
        (270.1, False),
        (315.0, False),
        (360.0, False),
    ],
)
def test_is_in_quarant_I(angle: Angle, result: bool):
    assert _is_in_quadrant_I(deg2rad(angle)) == result


@pytest.mark.parametrize(
    "angle, result",
    [
        (0.0, False),
        (45.0, False),
        (90.0, False),
        (90.1, True),
        (135.0, True),
        (180.0, True),
        (180.1, False),
        (225.0, False),
        (270.0, False),
        (270.1, False),
        (315.0, False),
        (360.0, False),
    ],
)
def test_is_in_quarant_II(angle: Angle, result: bool):
    assert _is_in_quadrant_II(deg2rad(angle)) == result


@pytest.mark.parametrize(
    "angle, result",
    [
        (0.0, False),
        (45.0, False),
        (90.0, False),
        (90.1, False),
        (135.0, False),
        (180.0, False),
        (180.1, True),
        (225.0, True),
        (270.0, True),
        (270.1, False),
        (315.0, False),
        (360.0, False),
    ],
)
def test_is_in_quarant_III(angle: Angle, result: bool):
    assert _is_in_quadrant_III(deg2rad(angle)) == result


@pytest.mark.parametrize(
    "angle, result",
    [
        (0.0, False),
        (45.0, False),
        (90.0, False),
        (90.1, False),
        (135.0, False),
        (180.0, False),
        (180.1, False),
        (225.0, False),
        (270.0, False),
        (270.1, True),
        (315.0, True),
        (360.0, True),
    ],
)
def test_is_in_quarant_IV_true(angle: Angle, result: bool):
    assert _is_in_quadrant_IV(deg2rad(angle)) == result


@pytest.mark.parametrize(
    "angle, result_angle",
    [
        (0.0, 0.0),
        (360.0, 360.0),
        (360.1, 0.1),
        (540.0, 180.0),
        (-0.1, 359.9),
        (-360.0, 0.0),
        (-540.0, 180.0),
    ],
)
def test_calc_angle_if_out_of_range(angle, result_angle):
    assert _calc_angle_if_out_of_rangle(deg2rad(angle)) == approx(
        deg2rad(result_angle)
    )

