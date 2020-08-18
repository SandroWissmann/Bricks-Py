from bricks.source.game_objects.game_object import GameObject
from bricks.source.types.point import Point


class Wall(GameObject):
    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
    ):
        GameObject.__init__(self, top_left, width, height)
