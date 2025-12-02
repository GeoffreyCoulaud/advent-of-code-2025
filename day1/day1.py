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

    def __init__(self, starting_position: int, size: int):
        self.__position = starting_position
        self.__size = size
        self.__pointed_at_zero_count = 0
        if starting_position == 0:
            self.__pointed_at_zero_count += 1

    def __get_rotation_multplier(
        self, direction: DialRotationDirection
    ) -> Literal[1, -1]:
        return -1 if direction == DialRotationDirection.L else 1

    def rotate(self, direction: DialRotationDirection, amount: int) -> None:
        new_position = self.__position
        new_position += self.__get_rotation_multplier(direction) * amount
        # if new_position // self.__size != 0:
        #     self.__pointed_at_zero_count += abs()
        new_position %= self.__size

        print(
            "Moving dial: %02d -[%s%02d]-> %02d"
            % (
                self.__position,
                direction,
                amount,
                new_position,
            )
        )
        self.__position = new_position

    @property
    def position(self) -> int:
        return self.__position


def main():
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args(namespace=CliArgs())

    dial = Dial(starting_position=50, size=100)
    returns_to_zero = 0

    with open(file=args.file_path, mode="r") as file:
        for raw_line in file:
            line = raw_line.rstrip()
            direction = DialRotationDirection(line[0])
            amount = int(line[1:])

            dial.rotate(direction=direction, amount=amount)
            if dial.position == 0:
                returns_to_zero += 1

    print("Final position: %d" % dial.position)
    print("Returns to zero: %d" % returns_to_zero)


if __name__ == "__main__":
    main()
