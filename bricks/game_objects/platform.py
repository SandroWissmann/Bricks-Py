from source.game_objects.moveable_game_objects import MoveableGameObject
from source.types.point import Point


class Platform(MoveableGameObject):
    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        velocity: float = 0.0,
    ):
        MoveableGameObject.__init__(self, top_left, width, height, velocity)

    def move(self, elapsed_time_in_ms: float):
        if self.velocity == 0.0:
            return

        delta_x = elapsed_time_in_ms / 1000.0 * self.velocity
        self.top_left.x = self.top_left.x + delta_x

