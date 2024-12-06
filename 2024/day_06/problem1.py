"""
Advent of Code 2024
Day: 06
Problem: 01
Author: Nathan Rand
Date: 12.06.2024
"""

_INPUT_FILE_NAME = "example.txt"


def main():
    """Advent of Code - Day 06 - Part 01 [Guard Gallivant]"""
    # Read in our input file (the suit factory lab map)
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        lab_map = f.read().split("\n")
        print(lab_map)


if __name__ == "__main__":
    main()
