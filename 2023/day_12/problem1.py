"""
Advent of Code 2023
Day: 12
Problem: 01
Author: Nathan Rand
Date: 10.12.2024
"""

from typing import NamedTuple


class ConditionRecord(NamedTuple):
    springs: str
    record: str

    def get_num_arrangements(self):
        """Determines the number of possible arrangements for a condition record."""
        # TODO: implement logic here
        return 1


def main():
    with open("example.txt", "r") as f:
        # First read in our file data for the universe
        condition_records = [ConditionRecord(row.split(" ")[0], row.split(" ")[1])  for row in f.read().split("\n")]
    
    # Compute our total number of arrangements
    num_arrangements = 0
    for cr in condition_records:
        num_arrangements += cr.get_num_arrangements()
    
    # Output the result
    print(f"Total number of arrangements for the condition records is: {int(num_arrangements)}")

if __name__ == "__main__":
    main() 