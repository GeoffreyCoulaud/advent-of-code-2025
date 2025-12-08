from argparse import ArgumentParser, Namespace
from functools import reduce
from operator import mul
from typing import NamedTuple, cast


class CliArgs(Namespace):
    file_path: str
    connections: int
    count_to_multiply: int


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def d2(self, other: "Vec3") -> float:
        return sum((ca - cb) ** 2 for ca, cb in zip(self, other))


def find_circuit(a: int, circuits: list[set[int]]) -> int:
    for i, c in enumerate(circuits):
        if a in c:
            return i
    raise RuntimeError("Cannot happen")


def in_same_circuit(a: int, b: int, circuits: list[set[int]]) -> bool:
    ca = find_circuit(a, circuits)
    if ca is None:
        return False
    cb = find_circuit(b, circuits)
    if cb is None:
        return False
    return ca == cb


def closest_junction_boxes(
    positions: list[Vec3], circuits: list[set[int]]
) -> tuple[int, int]:
    smallest_d2: float = float("+inf")
    smallest_pair: tuple[int, int]
    for i, first in enumerate(positions):
        for j, second in enumerate(positions[i + 1 :]):
            if in_same_circuit(i, j, circuits):
                continue
            d2 = first.d2(second)
            if d2 < smallest_d2:
                smallest_pair = (i, j)
    return smallest_pair


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("connections", type=int)
    parser.add_argument("count_to_multiply", type=int, default=3)
    args = parser.parse_args(namespace=CliArgs())

    with open(args.file_path, "r") as file:
        positions = [
            Vec3(*[int(coord) for coord in line.split(",")])
            for line in file.read().strip().splitlines()
        ]
    circuits = [set([i]) for i in range(len(positions))]

    # Connect the N closest pairs
    for i in range(args.connections):
        print("Iteration %d" % i)

        a, b = closest_junction_boxes(positions, circuits)

        # Identify circuits
        cai = find_circuit(a, circuits)
        cbi = find_circuit(b, circuits)

        # Merge
        circuits[cai] = circuits[cai] | circuits[cbi]
        circuits.pop(cbi)

    sorted_circuits = sorted(circuits, key=lambda c: len(c), reverse=True)
    biggest = sorted_circuits[: args.count_to_multiply]
    print("Biggest:", ", ".join(str(b) for b in biggest))
    result = reduce(mul, (len(c) for c in biggest))
    print("Result: %d" % result)


if __name__ == "__main__":
    main()
