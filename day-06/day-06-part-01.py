import operator
import re
from argparse import ArgumentParser, Namespace
from functools import reduce
from typing import cast


class CliArgs(Namespace):
    file_path: str


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    columns = list[list[int]]()
    with open(args.file_path, "r") as file:
        for y, raw_line in enumerate(file):
            print("Line %d: %s" % (y, raw_line.rstrip()))
            line = re.sub(r"\s+", " ", raw_line.strip()).split(" ")
            for x, slot in enumerate(line):
                if len(columns) <= x:
                    columns.append([])
                if slot.isdigit():
                    columns[x].append(int(slot))
                else:
                    op = operator.add if slot == "+" else operator.mul
                    acc = cast(int, reduce(op, columns[x]))
                    print("Column %d, %s : %d" % (x, slot, acc))
                    columns[x] = [acc]
    print("Total:", sum(column[0] for column in columns))


if __name__ == "__main__":
    main()
