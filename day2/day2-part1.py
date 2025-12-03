from argparse import ArgumentParser, Namespace


class CliArgs(Namespace):
    file_path: str


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    with open(args.file_path) as file:
        data = file.readline()  # Only first line has data
    ranges_strings = data.split(",")
    ranges_tuples = [r.split("-") for r in ranges_strings]
    ranges = [
        # +1 because stop is exclusive in python
        range(int(r[0]), int(r[1]) + 1)
        for r in ranges_tuples
    ]

    invalid_ids_sum = 0
    invalid_ids_count = 0
    for r in ranges:
        for i in r:
            id_string = str(i)
            # Exclude odd number of digits
            if len(id_string) % 2 != 0:
                continue
            side_size = len(id_string) // 2
            left = id_string[:side_size]
            right = id_string[side_size:]
            if left == right:
                print("[%d-%d] Found invalid id: %d" % (r.start, r.stop, i))
                invalid_ids_count += 1
                invalid_ids_sum += i

    print("Found %d invalid ids" % invalid_ids_count)
    print("Sum of invalid ids: %d" % invalid_ids_sum)


if __name__ == "__main__":
    main()
