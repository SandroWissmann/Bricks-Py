from bricks.game_objects.ball import Ball
from bricks.game_objects.brick import Brick
from bricks.game_objects.platform import Platform
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point
from bricks.types.angle import Angle, Quadrant

from bricks.game_objects.physics import reflect_from_game_objects
from bricks.game_objects.physics import _calc_angle_factor
from bricks.game_objects.physics import _clamp_angle

from pytest import approx
from numpy import deg2rad
import pytest


class TestPhysics:
    @pytest.mark.parametrize(
        "ball_top_left, ball_angle, ball_result_top_left, ball_result_angle",
        [
            (Point(1.0, 0.0), 30.0, Point(0.0, 0.0), 150.0,),
            (Point(1.0, 3.0), 30.0, Point(0.0, 3.0), 150.0,),
            (Point(1.0, 6.0), 30.0, Point(0.0, 6.0), 150.0,),
            (Point(1.0, 8.0), 30.0, Point(0.0, 8.0), 150.0,),
            (Point(1.0, 11.0), 30.0, Point(0.0, 11.0), 150.0,),
            (Point(1.0, 0.0), 330.0, Point(0.0, 0.0), 210.0,),
            (Point(1.0, 3.0), 330.0, Point(0.0, 3.0), 210.0,),
            (Point(1.0, 6.0), 330.0, Point(0.0, 6.0), 210.0,),
            (Point(1.0, 8.0), 330.0, Point(0.0, 8.0), 210.0,),
            (Point(1.0, 11.0), 330.0, Point(0.0, 11.0), 210.0,),
            (Point(6.0, 0.0), 150.0, Point(7.0, 0.0), 30.0,),
            (Point(6.0, 3.0), 150.0, Point(7.0, 3.0), 30.0,),
            (Point(6.0, 6.0), 150.0, Point(7.0, 6.0), 30.0,),
            (Point(6.0, 8.0), 150.0, Point(7.0, 8.0), 30.0,),
            (Point(6.0, 11.0), 150.0, Point(7.0, 11.0), 30.0,),
            (Point(6.0, 0.0), 210.0, Point(7.0, 0.0), 330.0,),
            (Point(6.0, 3.0), 210.0, Point(7.0, 3.0), 330.0,),
            (Point(6.0, 6.0), 210.0, Point(7.0, 6.0), 330.0,),
            (Point(6.0, 8.0), 210.0, Point(7.0, 8.0), 330.0,),
            (Point(6.0, 11.0), 210.0, Point(7.0, 11.0), 330.0,),
        ],
    )
    def test_reflect_horizontal(
        self,
        ball_top_left: Point,
        ball_angle: float,
        ball_result_top_left: Point,
        ball_result_angle: float,
    ):
        ball = Ball(
            top_left=ball_top_left,
            width=3.0,
            height=3.0,
            velocity=1.0,
            angle=Angle(deg2rad(ball_angle)),
        )

        bricks = [
            Brick(top_left=Point(3.0, 1.0), width=4.0, height=4.0),
            Brick(top_left=Point(3.0, 5.0), width=4.0, height=4.0),
            Brick(top_left=Point(3.0, 9.0), width=4.0, height=4.0),
        ]

        result = reflect_from_game_objects(ball, bricks)

        assert result == True
        assert ball.top_left.x == ball_result_top_left.x
        assert ball.top_left.y == ball_result_top_left.y
        assert ball.angle.value == approx(deg2rad(ball_result_angle))

    @pytest.mark.parametrize(
        "ball_top_left, ball_angle, ball_result_top_left, ball_result_angle",
        [
            (Point(0.0, 1.0), 30.0, Point(0.0, 0.0), 330.0,),
            (Point(3.0, 1.0), 30.0, Point(3.0, 0.0), 330.0,),
            (Point(6.0, 1.0), 30.0, Point(6.0, 0.0), 330.0,),
            (Point(8.0, 1.0), 30.0, Point(8.0, 0.0), 330.0,),
            (Point(11.0, 1.0), 30.0, Point(11.0, 0.0), 330.0,),
            (Point(0.0, 1.0), 150.0, Point(0.0, 0.0), 210.0,),
            (Point(3.0, 1.0), 150.0, Point(3.0, 0.0), 210.0,),
            (Point(6.0, 1.0), 150.0, Point(6.0, 0.0), 210.0,),
            (Point(8.0, 1.0), 150.0, Point(8.0, 0.0), 210.0,),
            (Point(11.0, 1.0), 150.0, Point(11.0, 0.0), 210.0,),
            (Point(0.0, 6.0), 330.0, Point(0.0, 7.0), 30.0,),
            (Point(3.0, 6.0), 330.0, Point(3.0, 7.0), 30.0,),
            (Point(6.0, 6.0), 330.0, Point(6.0, 7.0), 30.0,),
            (Point(8.0, 6.0), 330.0, Point(8.0, 7.0), 30.0,),
            (Point(11.0, 6.0), 330.0, Point(11.0, 7.0), 30.0,),
            (Point(0.0, 6.0), 210.0, Point(0.0, 7.0), 150.0,),
            (Point(3.0, 6.0), 210.0, Point(3.0, 7.0), 150.0,),
            (Point(6.0, 6.0), 210.0, Point(6.0, 7.0), 150.0,),
            (Point(8.0, 6.0), 210.0, Point(8.0, 7.0), 150.0,),
            (Point(11.0, 6.0), 210.0, Point(11.0, 7.0), 150.0,),
        ],
    )
    def test_reflect_vertical(
        self,
        ball_top_left: Point,
        ball_angle: float,
        ball_result_top_left: Point,
        ball_result_angle: float,
    ):
        ball = Ball(
            top_left=ball_top_left,
            width=3.0,
            height=3.0,
            velocity=1.0,
            angle=Angle(deg2rad(ball_angle)),
        )

        bricks = [
            Brick(top_left=Point(1.0, 3.0), width=4.0, height=4.0),
            Brick(top_left=Point(5.0, 3.0), width=4.0, height=4.0),
            Brick(top_left=Point(9.0, 3.0), width=4.0, height=4.0),
        ]

        result = reflect_from_game_objects(ball, bricks)

        assert result == True
        assert ball.top_left.x == ball_result_top_left.x
        assert ball.top_left.y == ball_result_top_left.y
        assert ball.angle.value == approx(deg2rad(ball_result_angle))

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
