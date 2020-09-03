"""Module to render level on the screen."""
from bricks.game_objects.ball import Ball
from bricks.game_objects.brick import Brick
from bricks.game_objects.game_object import GameObject
from bricks.game_objects.indestructible_brick import IndestructibleBrick
from bricks.game_objects.platform import Platform
from bricks.game_objects.wall import Wall
from bricks.types.rgb_color import RGBColor
from bricks.level import Level

import pygame

BLACK = (0, 0, 0)


class Renderer:
    """
    Class to render level on the screen.
    Only one instance of the class should be used at the same time.

    Attributes
    ----------
    is_paused: bool
        Indicates if game is in state pause.
    window_title: str
        Defines what is shown on the window title screen.

    Mehods
    ------
    render(self, level: Level):
        Renders the level on the screen. 
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        grid_width: int,
        grid_height: int,
    ):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._width_factor = screen_width / grid_width
        self._height_factor = screen_height / grid_height

        self._screen = pygame.display.set_mode((screen_width, screen_height))
        self._screen.fill(BLACK)
        self._is_paused = False
        self._window_title = ""

        pygame.display.flip()

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @is_paused.setter
    def is_paused(self, is_paused: bool):
        self._is_paused = is_paused

    @property
    def window_title(self) -> str:
        return self._window_title

    @window_title.setter
    def window_title(self, window_title: str):
        self._window_title = window_title
        pygame.display.set_caption(window_title)

    def render(self, level: Level):
        """
        Renders the level on the screen. 
        Changes color of level to grayscale if paused active.
        """
        self._clear_screen()
        self._render_ball(level.ball)
        self._render_platform(level.platform)
        self._render_wall(level.left_wall)
        self._render_wall(level.right_wall)
        self._render_wall(level.top_wall)

        for brick in level.bricks:
            self._render_brick(brick)
        for indestructible_brick in level.indestructible_bricks:
            self._render_indestructible_brick(indestructible_brick)
        self._update_screen()

    def _clear_screen(self):
        white = RGBColor(0x1E, 0x1E, 0x1E)
        if not self._is_paused:
            self._screen.fill(white.as_tuple())
        else:
            self._screen.fill(white.grayscale().as_tuple())

    def _update_screen(self):
        pygame.display.update()

    def _render_ball(self, ball: Ball):
        light_blue = RGBColor(0xCC, 0xFF, 0xFF)
        self._render_game_object(ball, light_blue)

    def _render_platform(self, platform: Platform):
        gray = RGBColor(0xBF, 0xBF, 0xBF)
        self._render_game_object(platform, gray)

    def _render_wall(self, wall: Wall):
        brown = RGBColor(0xBF, 0x80, 0x40)
        self._render_game_object(wall, brown)

    def _render_brick(self, brick: Brick):
        if brick.is_destroyed():
            return
        color = _get_brick_draw_color(brick)
        self._render_game_object(brick, color)

    def _render_indestructible_brick(
        self, indestructibleBrick: IndestructibleBrick
    ):
        red = RGBColor(0xFF, 0x00, 0x00)
        self._render_game_object(indestructibleBrick, red)

    def _render_game_object(self, obj: GameObject, color: RGBColor):
        if self.is_paused:
            color = color.grayscale()
        rect = self._to_pygame_rect(obj)
        pygame.draw.rect(self._screen, color.as_tuple(), rect)
        self._draw_highlights(rect, color)

    def _draw_highlights(self, rect: pygame.Rect, color: RGBColor):
        x = rect.x
        y = rect.y
        w = rect.width
        h = rect.height

        draw_color = color.lighter().as_tuple()
        pygame.draw.line(self._screen, draw_color, (x, y + h), (x, y))
        pygame.draw.line(self._screen, draw_color, (x + 1, y + h), (x + 1, y))
        pygame.draw.line(self._screen, draw_color, (x, y), (x + w, y))
        pygame.draw.line(self._screen, draw_color, (x, y + 1), (x + w, y + 1))

        draw_color = color.darker().as_tuple()
        pygame.draw.line(self._screen, draw_color, (x, y + h), (x + w, y + h))
        pygame.draw.line(
            self._screen, draw_color, (x, y + h - 1), (x + w, y + h - 1)
        )
        pygame.draw.line(self._screen, draw_color, (x + w, y + h), (x + w, y))
        pygame.draw.line(
            self._screen, draw_color, (x + w - 1, y + h), (x + w - 1, y)
        )

    def _to_pygame_rect(self, obj: GameObject) -> pygame.Rect:
        return pygame.Rect(
            obj.top_left.x * self._width_factor,
            obj.top_left.y * self._height_factor,
            obj.width * self._width_factor,
            obj.height * self._height_factor,
        )


def _get_brick_draw_color(brick: Brick) -> RGBColor:
    assert 0 <= brick.hitpoints <= 9

    colors = (
        RGBColor(0xFD, 0xEF, 0x42),
        RGBColor(0x99, 0xFF, 0x00),
        RGBColor(0x00, 0x7E, 0x56),
        RGBColor(0x00, 0x5A, 0x7E),
        RGBColor(0x46, 0x3A, 0xCB),
        RGBColor(0xF4, 0x0B, 0xEC),
        RGBColor(0xA4, 0x4E, 0xFE),
        RGBColor(0xFF, 0x7B, 0x00),
        RGBColor(0xF4, 0x46, 0x11),
    )
    return colors[brick.hitpoints - 1]

