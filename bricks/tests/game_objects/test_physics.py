from bricks.source.game_objects.ball import Ball
from bricks.source.game_objects.brick import Brick
from bricks.source.game_objects.platform import Platform
from bricks.source.game_objects.game_object import GameObject
from bricks.source.types.point import Point
from bricks.source.types.angle import Angle, Quadrant

from bricks.source.game_objects.physics import _calc_angle_factor
from bricks.source.game_objects.physics import _clamp_angle
from bricks.source.game_objects.physics import _intersects_with_right_x
from bricks.source.game_objects.physics import _intersects_with_left_x
from bricks.source.game_objects.physics import _intersects_with_bottom_y
from bricks.source.game_objects.physics import _intersects_with_top_y
from bricks.source.game_objects.physics import _is_inside_with_x
from bricks.source.game_objects.physics import _is_inside_with_y
from bricks.source.game_objects.physics import _not_through_with_right_x
from bricks.source.game_objects.physics import _not_through_with_left_x
from bricks.source.game_objects.physics import _not_through_with_top_y
from bricks.source.game_objects.physics import _not_through_with_bottom_y
from bricks.source.game_objects.physics import (
    _put_before_intersects_with_right_x,
)
from bricks.source.game_objects.physics import (
    _put_before_intersects_with_left_x,
)
from bricks.source.game_objects.physics import (
    _put_before_intersects_with_top_y,
)
from bricks.source.game_objects.physics import (
    _put_before_intersects_with_bottom_y,
)

from pytest import approx
from numpy import deg2rad
import pytest


