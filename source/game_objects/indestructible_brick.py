from source.game_objects.game_object import GameObject
from source.types.point import Point


class IndestructibleBrick(GameObject):
    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
    ):
        GameObject.__init__(self, top_left, width, height)

