from source.game_objects.game_object import GameObject
from source.game_objects.ball import Ball
from source.game_objects.platform import Platform
from source.game_objects.wall import Wall
from source.game_objects.brick import Brick
from source.game_objects.indestructible_brick import IndestructibleBrick
from source.difficulty_parameter import DifficultyParameter
from source.types.point import Point
from source.types.angle import Angle

import json
from numpy import deg2rad
from typing import List

WALL_THICKNESS = 1.0
PLATFORM_HEIGHT = 0.5
BALL_WIDTH = 0.75
BALL_HEIGHT = 0.75
BALL_ANGLE = deg2rad(135.0)


class Level:
    def __init__(
        self,
        difficulty_parameter: DifficultyParameter,
        grid_width: int,
        grid_height: int,
        bricks: List[Brick],
        indestructible_bricks: List[IndestructibleBrick],
    ):
        assert grid_width > 0
        assert grid_height > 0

        self._difficulty_parameter = difficulty_parameter
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._left_wall = _make_left_wall(grid_width, grid_height)
        self._right_wall = _make_right_wall(grid_width, grid_height)
        self._top_wall = _make_top_wall(grid_width)
        self.platform = _make_platform(
            difficulty_parameter.platform_width,
            difficulty_parameter.platform_velocity,
            grid_width,
            grid_height,
        )
        self.ball = _make_ball(
            difficulty_parameter.ball_velocity,
            difficulty_parameter.ball_gravity,
            grid_width,
            grid_height,
        )
        self.bricks = bricks
        self.indestructible_bricks = indestructible_bricks

        self._grid_width += 2 * WALL_THICKNESS
        self._grid_height += WALL_THICKNESS

        _transpose_coordinates_with_walls(self.platform)
        _transpose_coordinates_with_walls(self.ball)
        for brick in self.bricks:
            _transpose_coordinates_with_walls(brick)
        for indestructible_brick in self.indestructible_bricks:
            _transpose_coordinates_with_walls(indestructible_brick)

    @property
    def grid_width(self) -> int:
        return self._grid_width

    @property
    def grid_height(self) -> int:
        return self._grid_height

    @property
    def left_wall(self) -> Wall:
        return self._left_wall

    @property
    def right_wall(self) -> Wall:
        return self._right_wall

    @property
    def top_wall(self) -> Wall:
        return self._top_wall

    def difficulty_parameter(self, difficulty_parameter: DifficultyParameter):
        self._difficulty_parameter = difficulty_parameter
        self.reset_ball()
        self.reset_platform()

    def reset_ball(self):
        self.ball = _make_ball(
            self._difficulty_parameter.ball_velocity,
            self._difficulty_parameter.ball_gravity,
            self._grid_width,
            self._grid_height,
        )

    def reset_platform(self):
        self.platform = _make_platform(
            self._difficulty_parameter.platform_width,
            self._difficulty_parameter.platform_velocity,
            self._grid_width,
            self._grid_height,
        )


def read_level_from_json_file(filename: str) -> Level:
    try:
        with open(filename) as file:
            try:
                data = json.load(file)

                grid_width: int = data["width"]
                grid_height: int = data["height"]

                bricks: List[Brick] = []
                if "bricks" in data:
                    for brick_data in data["bricks"]:
                        x: float = brick_data["top_left_x"]
                        y: float = brick_data["top_left_y"]
                        w: float = brick_data["width"]
                        h: float = brick_data["height"]
                        hp: int = brick_data["hitpoints"]
                        brick = Brick(
                            top_left=Point(x, y),
                            width=w,
                            height=h,
                            hitpoints=hp,
                        )
                        bricks.append(brick)

                ind_bricks: List[IndestructibleBrick] = []
                if "indestructible_bricks" in data:
                    for ind_brick_data in data["indestructible_bricks"]:
                        x: float = ind_brick_data["top_left_x"]
                        y: float = ind_brick_data["top_left_y"]
                        w: float = ind_brick_data["width"]
                        h: float = ind_brick_data["height"]
                        hp: int = ind_brick_data["hitpoints"]
                        ind_brick = IndestructibleBrick(
                            top_left=Point(x, y), width=w, height=h
                        )
                        ind_bricks.append(ind_brick)

                return Level(
                    difficulty_parameter=DifficultyParameter(),
                    grid_width=grid_width,
                    grid_height=grid_height,
                    bricks=bricks,
                    indestructible_bricks=ind_bricks,
                )

            except ValueError as error:
                print("File is not valid JSON (%s)" % error)
    except IOError as error:
        print("Couldn't open level file (%s)" % error)


def _make_left_wall(grid_width: int, grid_height: int) -> Wall:
    return Wall(
        top_left=Point(x=0.0, y=0.0),
        width=WALL_THICKNESS,
        height=grid_width + WALL_THICKNESS,
    )


def _make_right_wall(grid_width: int, grid_height: int) -> Wall:
    return Wall(
        top_left=Point(x=grid_width + WALL_THICKNESS, y=0.0),
        width=WALL_THICKNESS,
        height=grid_width + WALL_THICKNESS,
    )


def _make_top_wall(grid_width: int) -> Wall:
    return Wall(
        top_left=Point(x=WALL_THICKNESS, y=0.0),
        width=grid_width,
        height=WALL_THICKNESS,
    )


def _make_platform(
    width: float, velocity: float, grid_width: int, grid_height: int
) -> Platform:
    point = _platform_init_position(
        platform_width=width, grid_width=grid_width, grid_height=grid_height
    )

    return Platform(
        top_left=point, width=width, height=PLATFORM_HEIGHT, velocity=velocity
    )


def _make_ball(
    velocity: float, gravity: float, grid_width: int, grid_height: int
) -> Ball:
    point = _ball_init_position(grid_width=grid_width, grid_height=grid_height)

    return Ball(
        top_left=point,
        width=BALL_WIDTH,
        height=BALL_HEIGHT,
        velocity=velocity,
        angle=Angle(BALL_ANGLE),
        gravity=gravity,
    )


def _transpose_coordinates_with_walls(obj: GameObject):
    obj.top_left.x += WALL_THICKNESS
    obj.top_left.y += WALL_THICKNESS


def _platform_init_position(
    platform_width: float, grid_width: int, grid_height: int
):
    return Point(
        x=grid_width / 2.0 - platform_width / 2.0, y=grid_height - 1.0
    )


def _ball_init_position(grid_width: int, grid_height: int) -> Point:
    return Point(x=grid_width / 2.0, y=grid_height / 2.0)
