"""Bass class for all objects on the game board."""
from bricks.types.point import Point


class GameObject:
    """
    Bass class for all objects on the game board.
    Abstract class only to be used with inheritance.
    
    Attributes
    ----------
    top_left: Point
        Top left coordinate of the game object.
    top_right: Point
        Top right coordinate of the game object.
    bottom_left: Point
        Bottom left coordinate of the game object.
    bottom_right: Point
        Bottom right coordinate of the game object.
    width: float
        Width of the game object.
    height: float
        Height of the game object.
    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
    ):
        """
        Raises ValueError if height, width or top left contain negative values.
        Raises Exception on direct use as GameObject.
        """
        if type(self) is GameObject:
            raise Exception(
                "GameObject is an abstract class and cannot be instantiated "
                "directly"
            )
        self._top_left = _check_args_point(top_left)
        self._witdh = _check_args_width(width)
        self._height = _check_args_height(height)

    @property
    def top_left(self) -> Point:
        return self._top_left

    @top_left.setter
    def top_left(self, top_left: Point):
        self._top_left = top_left

    @property
    def bottom_right(self) -> Point:
        return Point(
            self._top_left.x + self._witdh, self._top_left.y + self._height
        )

    @property
    def bottom_left(self) -> Point:
        return Point(self._top_left.x, self._top_left.y + self._height)

    @property
    def top_right(self) -> Point:
        return Point(self._top_left.x + self._witdh, self._top_left.y)

    @property
    def width(self) -> float:
        return self._witdh

    @property
    def height(self) -> float:
        return self._height


def _check_args_point(point: Point) -> Point:
    if point.x < 0.0 or point.y < 0.0:
        raise ValueError(
            "game_object.def _check_args_point(point):\n"
            "Point must be >= 0\n"
            "Point x: %s\n"
            "Point y: %s\n" % (point.x, point.y)
        )
    return point


def _check_args_width(width: float) -> float:
    if width < 0.0:
        raise ValueError(
            "game_object.def _check_args_width(point):\n"
            "Width must be >= 0\n"
            "Width: %s\n" % (width)
        )
    return width


def _check_args_height(height: float) -> float:
    if height < 0.0:
        raise ValueError(
            "game_object.def _check_args_height(point):\n"
            "Height must be >= 0\n"
            "Height: %s\n" % (height)
        )
    return height
