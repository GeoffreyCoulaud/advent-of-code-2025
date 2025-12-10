import logging
from argparse import ArgumentParser, Namespace
from typing import NamedTuple


class CliArgs(Namespace):
    file_path: str
    connections: int
    count_to_multiply: int


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __str__(self):
        return ",".join(["%03d" % c for c in self])


IndexedVec3 = tuple[int, Vec3]
PairOfIndexedVec3 = tuple[IndexedVec3, IndexedVec3]


def pair_get_indexes(pair: PairOfIndexedVec3) -> tuple[int, int]:
    (i, _), (j, _) = pair
    return (i, j)


def pair_get_vectors(pair: PairOfIndexedVec3) -> tuple[Vec3, Vec3]:
    (_, a), (_, b) = pair
    return a, b


def pair_distance_squared(pair: PairOfIndexedVec3) -> float:
    return sum((ca - cb) ** 2 for ca, cb in zip(*pair_get_vectors(pair)))


def build_sorted_pairs(positions: list[Vec3]) -> list[tuple[int, int]]:
    """Create a list of unique pairs of indexes, sorted by smallest distance"""
    pairs = list[PairOfIndexedVec3]()
    for i in range(len(positions) - 1):
        for j in range(i + 1, len(positions)):
            pair = ((i, positions[i]), (j, positions[j]))
            pairs.append(pair)
    pairs.sort(key=pair_distance_squared)
    return [pair_get_indexes(pair) for pair in pairs]


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

    # Start with each box in its own circuit
    circuits = [{i} for i in range(len(positions))]
    circuit_per_box = {i: i for i in range(len(positions))}

    # Merge circuits with N connections
    box_index_pairs: list[tuple[int, int]] = build_sorted_pairs(positions)
    for i, (a_box_index, b_box_index) in enumerate(box_index_pairs[: args.connections]):
        a_circuit_index = circuit_per_box[a_box_index]
        b_circuit_index = circuit_per_box[b_box_index]

        msg = "%d -  %s <-> %s"
        msg_args = [i, positions[a_box_index], positions[b_box_index]]

        if a_circuit_index == b_circuit_index:
            msg += " Skipped"
            logging.info(msg, *msg_args)
            continue

        # Assign box to new circuit
        circuit_per_box[b_box_index] = a_circuit_index
        circuits[b_circuit_index].remove(b_box_index)
        circuits[a_circuit_index].add(b_box_index)

        msg += " Merged into %d"
        msg_args += [a_circuit_index]
        logging.info(msg, *msg_args)

    # Sort the circuits by size
    circuits = [c for c in circuits if len(c) > 0]
    sorted_circuits = sorted(circuits, key=len, reverse=True)
    for circuit in sorted_circuits:
        logging.info(", ".join("%02d" % box_index for box_index in circuit))

    # Compute the result
    result = 1
    for circuit in sorted_circuits[: args.count_to_multiply]:
        result *= len(circuit)
    print(result)


if __name__ == "__main__":
    main()
