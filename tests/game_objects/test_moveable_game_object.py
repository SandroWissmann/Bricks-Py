from Bricks_py.source.game_objects.moveable_game_objects import (
    MoveableGameObject,
)
from Bricks_py.source.types.point import Point

import pytest


class DerrivedGameObject(MoveableGameObject):
    def __init__(
        self, top_left=Point(0.0, 0.0), width=0.0, height=0.0, velocity=0.0
    ):
        MoveableGameObject.__init__(self, top_left, width, height, velocity)


class TestMoveableGameObject:
    def test_init_default(self):
        obj = DerrivedGameObject()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0
        assert obj.velocity == 0.0

    def test_init(self):
        obj = DerrivedGameObject(Point(8.2, 1.3), 3.1, 4.2, 1.2)

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
        assert obj.velocity == 1.2

    def test_velocity(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2),
            width=10.5,
            height=20.6,
            velocity=1.2,
        )
        assert obj.velocity == 1.2

        obj.velocity = 3.5
        assert obj.velocity == 3.5
