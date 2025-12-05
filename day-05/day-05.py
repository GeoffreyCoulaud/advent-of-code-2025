from argparse import ArgumentParser, Namespace


class CliArgs(Namespace):
    file_path: str


def check_ranges_intersect(range1: range, range2: range) -> bool:
    return (
        range1.start in range2
        or (range1.stop - 1) in range2
        or range2.start in range1
        or (range2.stop - 1) in range1
    )


def merge_ranges(range1: range, range2: range) -> range:
    new_start = min(range1.start, range2.start)
    new_end = max(range1.stop, range2.stop)
    return range(new_start, new_end)


def get_disjoined_ranges(input_ranges: list[range]) -> list[range]:
    disjoined_ranges = list[range]()
    to_check = [*input_ranges]
    cursor = 0
    while cursor < len(to_check):
        range1 = to_check[cursor]
        for j, range2 in enumerate(to_check[cursor + 1 :]):
            # Check for intersection
            range2_index = cursor + 1 + j
            if check_ranges_intersect(range1, range2):
                new = merge_ranges(range1, range2)
                message = "%d-%d" % (range1.start, range1.stop - 1)
                message += " and %d-%d" % (range2.start, range2.stop - 1)
                message += " become %d-%d" % (new.start, new.stop - 1)
                print(message)
                to_check.pop(range2_index)
                to_check[cursor] = new
                break
        else:
            # Range does not intersect with anything, keep it as is
            disjoined_ranges.append(range1)
            cursor += 1
    return disjoined_ranges


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    fresh_ranges = list[range]()
    available_ids = set[int]()
    is_parsing_available_ids = False
    with open(args.file_path, "r") as file:
        for raw_line in file:
            line = raw_line.strip()
            # Handle the switch to availables
            if not is_parsing_available_ids and line == "":
                print("Parsing available IDs")
                is_parsing_available_ids = True
                continue
            # Handle fresh range
            if not is_parsing_available_ids:
                split = line.split("-")
                start = int(split[0])
                stop = int(split[1]) + 1
                fresh_ranges.append(range(start, stop))
            # Handle available
            if is_parsing_available_ids:
                available_ids.add(int(line))

    available_and_fresh = set[int]()
    for i in available_ids:
        for r in fresh_ranges:
            if i in r:
                available_and_fresh.add(i)
                break

    disjoined_fresh_ranges = get_disjoined_ranges(fresh_ranges)
    for r in disjoined_fresh_ranges:
        print("%d-%d" % (r.start, r.stop - 1))

    print("Count of available and fresh: %d" % len(available_and_fresh))
    print("Count of unique fresh ids: %d" % sum(len(r) for r in disjoined_fresh_ranges))


if __name__ == "__main__":
    main()
