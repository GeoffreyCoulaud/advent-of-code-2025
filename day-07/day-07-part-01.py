from argparse import ArgumentParser, Namespace


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


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    lines = parse_input(path=args.file_path)
    assert len(lines) > 1, "There must be at least 2 lines"

    splits = 0
    for y in range(len(lines) - 1):
        line = lines[y]
        origins = {x for (x, slot) in enumerate(line) if slot in ("S", "|")}
        for ray_x in origins:
            next_line = lines[y + 1]

            # Ray continues
            if next_line[ray_x] == ".":
                next_line[ray_x] = "|"

            # Ray encounters another ray
            elif next_line[ray_x] == "|":
                continue

            # Ray encounters a splitter
            elif next_line[ray_x] == "^":
                splits += 1
                for new_ray_x in (ray_x - 1, ray_x + 1):
                    if new_ray_x not in range(len(next_line)):
                        continue
                    if next_line[new_ray_x] != ".":
                        continue
                    next_line[new_ray_x] = "|"

    for line in lines:
        print("".join(line))
    print("Splits: %d" % splits)


if __name__ == "__main__":
    main()
