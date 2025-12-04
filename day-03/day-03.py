from argparse import ArgumentParser, Namespace


class CliArgs(Namespace):
    file_path: str
    digits: int


def find_max_index(digits: list[int]) -> int:
    max_digit = -1
    max_digit_index = 0
    for i, digit in enumerate(digits):
        if digit > max_digit:
            max_digit = digit
            max_digit_index = i
    return max_digit_index


def find_max_joltage(digits: list[int], to_keep: int) -> int:
    kept = list[int]()
    remaining = [*digits]
    for _ in range(to_keep):
        # Find the first max in haystack minus a buffer at the end
        # eg. With still 3 digits to add
        # -> "123456789" are the digits left
        # -> "1234567"   are searched
        # If we considered 8, we'd have less digits left than needed
        i = find_max_index(remaining[: len(remaining) + 1 - to_keep + len(kept)])
        kept.append(remaining[i])
        remaining = remaining[i + 1 :]
    return sum(digit * 10**i for i, digit in enumerate(reversed(kept)))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("digits", type=int, default=12)
    args = parser.parse_args(namespace=CliArgs())

    total_max_joltage = 0
    with open(args.file_path, "r") as file:
        for i, line_raw in enumerate(file):
            line = line_raw.strip()
            line_max_joltage = find_max_joltage([int(d) for d in line], args.digits)
            total_max_joltage += line_max_joltage
            print("[%d] %s -> %d" % (i, line, line_max_joltage))

    print("Total max joltage: %d" % total_max_joltage)


if __name__ == "__main__":
    main()
