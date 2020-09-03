"""Storage of Parameters which can be increased to increase difficulty."""


class DifficultyParameters:
    """
    Class to store variable parameters for increasing difficulty.
    
    Attributes
    ----------
    platform_velocity: float
        Velocity of the platform.
    platform_width: float
        Width of the platform.
    ball_velocity: float
        Velocity of the ball.
    bottom_right: Point
        Gravity of the ball.
    """

    def __init__(
        self,
        platform_velocity: float = 16.0,
        platform_width: float = 4.0,
        ball_velocity: float = 16.0,
        ball_gravity: float = 1.5,
    ):
        self._platform_velocity = platform_velocity
        self._platform_width = platform_width
        self._ball_velocity = ball_velocity
        self._ball_gravity = ball_gravity

    @property
    def platform_velocity(self) -> float:
        return self._platform_velocity

    @platform_velocity.setter
    def platform_velocity(self, platform_velocity: float):
        self._platform_velocity = platform_velocity

    @property
    def platform_width(self) -> float:
        return self._platform_width

    @platform_width.setter
    def platform_width(self, platform_width: float):
        self._platform_width = platform_width

    @property
    def ball_velocity(self) -> float:
        return self._platform_velocity

    @ball_velocity.setter
    def ball_velocity(self, ball_velocity: float):
        self._ball_velocity = ball_velocity

    @property
    def ball_gravity(self) -> float:
        return self._ball_gravity

    @ball_gravity.setter
    def ball_gravity(self, ball_gravity: float):
        self._ball_gravity = ball_gravity
