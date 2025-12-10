import logging
from argparse import ArgumentParser, Namespace
from collections import Counter
from functools import reduce
from operator import mul
from typing import NamedTuple


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

    def __str__(self):
        return ",".join(["%03d" % c for c in self])


def find_circuit_index(junction_box_index: int, circuits: list[set[int]]) -> int:
    for circuit_index, circuit in enumerate(circuits):
        if junction_box_index in circuit:
            return circuit_index
    raise RuntimeError("Cannot happen")


def in_same_circuit(a: int, b: int, circuits: list[set[int]]) -> bool:
    cai = find_circuit_index(a, circuits)
    cbi = find_circuit_index(b, circuits)
    return cai == cbi


def closest_junction_boxes(
    positions: list[Vec3], circuits: list[set[int]]
) -> tuple[int, int]:
    assert len(circuits) > 1, "There must be at least 2 circuits"

    smallest_d2: float = float("+inf")
    smallest_pair: tuple[int, int]
    for i, first in enumerate(positions):
        for j in range(i + 1, len(positions)):
            second = positions[j]
            if in_same_circuit(i, j, circuits):
                logging.debug("%s <---> %s : Skipped", str(first), str(second))
                continue
            d2 = first.d2(second)
            if d2 < smallest_d2:
                logging.debug(
                    "%s <---> %s : New smallest %f", str(first), str(second), d2
                )
                smallest_d2 = d2
                smallest_pair = (i, j)
    return smallest_pair


def main() -> None:
    logging.basicConfig(level="INFO")

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
        logging.debug("Iteration %02d", i)

        ai, bi = closest_junction_boxes(positions, circuits)
        a = positions[ai]
        b = positions[bi]

        # Identify circuits
        cai = find_circuit_index(ai, circuits)
        ca = circuits[cai]
        cbi = find_circuit_index(bi, circuits)
        cb = circuits[cbi]

        # fmt: off
        logging.info(
            "Iteration %02d: Connecting "
            + "%s %02d (circuit %02d size %02d) + "
            + "%s %02d (circuit %02d size %02d)",
            i, 
            str(a), ai, cai, len(ca),
            str(b), bi, cbi, len(cb)
        )
        # fmt: on

        # Merge
        circuits[cai] = ca | cb
        circuits.pop(cbi)

        circuits_per_size = Counter(len(c) for c in circuits)
        logging.debug("Circuit sizes : %s", str(circuits_per_size))

    logging.info("Ended with %d circuits", len(circuits))
    sorted_circuits = sorted(circuits, key=lambda c: len(c), reverse=True)
    biggest = sorted_circuits[: args.count_to_multiply]
    logging.info("Biggest: %s", ", ".join(str(b) for b in biggest))
    result = reduce(mul, (len(c) for c in biggest))
    print(result)


if __name__ == "__main__":
    main()
