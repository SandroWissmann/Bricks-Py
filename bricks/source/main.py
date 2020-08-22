from bricks.source.level import Level
from bricks.source.level import read_level_from_json_file


def main():
    level = read_level_from_json_file("../level/1.json")
    print(level)


if __name__ == "__main__":
    main()
