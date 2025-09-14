"""
Advent of Code 2024
Day: 17
Problem: 01
Author: Nathan Rand
Date: 12.18.24
"""
import re
from chronospatial_computer import get_chrono_computer_output
_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 17 - Part 01 [Chronospatial Computer]"""
    # Read in our input file with the given registers and program
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        registers_str, program_str = f.read().split("\n\n")

    # Process our input strings into registers and program for easier use
    registers = {
        register: int(val) for register, val in
        zip(["A", "B", "C"], re.findall(r"(\d+)", registers_str))
    }
    program = [int(num) for num in re.findall(r"(\d)", program_str)]

    # Go through our programs performing the instructed actions
    program_output = get_chrono_computer_output(program, registers)

    # Form our program output string
    program_output_str = ",".join([str(num) for num in program_output])

    # Output our result
    print(
        "The resulting output once the program halts is: "
        f"{program_output_str}"
    )


if __name__ == "__main__":
    main()
