from source.game_objects.game_object import GameObject
from source.types.point import Point


class Brick(GameObject):
    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        hitpoints: int = 1,
    ):
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
        if self.hitpoints > 0:
            self._hitpoints -= 1

    def is_destroyed(self) -> bool:
        return self.hitpoints == 0


def _check_args_hitpoints(hitpoints: int) -> int:
    if hitpoints < 1 or hitpoints > 9:
        raise ValueError(
            "brick.def _check_args_hitpoints(hitpoints):\n"
            "hitpoints must be >= 0 and < 10\n"
            "hitpoints: %s\n" % (hitpoints)
        )
    return hitpoints
