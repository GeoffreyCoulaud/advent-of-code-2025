from argparse import ArgumentParser, Namespace
from enum import StrEnum
from typing import Literal


class CliArgs(Namespace):
    file_path: str


class DialRotationDirection(StrEnum):
    L = "L"
    R = "R"


class Dial:
    __size: int
    __position: int
    __pointed_at_zero_count: int
    __returns_at_zero_count: int

    def __init__(self, starting_position: int, size: int):
        self.__position = starting_position
        self.__size = size
        self.__returns_at_zero_count = 0
        self.__pointed_at_zero_count = 0

    def __get_rotation_multplier(
        self, direction: DialRotationDirection
    ) -> Literal[1, -1]:
        return -1 if direction == DialRotationDirection.L else 1

    def rotate(self, direction: DialRotationDirection, amount: int) -> None:
        pointed_at_zero_count = 0
        factor = self.__get_rotation_multplier(direction)
        new_position = self.__position

        # Turbo-stupid code, but should work
        for _ in range(amount):
            new_position = (new_position + factor) % self.__size
            if new_position == 0:
                pointed_at_zero_count += 1

        # Update counters
        self.__pointed_at_zero_count += pointed_at_zero_count
        if new_position == 0:
            self.__returns_at_zero_count += 1

        message = "Moving dial: %02d -[%s%02d]-> %02d" % (
            self.__position,
            direction,
            amount,
            new_position,
        )
        if pointed_at_zero_count > 0:
            message += " (pointed at zero %d times)" % pointed_at_zero_count
        print(message)

        # Apply the new position
        self.__position = new_position

    @property
    def position(self) -> int:
        return self.__position

    @property
    def pointed_at_zero_count(self) -> int:
        return self.__pointed_at_zero_count

    @property
    def returns_at_zero_count(self) -> int:
        return self.__returns_at_zero_count


def main():
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    dial = Dial(starting_position=50, size=100)

    with open(file=args.file_path, mode="r") as file:
        for raw_line in file:
            line = raw_line.rstrip()
            direction = DialRotationDirection(line[0])
            amount = int(line[1:])
            dial.rotate(direction=direction, amount=amount)

    print("Final position: %d" % dial.position)
    print("Returns at zero: %d" % dial.returns_at_zero_count)
    print("Pointed at zero: %d" % dial.pointed_at_zero_count)


if __name__ == "__main__":
    main()
