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
    for product_id_range in ranges:
        for product_id in product_id_range:
            id_string = str(product_id)

            for prefix_size in range(1, len(id_string)):
                # Keep only prefix sizes that are divisors of the total size
                if len(id_string) % prefix_size != 0:
                    continue
                # Check if number is a repeat of prefix
                prefix = id_string[:prefix_size]
                if str(prefix) * (len(id_string) // prefix_size) == id_string:
                    invalid_ids_sum += product_id
                    invalid_ids_count += 1
                    print(
                        "[%d-%d] Invalid: %d (%dx)"
                        % (
                            product_id_range.start,
                            product_id_range.stop,
                            product_id,
                            prefix_size,
                        )
                    )

                    # Avoid counting multiple times the same prefix
                    break

    print("Found %d invalid ids" % invalid_ids_count)
    print("Sum of invalid ids: %d" % invalid_ids_sum)


if __name__ == "__main__":
    main()
