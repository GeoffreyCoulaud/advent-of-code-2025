import operator
from argparse import ArgumentParser, Namespace
from functools import reduce

ComputationGrid = list[list[str]]


class CliArgs(Namespace):
    file_path: str


def column_to_int(column: list[str]) -> int:
    return int("".join(column).strip().replace(" ", "0"))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    # Read file as a grid of characters
    print("--- Reading file ---")
    columns = list[list[str]]()
    with open(args.file_path, "r") as file:
        for y, raw_line in enumerate(file):
            line = raw_line.replace("\n", " ")
            print("Line %d: %s" % (y, line))
            for cursor, slot in enumerate(line):
                if len(columns) <= cursor:
                    columns.append([])
                columns[cursor].append(slot)

    # Split grid where there are empty columns
    print("--- Splitting into computations ---")
    computations = list[ComputationGrid]()
    cursor = 0
    while cursor < len(columns):
        column = columns[cursor]
        print("Column: %s" % "".join(column))
        if all([slot == " " for slot in column]):
            print("Separator column found")
            computations.append(columns[0:cursor])
            columns = columns[cursor + 1 :]
            cursor = 0
        else:
            cursor += 1
    if len(columns) > 0:
        computations.append(columns)
    print("Found %d computations" % len(computations))

    # Perform each computation
    print("--- Performing computations ---")
    total = 0
    for i, computation in enumerate(computations):
        op = "".join([col[-1] for col in computation]).strip()
        operation = operator.add if op == "+" else operator.mul
        number_columns = [[slot for slot in col[:-1]] for col in computation]
        numbers = [column_to_int(col) for col in number_columns]
        print("Computation %d: %s" % (i, f" {op} ".join(str(n) for n in numbers)))
        result = reduce(operation, numbers)
        print("Result: %d" % result)
        total += result

    print("Total: %d" % total)


if __name__ == "__main__":
    main()
