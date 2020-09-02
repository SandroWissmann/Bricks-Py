"""Representation of an indestructible brick on the game board."""
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point


class IndestructibleBrick(GameObject):
    """
    Representation of an indestructible brick on the game board.
    
    Attributes
    ----------
    top_left: Point
        Top left coordinate of the indestructible brick.
    top_right: Point
        Top right coordinate of the indestructible brick.
    bottom_left: Point
        Bottom left coordinate of the indestructible brick.
    bottom_right: Point
        Bottom right coordinate of the indestructible brick.
    width: float
        Width of the indestructible brick.
    height: float
        Height of the indestructible brick.
    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
    ):
        GameObject.__init__(self, top_left, width, height)

