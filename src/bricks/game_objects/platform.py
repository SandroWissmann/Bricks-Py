"""Representation of the platform on the game board."""
from bricks.game_objects.moveable_game_objects import MoveableGameObject
from bricks.types.point import Point


class Platform(MoveableGameObject):
    """
    Representation of the platform on the game board.
    
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
    velocity: float
        Velocity of the platform.

    Methods
    -------
    move(self, elapsed_time_in_ms: float):
        Calculates the movement to the right and left of the platform. 
    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        velocity: float = 0.0,
    ):
        MoveableGameObject.__init__(self, top_left, width, height, velocity)

    def move(self, elapsed_time_in_ms: float):
        """
        Calculates the movement to the right and left of the platform.
        When velocity is positive -> Movement to the right.
        When velocity is negative -> Movement to the left.
        """
        if self.velocity == 0.0:
            return

        delta_x = elapsed_time_in_ms / 1000.0 * self.velocity
        self.top_left.x = self.top_left.x + delta_x

