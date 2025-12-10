from argparse import ArgumentParser, Namespace
from collections.abc import MutableSequence, Sequence
from functools import lru_cache
from typing import NamedTuple


class CliArgs(Namespace):
    file_path: str


def minmax(*args: int) -> tuple[int, int]:
    return min(*args), max(*args)


class Vec2(NamedTuple):
    x: int
    y: int


@lru_cache(10)
def count_crossings(pos: Vec2, outline: frozenset[Vec2]) -> int:
    """
    Raycast towards the left, from x,y counting the number of line intersections.
    Starting on a line guarantees a crossing.
    """
    current = 1 if pos in outline else 0
    if pos.x == 0:
        return current
    else:
        return current + count_crossings(Vec2(pos.x - 1, pos.y), outline)


WHITE = 0
RED = 1
GREEN = 2


def get_slot(
    x: int,
    y: int,
    data: Sequence[int],
    stride: int,
) -> int:
    return data[x + y * stride]


def put_slot(
    value: int,
    x: int,
    y: int,
    data: MutableSequence[int],
    stride: int,
) -> None:
    data[x + y * stride] = value


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
    frozen_outline_positions = frozenset(outline_positions)
    del outline_positions

    # Populate the inside
    print("Populating inside")
    inside_positions = set[Vec2]()
    width = max_x + 1
    height = max_y + 1
    for y in range(height):
        print("Line %03d of %dx%d grid" % (y, width, height))
        for x in range(width):
            # Ignore already colored slots
            pos = Vec2(x, y)
            if pos in frozen_outline_positions:
                continue
            # Count line crossings for coord.
            # Even = outside, odd = inside
            if count_crossings(pos, frozen_outline_positions) % 2 != 0:
                inside_positions.add(pos)

    # TODO - Parallelize this bad boy, lines are independent

    print("Done")


if __name__ == "__main__":
    main()
