from bricks.source.game_objects.brick import Brick
from bricks.source.types.point import Point

import pytest


class TestBrick:
    def test_init_default(self):
        obj = Brick()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0
        assert obj.start_hitpoints == 1
        assert obj.hitpoints == 1

    def test_init(self):
        obj = Brick(
            top_left=Point(8.2, 1.3), width=3.1, height=4.2, hitpoints=5
        )

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
        assert obj.start_hitpoints == 5
        assert obj.hitpoints == 5

    @pytest.mark.parametrize("hitpoints", [(-1), (10)])
    def test_init_throws_ValueError(self, hitpoints):
        with pytest.raises(ValueError):
            Brick(
                top_left=Point(8.2, 1.3),
                width=3.1,
                height=4.2,
                hitpoints=hitpoints,
            )

    def test_start_hitpoints(self):
        obj = Brick(
            top_left=Point(8.2, 1.3), width=3.1, height=4.2, hitpoints=5
        )
        assert obj.start_hitpoints == 5

    def test_hitpoints(self):
        obj = Brick(
            top_left=Point(8.2, 1.3), width=3.1, height=4.2, hitpoints=5
        )
        assert obj.hitpoints == 5

    def test_decrease_hitpoints(self):
        obj = Brick(
            top_left=Point(8.2, 1.3), width=3.1, height=4.2, hitpoints=5
        )
        assert obj.start_hitpoints == 5
        assert obj.hitpoints == 5

        obj.decrease_hitpoints()
        assert obj.start_hitpoints == 5
        assert obj.hitpoints == 4

    def test_is_destroyed(self):
        obj = Brick(
            top_left=Point(8.2, 1.3), width=3.1, height=4.2, hitpoints=1
        )
        assert obj.is_destroyed() == False

        obj.decrease_hitpoints()
        assert obj.is_destroyed() == True
