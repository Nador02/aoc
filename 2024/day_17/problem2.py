"""
Advent of Code 2024
Day: 17
Problem: 01
Author: Nathan Rand
Date: 12.18.24
"""
import re
_INPUT_FILE_NAME = "corrupted_example.txt"


def _num_to_base(num: int, base: int):
    if num == 0:
        return [0]

    num_in_base = []
    while num != 0:
        num_in_base.append(num % base)
        num //= base

    return num_in_base


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

    # NOTE: Going to brute force this first cause I am lazy
    solution_not_found = True
    A = 8**(len(program)-1)
    while solution_not_found:
        # Update our registry trying again with a new value for A)
        A += 8

        curr_output = _num_to_base(A//8, 8) + [0]
        invalid = False
        if len(program) > len(curr_output):
            continue
        else:
            for expected, computed in zip(program, curr_output):
                if expected != computed:
                    invalid = True
                    break

            solution_not_found = invalid

    # Output our result
    print(f"Register A should be: {A}")


if __name__ == "__main__":
    main()
