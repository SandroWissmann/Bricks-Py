class DifficultyParameter:
    def __init__(
        self,
        platform_velocity: float = 16.0,
        platform_width: float = 4.0,
        ball_velocity: float = 16.0,
        ball_gravity: float = 1.5,
    ):
        self.platform_velocity = platform_velocity
        self.platform_width = platform_width
        self.ball_velocity = ball_velocity
        self.ball_gravity = ball_gravity
