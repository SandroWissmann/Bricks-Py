"""Module to represent the main game logic."""

from bricks.game_objects.ball import Ball
from bricks.game_objects.brick import Brick
from bricks.game_objects.game_object import GameObject
from bricks.game_objects.indestructible_brick import IndestructibleBrick
from bricks.game_objects.physics import reflect_from_game_objects
from bricks.game_objects.physics import reflect_from_platform
from bricks.game_objects.platform import Platform
from bricks.game_objects.wall import Wall

from bricks.audio_device import AudioDevice
from bricks.audio_device import play_destroy_brick
from bricks.audio_device import play_hit_brick
from bricks.audio_device import play_hit_platform
from bricks.audio_device import play_game_over
from bricks.audio_device import play_next_level
from bricks.audio_device import play_lost_ball
from bricks.audio_device import play_extra_life
from bricks.audio_device import play_win_game

from bricks.level import Level, read_level_from_json_file
from bricks.audio_device import (
    AudioDevice,
    play_destroy_brick,
    play_extra_life,
    play_game_over,
    play_hit_brick,
    play_hit_platform,
    play_lost_ball,
    play_next_level,
    play_win_game,
)
from bricks.renderer import Renderer
from bricks.input_handler import InputHandler
from bricks.difficulty_parameters import DifficultyParameters

from typing import List
from time import sleep

import json
import pathlib
from time import time

FRAMES_PER_SECOND = 60
MS_PER_FRAME = 1000 / FRAMES_PER_SECOND

POINTS_PER_BRICK_HITPOINTS = 100
POINTS_FOR_EXTRA_LIVE = 10000

HIGHSCORE_FILENAME = "highscore.dat"

BALL_VELOCITY_INCREASE = 2.0
BALL_GRAVITY_INCREASE = 0.5
PLATFORM_VELOCITY_INCREASE = 2.0
PLATFORM_WIDTH_DECREASE = 0.5

BALL_VELOCITY_MAX = 30.0
BALL_GRAVITY_MAX = 5.0
PLATFORM_VELOCITY_MAX = 28.0
PLATFORM_WIDTH_MIN = 2.0

START_LIFES = 5


class Game:
    """
    Class to represent the main game logic.

    On construction current highscore is loaded from file.
    On construction the first level is loaded from file.

    Methods
    -------
    run(self):
        Method starts the game with the first level.
        Runs until the user quits the game.
    """

    def __init__(self, screen_width: int, screen_height: int):
        self._audio_device = AudioDevice()
        self._input_handler = InputHandler()
        self._level_filenames = _get_level_filenames_from_folder("level")
        self._level = _load_level(self._level_filenames, 1)
        self._difficulty_parameters = DifficultyParameters()
        self._renderer = Renderer(
            screen_width=screen_width,
            screen_height=screen_height,
            grid_width=self._level.grid_width,
            grid_height=self._level.grid_height,
        )
        self._highscore = _load_highscore()
        self._score = 0
        self._last_extra_life_divisor = 0
        self._current_level_idx = 1
        self._lifes = START_LIFES
        self._is_game_over = False
        self._update_values_in_title_bar()

    def _update_values_in_title_bar(self):
        self._renderer.window_title = _make_title(
            self._current_level_idx, self._lifes, self._score, self._highscore,
        )

    def run(self):
        """
        Method starts the game with the first level.
        
        Runs current level until it is beaten or game over occurs.
        If all levels are beaten starts on the first level with increased
        difficulty.

        Handles input from user.
        Checks if bricks get destroyed.
        Awards score for destroyed bricks.
        Renders the game on each iteration.
        Plays appropiated sounds for game situations(e.g. Brick destroyed)
        """
        while True:
            self._run_level()
            if self._input_handler.is_quit:
                return
            if self._is_game_over:
                play_game_over(self._audio_device)
                if self._score > self._highscore:
                    self._highscore = self._score
                    _save_highscore(self._highscore)
                self._current_level_idx = 1
                self._lifes = START_LIFES
                self._is_game_over = False
                self._score = 0
                self._difficulty_parameters = DifficultyParameters()
            elif self._all_levels_finished():
                play_win_game(self._audio_device)
                self._current_level_idx = 1
                self._difficulty_parameters = _increase_difficulty(
                    self._difficulty_parameters
                )
            else:
                play_next_level(self._audio_device)
                self._current_level_idx += 1
            self._level = _load_level(
                self._level_filenames, self._current_level_idx
            )
            self._level.difficulty_parameters = self._difficulty_parameters
            self._update_values_in_title_bar()

    def _run_level(self):
        while True:
            timepoint1 = time()

            self._renderer.render(self._level)

            self._input_handler.handle_input(self._level, MS_PER_FRAME)
            if self._input_handler.changed_pause_state:
                self._renderer.is_paused = self._input_handler.is_paused
            if self._input_handler.is_quit:
                return
            if self._input_handler.is_paused:
                continue

            if self._level.ball.is_active:
                self._level.ball.move(MS_PER_FRAME)

                if self._ball_is_lost():
                    self._lifes -= 1
                    if self._lifes <= 0:
                        self._is_game_over = True
                        return
                    play_lost_ball(self._audio_device)

                    self._update_values_in_title_bar()
                    self._level.reset_ball()
                    self._level.reset_platform()

                self._handle_ball_collisions()
                if _all_bricks_are_destroyed(self._level.bricks):
                    break

            timepoint2 = time()
            diff_in_ms = (timepoint2 - timepoint1) * 1000

            _delay_to_framerate(diff_in_ms)

    def _all_levels_finished(self) -> bool:
        return self._current_level_idx >= len(self._level_filenames)

    def _ball_is_lost(self) -> bool:
        return self._level.ball.bottom_right.y >= self._level.grid_height

    def _handle_ball_collisions(self):
        hit_objects = reflect_from_game_objects(
            ball=self._level.ball,
            game_objects=[self._level.left_wall]
            + [self._level.right_wall]
            + [self._level.top_wall]
            + self._level.bricks
            + self._level.indestructible_bricks,
        )

        for hit_object in hit_objects:
            if not isinstance(hit_object, Brick):
                continue
            if hit_object.is_destroyed():
                play_destroy_brick(self._audio_device)
                self._score += self._get_brick_score(hit_object)
                self._award_extra_life_it_threshold_reached()
                self._update_values_in_title_bar()
            else:
                play_hit_brick(self._audio_device)

        if reflect_from_platform(self._level.ball, self._level.platform):
            play_hit_platform(self._audio_device)

    def _get_brick_score(self, brick: Brick) -> int:
        return (
            POINTS_PER_BRICK_HITPOINTS
            * brick.start_hitpoints
            * self._current_level_idx
        )

    def _award_extra_life_it_threshold_reached(self):
        extra_life_divisor = int(self._score / POINTS_FOR_EXTRA_LIVE)
        if extra_life_divisor != self._last_extra_life_divisor:
            play_extra_life(self._audio_device)
            self._lifes += 1
            self._last_extra_life_divisor = extra_life_divisor


