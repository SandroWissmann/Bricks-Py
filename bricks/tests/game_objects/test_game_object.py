from bricks.source.game_objects.game_object import GameObject
from bricks.source.types.point import Point

import pytest


class DerrivedGameObject(GameObject):
    def __init__(self, top_left=Point(0.0, 0.0), width=0.0, height=0.0):
        GameObject.__init__(self, top_left, width, height)


class TestGameObject:
    def test_init_default(self):
        obj = DerrivedGameObject()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0

    def test_init(self):
        obj = DerrivedGameObject(Point(8.2, 1.3), 3.1, 4.2)

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2

    @pytest.mark.parametrize(
        "x, y, w, h",
        [(-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, -1, 0), (0, 0, 0, -1)],
    )
    def test_init_throws_ValueError(self, x, y, w, h):
        with pytest.raises(ValueError):
            DerrivedGameObject(top_left=Point(x, y), width=w, height=h)

    def test_top_left(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.top_left.x == 10.1
        assert obj.top_left.y == 20.2

        obj.top_left = Point(x=20.3, y=30.5)
        assert obj.top_left.x == 20.3
        assert obj.top_left.y == 30.5

    def test_bottom_right(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.bottom_right.x == 10.1 + obj.width
        assert obj.bottom_right.y == 20.2 + obj.height

    def test_bottom_left(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.bottom_left.x == 10.1
        assert obj.bottom_left.y == 20.2 + obj.height

    def test_top_right(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.top_right.x == 10.1 + obj.width
        assert obj.top_right.y == 20.2

    def test_width(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.width == 10.5

    def test_height(self):
        obj = DerrivedGameObject(
            top_left=Point(x=10.1, y=20.2), width=10.5, height=20.6
        )
        assert obj.height == 20.6
