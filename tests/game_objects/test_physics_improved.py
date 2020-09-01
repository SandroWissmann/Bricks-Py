from bricks.game_objects.ball import Ball
from bricks.game_objects.brick import Brick
from bricks.game_objects.platform import Platform
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point
from bricks.types.angle import Angle, Quadrant

from bricks.game_objects.physics_improved import reflect

from pytest import approx
from numpy import deg2rad
import pytest


class TestPhysicsImproved:
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

        result = reflect(ball, bricks)

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

        result = reflect(ball, bricks)

        assert result == True
        assert ball.top_left.x == ball_result_top_left.x
        assert ball.top_left.y == ball_result_top_left.y
        assert ball.angle.value == approx(deg2rad(ball_result_angle))
