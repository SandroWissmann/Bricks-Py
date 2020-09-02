"""Representation of the ball on the game board."""


from bricks.game_objects.moveable_game_objects import MoveableGameObject
from bricks.types.angle import Angle
from bricks.types.angle import Quadrant
from bricks.types.point import Point

from numpy import isclose
from numpy import sin
from numpy import cos

from numpy import deg2rad


class Ball(MoveableGameObject):
    """
    Representation of the Ball on the game board.

    Attributes
    ----------
    top_left: Point
        Top left coordinate of the ball.
    top_right: Point
        Top right coordinate of the ball.
    bottom_left: Point
        Bottom left coordinate of the ball.
    bottom_right: Point
        Bottom right coordinate of the ball.
    width: float
        Width of the ball.
    height: float
        Height of the ball.
    velocity: float
        Velocity of the ball.
    angle: Angle
        Direction of were the ball moves.
    gravity: float
        Gravity which acts on the ball.
    is_active: bool
        flag to pause the movement of the ball.

    Methods
    -------
    move(self, elapsed_time_in_ms: float):
        Calculates the movement of the ball. 

    """

    def __init__(
        self,
        top_left: Point = Point(0.0, 0.0),
        width: float = 0.0,
        height: float = 0.0,
        velocity: float = 0.0,
        angle: Angle = Angle(0.0),
        gravity: float = 0.0,
    ):
        MoveableGameObject.__init__(self, top_left, width, height, velocity)
        self._angle = angle
        self._gravity = gravity
        self._is_active = False

    @property
    def angle(self) -> Angle:
        return self._angle

    @angle.setter
    def angle(self, angle: Angle):
        self._angle = angle

    @property
    def gravity(self) -> float:
        return self._gravity

    @gravity.setter
    def gravity(self, gravity: float):
        self._gravity = gravity

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    def move(self, elapsed_time_in_ms: float):
        """
        Calculates were the ball moves in a timeframe.
        Considers velocity and gravity for calculation.
        """
        if not self._is_active:
            return

        new_pos = self.top_left

        if self.velocity != 0.0:
            new_pos = _calc_new_position(
                new_pos, self.velocity, self.angle, elapsed_time_in_ms
            )

        if self.gravity != 0.0:
            new_pos = _calc_new_position(
                new_pos, self.gravity, Angle(deg2rad(90.0)), elapsed_time_in_ms
            )

        self._top_left = new_pos


def _calc_new_position(
    point: Point, velocity: float, angle: Angle, elapsed_time_in_ms: float
) -> Point:
    traveld_way = _calc_traveld_way(elapsed_time_in_ms, velocity)
    delta = _calc_delta(angle, traveld_way)

    return Point(point.x + delta.x, point.y + delta.y)


def _calc_traveld_way(delta_time_ms: float, velocity_in_sec: float) -> float:
    return delta_time_ms / 1000.0 * velocity_in_sec


def _calc_delta(angle: Angle, side_c: float) -> Point:

    if isclose(side_c, 0.0):
        return Point(0.0, 0.0)

    side_a = sin(angle.quadrant_angle) * side_c
    side_b = cos(angle.quadrant_angle) * side_c

    if angle.quadrant == Quadrant.I:
        return Point(side_b, side_a)
    if angle.quadrant == Quadrant.II:
        return Point(-side_a, side_b)
    if angle.quadrant == Quadrant.III:
        return Point(-side_b, -side_a)
    if angle.quadrant == Quadrant.IV:
        return Point(side_a, -side_b)
    return Point(0.0, 0.0)