class TestPhysics:
    @pytest.mark.parametrize(
        "x_ball, expected_result",
        [
            (0.0, 1.0),
            (0.25, 0.75),
            (0.5, 0.5),
            (1.0, 0.0),
            (1.5, 0.5),
            (1.75, 0.75),
            (2.0, 1.0),
        ],
    )
    def test_calc_angle_factor(self, x_ball: float, expected_result: float):
        assert _calc_angle_factor(
            x_ball=x_ball, x_left=0.0, x_center=1.0, x_right=2.0,
        ) == approx(expected_result)

    @pytest.mark.parametrize(
        "input_angle, output_angle",
        [
            (0.0, 30.0),
            (5.0, 30.0),
            (10.0, 30.0),
            (15.0, 30.0),
            (20.0, 30.0),
            (25.0, 30.0),
            (30.0, 30.0),
            (35.0, 35.0),
            (40.0, 40.0),
            (45.0, 45.0),
            (50.0, 50.0),
            (55.0, 55.0),
            (60.0, 60.0),
            (65.0, 65.0),
            (70.0, 70.0),
            (75.0, 75.0),
            (80.0, 75.0),
            (85.0, 75.0),
            (90.0, 105.0),
            (95.0, 105.0),
            (100.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (105.0, 105.0),
            (110.0, 110.0),
            (115.0, 115.0),
            (120.0, 120.0),
            (125.0, 125.0),
            (130.0, 130.0),
            (135.0, 135.0),
            (140.0, 140.0),
            (145.0, 145.0),
            (150.0, 150.0),
            (155.0, 150.0),
            (160.0, 150.0),
            (165.0, 150.0),
            (170.0, 150.0),
            (175.0, 150.0),
            (180.0, 210.0),
            (185.0, 210.0),
            (190.0, 210.0),
            (195.0, 210.0),
            (200.0, 210.0),
            (205.0, 210.0),
            (210.0, 210.0),
            (215.0, 215.0),
            (220.0, 220.0),
            (225.0, 225.0),
            (230.0, 230.0),
            (235.0, 235.0),
            (240.0, 240.0),
            (245.0, 245.0),
            (250.0, 250.0),
            (255.0, 255.0),
            (260.0, 255.0),
            (265.0, 255.0),
            (270.0, 285.0),
            (275.0, 285.0),
            (280.0, 285.0),
            (285.0, 285.0),
            (290.0, 290.0),
            (295.0, 295.0),
            (300.0, 300.0),
            (305.0, 305.0),
            (310.0, 310.0),
            (315.0, 315.0),
            (320.0, 320.0),
            (325.0, 325.0),
            (330.0, 330.0),
            (335.0, 330.0),
            (340.0, 330.0),
            (345.0, 330.0),
            (350.0, 330.0),
            (355.0, 330.0),
            (360.0, 360.0),
        ],
    )
    def test_clamp_angle(self, input_angle: float, output_angle: float):
        angle = Angle(deg2rad(input_angle))
        output = _clamp_angle(angle)
        assert output.value == approx(deg2rad(output_angle))

    # fixtures for following test to check how the ball reacts to collisions
    # from all sides
    @pytest.fixture
    def collison_brick_top_left(self):
        return Brick(top_left=Point(0.0, 0.0), width=2.0, height=2.0)

    @pytest.fixture
    def collison_brick_top(self):
        return Brick(top_left=Point(0.0, 0.0), width=5.0, height=2.0)

    @pytest.fixture
    def collison_brick_top_right(self):
        return Brick(top_left=Point(3.0, 0.0), width=2.0, height=2.0)

    @pytest.fixture
    def collison_brick_right(self):
        return Brick(top_left=Point(3.0, 0.0), width=2.0, height=5.0)

    @pytest.fixture
    def collison_brick_bottom_right(self):
        return Brick(top_left=Point(3.0, 3.0), width=2.0, height=2.0)

    @pytest.fixture
    def collison_brick_bottom(self):
        return Brick(top_left=Point(0.0, 3.0), width=5.0, height=2.0)

    @pytest.fixture
    def collison_brick_bottom_left(self):
        return Brick(top_left=Point(0.0, 3.0), width=2.0, height=2.0)

    @pytest.fixture
    def collison_brick_left(self):
        return Brick(top_left=Point(0.0, 0.0), width=2.0, height=5.0)

    @pytest.fixture
    def collison_ball(self):
        return Ball(
            top_left=Point(1.0, 1.0),
            width=3.0,
            height=3.0,
            velocity=10.0,
            angle=Angle(deg2rad(0.0)),
            gravity=0.0,
        )

    @pytest.fixture
    def collision_fixtures(
        self,
        collison_ball,
        collison_brick_top_left,
        collison_brick_top,
        collison_brick_top_right,
        collison_brick_right,
        collison_brick_bottom_right,
        collison_brick_bottom,
        collison_brick_bottom_left,
        collison_brick_left,
    ):
        return {
            "collison_ball": collison_ball,
            "collison_brick_top_left": collison_brick_top_left,
            "collison_brick_top": collison_brick_top,
            "collison_brick_top_right": collison_brick_top_right,
            "collison_brick_right": collison_brick_right,
            "collison_brick_bottom_right": collison_brick_bottom_right,
            "collison_brick_bottom": collison_brick_bottom,
            "collison_brick_bottom_left": collison_brick_bottom_left,
            "collison_brick_left": collison_brick_left,
        }

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", False),
            ("collison_brick_top_right", True),
            ("collison_brick_right", True),
            ("collison_brick_bottom_right", True),
            ("collison_brick_bottom", False),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", False),
        ],
    )
    def test_intersects_with_right_x(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _intersects_with_right_x(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", True),
            ("collison_brick_top", False),
            ("collison_brick_top_right", False),
            ("collison_brick_right", False),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", False),
            ("collison_brick_bottom_left", True),
            ("collison_brick_left", True),
        ],
    )
    def test_intersects_with_left_x(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _intersects_with_left_x(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", False),
            ("collison_brick_top_right", False),
            ("collison_brick_right", False),
            ("collison_brick_bottom_right", True),
            ("collison_brick_bottom", True),
            ("collison_brick_bottom_left", True),
            ("collison_brick_left", False),
        ],
    )
    def test_intersects_with_bottom_y(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _intersects_with_bottom_y(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", True),
            ("collison_brick_top", True),
            ("collison_brick_top_right", True),
            ("collison_brick_right", False),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", False),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", False),
        ],
    )
    def test_intersects_with_top_y(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _intersects_with_top_y(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", True),
            ("collison_brick_top_right", False),
            ("collison_brick_right", False),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", True),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", False),
        ],
    )
    def test_is_inside_with_x(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _is_inside_with_x(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", False),
            ("collison_brick_top_right", False),
            ("collison_brick_right", True),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", False),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", True),
        ],
    )
    def test_is_inside_with_y(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _is_inside_with_y(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", True),
            ("collison_brick_top_right", True),
            ("collison_brick_right", True),
            ("collison_brick_bottom_right", True),
            ("collison_brick_bottom", True),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", False),
        ],
    )
    def test_not_through_with_right_x(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _not_through_with_right_x(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", True),
            ("collison_brick_top", True),
            ("collison_brick_top_right", False),
            ("collison_brick_right", False),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", True),
            ("collison_brick_bottom_left", True),
            ("collison_brick_left", True),
        ],
    )
    def test_not_through_with_left_x(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _not_through_with_left_x(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", True),
            ("collison_brick_top", True),
            ("collison_brick_top_right", True),
            ("collison_brick_right", True),
            ("collison_brick_bottom_right", False),
            ("collison_brick_bottom", False),
            ("collison_brick_bottom_left", False),
            ("collison_brick_left", True),
        ],
    )
    def test_not_through_with_top_y(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _not_through_with_top_y(ball, brick) == expected_result

    @pytest.mark.parametrize(
        "brickname, expected_result",
        [
            ("collison_brick_top_left", False),
            ("collison_brick_top", False),
            ("collison_brick_top_right", False),
            ("collison_brick_right", True),
            ("collison_brick_bottom_right", True),
            ("collison_brick_bottom", True),
            ("collison_brick_bottom_left", True),
            ("collison_brick_left", True),
        ],
    )
    def test_not_through_with_bottom_y(
        self, collision_fixtures, brickname: str, expected_result: bool
    ):
        brick = collision_fixtures[brickname]
        ball = collision_fixtures["collison_ball"]
        assert _not_through_with_bottom_y(ball, brick) == expected_result

    def test_put_before_intersects_with_right_x(self, collision_fixtures):
        ball = collision_fixtures["collison_ball"]
        brick_right = collision_fixtures["collison_brick_right"]

        assert ball.bottom_right.x != brick_right.top_left.x
        _put_before_intersects_with_right_x(ball, brick_right)
        assert ball.bottom_right.x == brick_right.top_left.x

    def test_put_before_intersects_with_left_x(self, collision_fixtures):
        ball = collision_fixtures["collison_ball"]
        brick_left = collision_fixtures["collison_brick_left"]

        assert ball.top_left.x != brick_left.bottom_right.x
        _put_before_intersects_with_left_x(ball, brick_left)
        assert ball.bottom_left.x == brick_left.bottom_right.x

    def test_put_before_intersects_with_bottom_y(self, collision_fixtures):
        ball = collision_fixtures["collison_ball"]
        brick_bottom = collision_fixtures["collison_brick_bottom"]

        assert ball.bottom_right.y != brick_bottom.top_left.y
        _put_before_intersects_with_bottom_y(ball, brick_bottom)
        assert ball.bottom_right.y == brick_bottom.top_left.y

    def test_put_before_intersects_with_top_y(self, collision_fixtures):
        ball = collision_fixtures["collison_ball"]
        brick_top = collision_fixtures["collison_brick_top"]

        assert ball.top_left.y != brick_top.bottom_right.y
        _put_before_intersects_with_top_y(ball, brick_top)
        assert ball.top_left.y == brick_top.bottom_right.y

