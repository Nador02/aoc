"""
Advent of Code 2024
Day: 17
Problem: 01
Author: Nathan Rand
Date: 12.18.24
"""
import re
_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 17 - Part 01 [Chronospatial Computer]"""
    # Read in our input file with the given registers and program
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        _, program_str = f.read().split("\n\n")

    # Process our input string and grab the program to use for determining
    # the corresponding register
    program = [int(num) for num in re.findall(r"(\d)", program_str)]

    register_A = 0
    for i, num in enumerate(program[::-1]):
        register_A += num*8**(len(program)-i)

    # Output our result
    print(
        "To make our program input match the output, register A "
        f"should be defined as: A = {register_A}"
    )


if __name__ == "__main__":
    main()
