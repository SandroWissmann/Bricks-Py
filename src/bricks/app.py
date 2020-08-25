from bricks.level import Level
from bricks.level import read_level_from_json_file
from bricks.renderer import Renderer
import pygame


def main():
    level = read_level_from_json_file("level/1.json")
    # print(level)

    # background_color = (255, 255, 255)
    # (width, height) = (300, 200)
    # screen = pygame.display.set_mode((width, height))
    # pygame.display.set_caption("Tutorial 1")
    # screen.fill(background_color)
    # pygame.display.flip()

    # BLUE = (0, 0, 255)
    # pygame.draw.rect(screen, BLUE, (200, 150, 100, 50))

    renderer = Renderer(780, 540, 28, 19)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        renderer.render(level)
        # renderer.update_screen()


if __name__ == "__main__":
    main()
