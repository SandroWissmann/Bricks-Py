from bricks.source.game_objects.platform import Platform
from bricks.source.types.point import Point

from pytest import approx
import pytest


class TestPlatform:
    def test_init_default(self):
        obj = Platform()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0
        assert obj.velocity == 0.0

    def test_init(self):
        obj = Platform(Point(8.2, 1.3), 3.1, 4.2, 1.2)

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
        assert obj.velocity == 1.2

    @pytest.mark.parametrize("velocity, end_x", [(-2.0, -2.0), (2.0, 2.0)])
    def test_move(self, velocity, end_x):
        obj = Platform(
            top_left=Point(0, 0), width=3.1, height=4.2, velocity=velocity
        )
        time_in_ms = 1000
        obj.move(time_in_ms)

        assert obj.top_left.x == approx(end_x)
        assert obj.top_left.y == obj.top_left.y
