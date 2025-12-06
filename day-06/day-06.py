from argparse import ArgumentParser, Namespace


class CliArgs(Namespace):
    file_path: str


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    with open(args.file_path, "r") as file:
        for raw_line in file:
            line = raw_line.strip()
            pass

    print()


if __name__ == "__main__":
    main()
