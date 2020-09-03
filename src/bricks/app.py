#!/usr/bin/env python3
"""Main function to run the game."""
from bricks.game import Game

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 540


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()


if __name__ == "__main__":
    main()
