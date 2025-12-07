from argparse import ArgumentParser, Namespace
from functools import lru_cache


class CliArgs(Namespace):
    file_path: str


def parse_input(path: str) -> list[list[str]]:
    lines = list[list[str]]()
    with open(path, "r") as file:
        for raw_line in file:
            line = raw_line.strip()
            lines.append([c for c in line])
    # Don't consider the last empty lines
    while len(lines[-1]) == 0:
        lines.pop()
    return lines


LINES: list[list[str]]


@lru_cache(maxsize=50)  # Magic sauce
def count_timelines(x: int, y: int) -> int:
    global LINES
    # End condition
    if y >= len(LINES) - 1:
        return 1
    # Ray continues
    if LINES[y + 1][x] == ".":
        return count_timelines(x, y + 1)
    # Ray encounters a splitter
    elif LINES[y + 1][x] == "^":
        return (
            count_timelines(x - 1, y + 1)  # -
            + count_timelines(x + 1, y + 1)
        )

    else:
        raise RuntimeError("That cannot happen")


def main() -> None:
    global LINES

    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    LINES = parse_input(path=args.file_path)
    assert len(LINES) > 1, "There must be at least 2 lines"

    start_x = [x for x, slot in enumerate(LINES[0]) if slot == "S"][0]
    timelines = count_timelines(x=start_x, y=0)
    print("Universes: %d" % timelines)


if __name__ == "__main__":
    main()
