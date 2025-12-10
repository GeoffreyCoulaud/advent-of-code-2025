from argparse import ArgumentParser, Namespace


class CliArgs(Namespace):
    file_path: str


def minmax(*args: int) -> tuple[int, int]:
    return min(*args), max(*args)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    positions = list[tuple[int, int]]()
    with open(args.file_path, "r") as file:
        for raw_line in file:
            coords = [int(c) for c in raw_line.strip().split(",")]
            positions.append((coords[0], coords[1]))

    biggest_rectangle_area = 0
    for i in range(len(positions) - 1):
        for j in range(i + 1, len(positions)):
            a, b = positions[i], positions[j]
            x_min, x_max = minmax(a[0], b[0])
            y_min, y_max = minmax(a[1], b[1])
            width = x_max - x_min + 1
            height = y_max - y_min + 1
            area = width * height
            if area > biggest_rectangle_area:
                print("New max: %02d,%02d and %02d,%02d -> %d" % (*a, *b, area))
                print("Width: %d, height: %d" % (width, height))
                biggest_rectangle_area = area

    print(biggest_rectangle_area)


if __name__ == "__main__":
    main()
