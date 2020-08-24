from bricks.game_objects.ball import Ball
from bricks.types.point import Point
from bricks.types.angle import Angle

from numpy import deg2rad

from pytest import approx
import pytest


class TestBall:
    def test_init_default(self):
        obj = Ball()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0
        assert obj.velocity == 0.0
        assert obj.angle.value == 0.0
        assert obj.gravity == 0.0
        assert obj.is_active == False

    def test_init(self):
        obj = Ball(
            top_left=Point(8.2, 1.3),
            width=3.1,
            height=4.2,
            velocity=2.4,
            angle=Angle(deg2rad(90.0)),
            gravity=9.8,
        )

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
        assert obj.velocity == 2.4
        assert obj.angle.value == approx(deg2rad(90.0))
        assert obj.gravity == 9.8
        assert obj.is_active == False

    def test_angle(self):
        obj = Ball(
            top_left=Point(8.2, 1.3),
            width=3.1,
            height=4.2,
            velocity=2.4,
            angle=Angle(deg2rad(30.0)),
            gravity=9.8,
        )
        assert obj.angle.value == approx(deg2rad(30.0))

        obj.angle = Angle(deg2rad(65))
        assert obj.angle.value == approx(deg2rad(65.0))

    def test_gravity(self):
        obj = Ball(
            top_left=Point(8.2, 1.3),
            width=3.1,
            height=4.2,
            velocity=2.4,
            angle=Angle(deg2rad(30.0)),
            gravity=9.8,
        )
        assert obj.gravity == 9.8

        obj.gravity = 4.5
        assert obj.gravity == 4.5

    def test_is_active(self):
        obj = Ball()
        assert obj.is_active == False

        obj.is_active = True
        assert obj.is_active == True

    @pytest.mark.parametrize(
        "active, velocity, degree, gravity, end_point",
        [
            (False, 2.0, 0.0, 0.0, Point(0.0, 0.0),),  # not active
            (True, 0.0, 90.0, 2.0, Point(0.0, 2.0),),  # only gravity
            (True, 2.0, 0.0, 0.0, Point(2.0, 0.0),),  # 0 degrees
            (True, 2.0, 30.0, 0.0, Point(1.732050807568877, 1),),  # 30 degrees
            (  # 45 degrees
                True,
                2.0,
                45.0,
                0.0,
                Point(1.414213562373096, 1.414213562373096),
            ),
            (True, 2.0, 60.0, 0.0, Point(1, 1.732050807568877),),  # 60 degrees
            (True, 2.0, 90.0, 0.0, Point(0.0, 2.0),),  # 90 degrees
            (True, 2.0, 90.0, 2.0, Point(0.0, 4.0),),  # 90 degrees + gravity
            (  # 120 degrees
                True,
                2.0,
                120.0,
                0.0,
                Point(-1, 1.732050807568877),
            ),
            (  # 135 degrees
                True,
                2.0,
                135.0,
                0.0,
                Point(-1.41421356237, 1.414213562373096),
            ),
            (True, 2.0, 180.0, 0.0, Point(-2, 0),),  # 180 degrees
            (True, 2.0, 180.0, 0.0, Point(-2.0, 0),),  # 230 degrees
            (  # 230 degrees
                True,
                2.0,
                230.0,
                0.0,
                Point(-1.28557521937, -1.53208888624),
            ),
            (True, 2.0, 270.0, 0.0, Point(0.0, -2.0),),  # 270 degrees
            (True, 2.0, 270.0, 2.0, Point(0.0, 0.0),),  # 270 degrees + gravity
            (  # 315 degrees
                True,
                2.0,
                315.0,
                0.0,
                Point(1.414213562373096, -1.414213562373096),
            ),
        ],
    )
    def test_move(self, active, velocity, degree, gravity, end_point):
        obj = Ball(
            top_left=Point(0.0, 0.0),
            width=3.1,
            height=4.2,
            velocity=velocity,
            angle=Angle(deg2rad(degree)),
            gravity=gravity,
        )
        obj.is_active = active
        time_in_ms = 1000
        obj.move(time_in_ms)

        assert obj.top_left.x == approx(end_point.x)
        assert obj.top_left.y == approx(end_point.y)