def _increase_difficulty(
    difficulty_paramters: DifficultyParameters,
) -> DifficultyParameters:

    dp = difficulty_paramters

    dp.platform_velocity = _clamp(
        dp.platform_velocity,
        dp.platform_velocity + PLATFORM_VELOCITY_INCREASE,
        PLATFORM_VELOCITY_MAX,
    )
    dp.platform_width = _clamp(
        PLATFORM_WIDTH_MIN,
        dp.platform_width - PLATFORM_WIDTH_DECREASE,
        dp.platform_width,
    )
    dp.ball_velocity = _clamp(
        dp.ball_velocity,
        dp.ball_velocity + BALL_VELOCITY_INCREASE,
        BALL_VELOCITY_MAX,
    )
    dp.ball_gravity = _clamp(
        dp.ball_gravity,
        dp.ball_gravity + BALL_GRAVITY_INCREASE,
        BALL_GRAVITY_MAX,
    )
    return dp


def _load_highscore() -> int:
    try:
        with open(HIGHSCORE_FILENAME) as file:
            try:
                data = json.load(file)
                return data["highscore"]
            except ValueError as error:
                print("File has no highscore JSON entry (%s)" % error)
                return 0
    except IOError as error:
        return 0


def _save_highscore(highscore: int):
    try:
        with open(HIGHSCORE_FILENAME, "w") as file:
            json.dump({"highscore": highscore}, file)
    except IOError as error:
        print("Couldn't open highscore file (%s)" % error)


def _make_title(level: int, lifes: int, score: int, highscore: int) -> str:
    return "Level: %s     Lifes: %s     Score: %s     Highscore: %s" % (
        level,
        lifes,
        score,
        highscore,
    )


def _all_bricks_are_destroyed(bricks: List[Brick]) -> bool:
    return all(brick.is_destroyed() for brick in bricks)


def _delay_to_framerate(elapsed_time_in_ms: float):
    if elapsed_time_in_ms < MS_PER_FRAME:
        sleep((MS_PER_FRAME - elapsed_time_in_ms) / 1000)


def _load_level(level_filenames: List[str], level_idx: int) -> Level:
    assert len(level_filenames) > 0

    return read_level_from_json_file(level_filenames[level_idx - 1])


def _get_level_filenames_from_folder(folder_name: str) -> List[str]:
    filenames: List[str] = []
    for filepath in pathlib.Path(folder_name).glob("**/*.json"):
        filenames.append(str(filepath.absolute()))
    return sorted(filenames)


def _clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
