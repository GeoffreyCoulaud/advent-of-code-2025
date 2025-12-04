from argparse import ArgumentParser, Namespace
from typing import Generator


class CliArgs(Namespace):
    file_path: str


def iter_grid(grid: list[str]) -> Generator[tuple[int, int, str], None, None]:
    for y, line in enumerate(grid):
        for x, slot in enumerate(line):
            yield (x, y, slot)


def iter_offsets() -> Generator[tuple[int, int], None, None]:
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if y == 0 and x == 0:
                continue
            yield (x, y)


def count_adjacent_rolls(grid: list[str], x_center: int, y_center: int) -> int:
    counter = 0
    for x_offset, y_offset in iter_offsets():
        x = x_center + x_offset
        y = y_center + y_offset
        if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
            continue
        neighbor = grid[y][x]
        if neighbor == "@":
            counter += 1
    return counter


def find_accessible_coords(grid: list[str]) -> set[tuple[int, int]]:
    acessible_coords = set[tuple[int, int]]()
    for x, y, slot in iter_grid(grid):
        if slot != "@":
            continue
        adjacent_rolls = count_adjacent_rolls(grid, x, y)
        if adjacent_rolls < 4:
            acessible_coords.add((x, y))
    return acessible_coords


def remove_rolls(grid: list[str], removed: set[tuple[int, int]]) -> list[str]:
    new_grid = []
    for y, line in enumerate(grid):
        new_line = ""
        for x, slot in enumerate(line):
            if (x, y) in removed:
                new_line += "."
            else:
                new_line += slot
        new_grid.append(new_line)
    return new_grid


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    with open(args.file_path, "r") as file:
        grid = file.readlines()
    grid = [line.strip() for line in grid]

    i = 0
    new_grid = [*grid]
    total_accessible = 0

    # do-while
    accessible_coords = find_accessible_coords(new_grid)
    total_accessible += len(accessible_coords)
    print("[%d] Removing %d rolls" % (i, len(accessible_coords)))
    new_grid = remove_rolls(new_grid, accessible_coords)
    i += 1
    while len(accessible_coords) > 0:
        accessible_coords = find_accessible_coords(new_grid)
        total_accessible += len(accessible_coords)
        print("Removing %d rolls" % len(accessible_coords))
        new_grid = remove_rolls(new_grid, accessible_coords)
        i += 1

    print("Final accessible: %d" % len(accessible_coords))
    print("Total removed: %d" % total_accessible)


if __name__ == "__main__":
    main()
