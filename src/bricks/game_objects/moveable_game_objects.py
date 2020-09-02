"""Bass class for all moveable objects on the game board."""
from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point


class MoveableGameObject(GameObject):
    """
    Bass class for all moveable objects on the game board.
    Abstract class only to be used with inheritance.    
    
    Attributes
    ----------
    top_left: Point
        Top left coordinate of the moveable game object.
    top_right: Point
        Top right coordinate of the moveable game object.
    bottom_left: Point
        Bottom left coordinate of the moveable game object.
    bottom_right: Point
        Bottom right coordinate of the moveable game object.
    width: float
        Width of the moveable game object.
    height: float
        Height of the moveable game object.
    velocity: float
        Movement speed of the moveable game object.
    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        velocity: float = 0.0,
    ):
        """
        Raises Exception on direct use as MoveableGameObject.
        """
        if type(self) is MoveableGameObject:
            raise Exception(
                "MoveableGameObject is an abstract class and cannot be "
                "instantiated directly"
            )
        GameObject.__init__(self, top_left, width, height)
        self._velocity = velocity

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: float):
        self._velocity = velocity

