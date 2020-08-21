class DifficultyParameter:
    def __init__(
        self,
        platform_velocity: float,
        platform_width: float,
        ball_velocity: float,
        ball_gravity: float,
    ):
        self.platform_velocity = platform_velocity
        self.platform_width = platform_width
        self.ball_velocity = ball_velocity
        self.ball_gravity = ball_gravity
