from bricks.source.game_objects.wall import Wall
from bricks.source.types.point import Point


class TestWall:
    def test_init_default(self):
        obj = Wall()

        assert obj.top_left.x == 0.0
        assert obj.top_left.y == 0.0
        assert obj.width == 0.0
        assert obj.height == 0.0

    def test_init(self):
        obj = Wall(Point(8.2, 1.3), 3.1, 4.2)

        assert obj.top_left.x == 8.2
        assert obj.top_left.y == 1.3
        assert obj.width == 3.1
        assert obj.height == 4.2
