from bricks.game_objects.game_object import GameObject
from bricks.types.point import Point


class MoveableGameObject(GameObject):
    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        velocity: float = 0.0,
    ):
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

