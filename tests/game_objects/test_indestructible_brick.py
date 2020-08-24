from bricks.game_objects.indestructible_brick import IndestructibleBrick
from bricks.types.point import Point


class TestIndestructibleBrick:
    def test_init_default(self):
        obj = IndestructibleBrick()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0

    def test_init(self):
        obj = IndestructibleBrick(Point(8.2, 1.3), 3.1, 4.2)

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
