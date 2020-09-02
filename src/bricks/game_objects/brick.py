"""Representation of a brick on the game board."""
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point


class Brick(GameObject):
    """
    Representation of a brick on the game board.

    Attributes
    ----------
    top_left: Point
        Top left coordinate of the brick.
    top_right: Point
        Top right coordinate of the brick.
    bottom_left: Point
        Bottom left coordinate of the brick.
    bottom_right: Point
        Bottom right coordinate of the brick.
    width: float
        Width of the brick.
    height: float
        Height of the brick.
    hitpoints: int
        Actual hitpoints of the brick.
    start_hitpoints: int
        Hitpoints the brick has on creation

    Methods
    -------
    is_destroyed(self) -> bool:
        Indicates if brick is destroyed.

    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        hitpoints: int = 1,
    ):
        """
        Raises ValueError if hitpoints not in range between 1 and 9.
        """
        GameObject.__init__(self, top_left, width, height)
        self._start_hitpoints = _check_args_hitpoints(hitpoints)
        self._hitpoints = self._start_hitpoints

    @property
    def start_hitpoints(self) -> int:
        return self._start_hitpoints

    @property
    def hitpoints(self) -> int:
        return self._hitpoints

    def decrease_hitpoints(self):
        if self._hitpoints > 0:
            self._hitpoints -= 1

    def is_destroyed(self) -> bool:
        """Indicates if brick is destroyed. True if no hitpoints left"""
        return self._hitpoints == 0


def _check_args_hitpoints(hitpoints: int) -> int:
    if hitpoints < 1 or hitpoints > 9:
        raise ValueError(
            "brick.def _check_args_hitpoints(hitpoints):\n"
            "hitpoints must be >= 0 and < 10\n"
            "hitpoints: %s\n" % (hitpoints)
        )
    return hitpoints
