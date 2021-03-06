"""Module to handle key and events from user input."""
from bricks.level import Level
from bricks.game_objects.ball import Ball
from bricks.game_objects.platform import Platform
from bricks.game_objects.wall import Wall

from enum import Enum

import pygame
from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    K_p,
    NOEVENT,
    QUIT,
    KEYDOWN,
    KEYUP,
)


class InputHandler:
    """
    Class to get input from user and handle it.
    
    Attributes
    ----------
    is_paused: bool
        Indicates if game is paused.
    changed_pause_state: bool
        Indicates if game changed its pause state in last cycle.
    is_quit: bool
        Indicates if quit game was requested
    
    Methods
    -------
    handle_input(self, level: Level, elapsed_time_in_ms: float)
        Checks for events / pressed keys.
        Handle pressed keys.


    """

    class _Event(Enum):
        none = 0
        quit = 1
        left = 2
        right = 3
        space = 4
        escape = 5
        p = 6

    def __init__(self):
        self._is_paused = False
        self._changed_pause_state = False
        self._is_quit = False
        self._input_event = self._Event.none

    @property
    def is_paused(self):
        return self._is_paused

    @property
    def changed_pause_state(self):
        return self._changed_pause_state

    @property
    def is_quit(self):
        return self._is_quit

    def handle_input(self, level: Level, elapsed_time_in_ms: float):
        """
        Checks for events / pressed keys:
            quit - Quit was requested. e.g. from closing the window.
            left - Indicate left as long as it is hold down.
            right - Indicate right as long as it is hold down.
            space - Space was pressed.
            escape - Escape was pressed.
            p - Key p was pressed.

        Handles the events / pressed keys:
            quit - Set state quit.
            left - Move platform to the left, except it reached left wall.
            right - Move platform to the right, except it reached right wall.
            space - Set ball active.
            escape - Set state quit.
            p - Set/reset state pause.
        """
        self._update_input_event()
        self._handle_event(self._input_event, elapsed_time_in_ms, level)

    def _update_input_event(self):
        if self._input_event == self._Event.p:
            self._input_event = self._Event.none
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self._input_event = self._Event.quit
            if event.type == KEYUP:
                self._input_event = self._Event.none
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self._input_event = self._Event.space
                if event.key == K_ESCAPE:
                    self._input_event = self._Event.escape
                if event.key == K_LEFT:
                    self._input_event = self._Event.left
                if event.key == K_RIGHT:
                    self._input_event = self._Event.right
                if event.key == K_p:
                    self._input_event = self._Event.p

    def _handle_event(
        self, event: _Event, elapsed_time_in_ms: float, level: Level
    ):
        self._handle_event_from_level_objects(
            event,
            elapsed_time_in_ms,
            level.left_wall,
            level.right_wall,
            level.ball,
            level.platform,
        )

    def _handle_event_from_level_objects(
        self,
        event: _Event,
        elapsed_time_in_ms: float,
        left_wall: Wall,
        right_wall: Wall,
        ball: Ball,
        platform: Platform,
    ):
        if event == self._Event.p:
            self._is_paused = not self._is_paused
            self._changed_pause_state = True
            return
        self._changed_pause_state = False

        if event == self._Event.quit or event == self._Event.escape:
            self._is_quit = True
            return
        if event == self._Event.p:
            self._is_paused = not self._is_paused
            return

        if self._is_paused:
            return

        if event == self._Event.space:
            if not ball.is_active:
                ball.is_active = True
        elif event == self._Event.left:
            if _intersects_with_left_x(platform, left_wall):
                _put_before_intersects_with_left_x(platform, left_wall)
            else:
                _move_left(platform, elapsed_time_in_ms)
        elif event == self._Event.right:
            if _intersects_with_right_x(platform, right_wall):
                _put_before_intersects_with_right_x(platform, right_wall)
            else:
                _move_right(platform, elapsed_time_in_ms)


def _move_left(platform: Platform, elapsed_time_in_ms: float):
    if platform.velocity > 0:
        platform.velocity *= -1
    platform.move(elapsed_time_in_ms)


def _move_right(platform: Platform, elapsed_time_in_ms: float):
    if platform.velocity < 0:
        platform.velocity *= -1
    platform.move(elapsed_time_in_ms)


def _intersects_with_right_x(platform: Platform, wall: Wall) -> bool:
    return (
        platform.bottom_right.x >= wall.top_left.x
        and platform.top_left.x < wall.top_left.x
    )


def _intersects_with_left_x(platform: Platform, wall: Wall) -> bool:
    return (
        platform.top_left.x <= wall.bottom_right.x
        and platform.bottom_right.x > wall.bottom_right.x
    )


def _put_before_intersects_with_right_x(platform: Platform, wall: Wall):
    platform.top_left.x = wall.top_left.x - platform.width


def _put_before_intersects_with_left_x(platform: Platform, wall: Wall):
    platform.top_left.x = wall.bottom_right.x
