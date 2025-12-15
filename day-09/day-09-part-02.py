from argparse import ArgumentParser, Namespace
from typing import NamedTuple


class CliArgs(Namespace):
    file_path: str


def minmax(*args: int) -> tuple[int, int]:
    return min(*args), max(*args)


class Vec2(NamedTuple):
    x: int
    y: int


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    # Get the positions of red squares, and deduct the grid size
    max_x, max_y = 0, 0
    red_positions = list[Vec2]()
    with open(args.file_path, "r") as file:
        for raw_line in file:
            coords = [int(c) for c in raw_line.strip().split(",")]
            x, y = coords[0], coords[1]
            red_positions.append(Vec2(x, y))
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

    # Populate the outline
    print("Populating outline")
    outline_positions = set[Vec2]()
    prev = red_positions[-1]
    for i, pos in enumerate(red_positions):
        print("Iteration %03d of %d" % (i + 1, len(red_positions)))
        # Red corners
        outline_positions.add(pos)
        # Horizontal green line
        if prev.y == pos.y:
            min_x, max_x = minmax(prev.x, pos.x)
            for x in range(min_x + 1, max_x):
                outline_positions.add(Vec2(x, pos.y))
        # Vertical green line
        else:
            min_y, max_y = minmax(prev.y, pos.y)
            for y in range(min_y + 1, max_y):
                outline_positions.add(Vec2(pos.x, y))

    # - Write the inside function using winding number algorithm
    # - Find the first inside neighbor along the outline
    # - Flood fill from that
    # - Compress outline / inside regions into rectangles

    print("Done")


if __name__ == "__main__":
    main()
