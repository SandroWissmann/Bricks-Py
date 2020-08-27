from bricks.game import Game

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 540


def main():
    SCREEN_WIDTH = 780
    SCREEN_HEIGHT = 540

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()


if __name__ == "__main__":
    try:
        main()
    finally:
        quit()
