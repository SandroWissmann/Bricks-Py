"""Representation of a wall on the game board."""
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point


class Wall(GameObject):
    """
    Representation of a wall on the game board.
    
    Attributes
    ----------
    top_left: Point
        Top left coordinate of the platform.
    top_right: Point
        Top right coordinate of the platform.
    bottom_left: Point
        Bottom left coordinate of the platform.
    bottom_right: Point
        Bottom right coordinate of the platform.
    width: float
        Width of the platform.
    height: float
        Height of the platform.
    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
    ):
        GameObject.__init__(self, top_left, width, height)
