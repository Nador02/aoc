"""
Advent of Code 2024
Day: 03
Problem: 01
Author: Nathan Rand
Date: 12.03.2024
"""
import re
_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 03 - Part 01 [Mull It Over]"""
    # Read in our corrupted memory data
    with open(_INPUT_FILE_NAME, "r") as f:
        corrupted_memory = f.read()

    # Get all matches for our given regex pattern
    matches = re.findall(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", corrupted_memory)

    # Sum the matching multiplication instructions
    mul_instructions_sum = 0
    for match in matches:
        mul_instructions_sum += int(match[0])*int(match[1])

    # Output our result
    print(
        "The sum of all valid multiplication instructions in the "
        f"corrupted memory is: {mul_instructions_sum}"
    )


if __name__ == "__main__":
    main()
