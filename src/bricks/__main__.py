from source.level import Level
from source.level import read_level_from_json_file

import pygame


def main():
    # level = read_level_from_json_file("level/1.json")
    # print(level)
    (width, height) = (300, 200)
    screen = pygame.display.set_mode((width, height))
    while True:
        pygame.display.flip()


if __name__ == "__main__":
    main()
