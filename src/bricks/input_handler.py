from bricks.level import Level
from bricks.game_objects.ball import Ball
from bricks.game_objects.platform import Platform
from bricks.game_objects.wall import Wall
from bricks.game_objects.physics import (
    _intersects_with_left_x,
    _intersects_with_right_x,
    _put_before_intersects_with_left_x,
    _put_before_intersects_with_right_x,
)

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
        self._update_input_event()
        self._handle_event(self._input_event, elapsed_time_in_ms, level)

    def _update_input_event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self._input_event = self._Event.quit
            if event.type == KEYUP:
                print("KEYUP")
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

        # pressed = pygame.key.get_pressed()
        # if pressed[K_LEFT]:
        #     return self._Event.left
        # if pressed[K_RIGHT]:
        #     return self._Event.left
        # if pressed[K_SPACE]:
        #     return self._Event.space
        # if pressed[K_ESCAPE]:
        #     return self._Event.space

        # while True:
        #     poll_event = pygame.event.poll()
        #     if poll_event == NOEVENT:
        #         print("NOEVENT")
        #         break
        #     if poll_event.type == QUIT:
        #         print("QUIT")
        #         return self._Event.quit
        #     if poll_event.type == KEYDOWN:
        #         print("KEYDOWN")
        #         if poll_event.key == K_p:
        #             print("P")
        #             return self._Event.p
        #         if poll_event.key == K_LEFT:
        #             print("K_LEFT")
        #             return self._Event.left
        #         if poll_event.key == K_RIGHT:
        #             print("K_RIGHT")
        #             return self._Event.right
        #         if poll_event.key == K_SPACE:
        #             print("K_SPACE")
        #             return self._Event.space
        #         if poll_event.key == K_ESCAPE:
        #             print("K_ESCAPE")
        #             return self._Event.escape

        # keys = pygame.key.get_pressed()
        # if keys[K_LEFT]:
        #     print("K_LEFT")
        #     return self._Event.left
        # if keys[K_RIGHT]:
        #     print("K_RIGHT")
        #     return self._Event.right
        # if keys[K_SPACE]:
        #     print("K_SPACE")
        #     return self._Event.space
        # if keys[K_ESCAPE]:
        #     print("K_ESCAPE")
        #     return self._Event.escape
        # return self._Event.none

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
