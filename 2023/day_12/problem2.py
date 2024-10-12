"""
Advent of Code 2023
Day: 12
Problem: 02
Author: Nathan Rand
Date: 10.12.2024
"""
import itertools
from enum import StrEnum
from typing import List, NamedTuple

_UNFOLD_AMOUNT = 5

class Spring(StrEnum):
    DAMAGED = "#"
    OPERATIONAL = "."
    UNKNOWN = "?"


def _map_possibility_to_springs(possibility: List, springs: str):
    unknown_indices =  [i for i, ltr in enumerate(springs) if ltr == Spring.UNKNOWN]
    possible_springs = []
    idx = 0
    for i in range(len(springs)):
        if i not in unknown_indices:
            possible_springs.append(springs[i])
            continue
        possible_springs.append(possibility[idx])
        idx += 1
    return "".join(possible_springs)

def _get_record_from_springs(springs: str):
    record = []
    count = 0
    for i in range(len(springs)):
        if springs[i] == Spring.DAMAGED:
            count += 1
            continue

        if count > 0:
            record.append(count)
            count = 0

    if count > 0:
        record.append(count)

    return record

class ConditionRecord(NamedTuple):
    springs: str
    record: str

    @classmethod
    def load(cls, row):
        springs, record_str = row.split(" ")
        record = [int(r) for r in record_str.split(",")]
        return cls(springs, record)

    def get_num_arrangements(self):
        """Determines the number of possible arrangements for a condition record."""
        # Determine the missing number of damaged springs
        num_missing_damaged_springs = sum(self.record) - self.springs.count(Spring.DAMAGED)
        num_unknown_springs = self.springs.count(Spring.UNKNOWN)
        product = list(itertools.product([Spring.DAMAGED.value, Spring.OPERATIONAL.value], repeat=num_unknown_springs))
        possibilities = [possibility for possibility in product if possibility.count(Spring.DAMAGED) == num_missing_damaged_springs]
        print(len(possibilities))
        num_arrangements = 0
        # for possibility in possibilities:
        #     spring_possibile_order = _map_possibility_to_springs(possibility, self.springs)
        #     curr_record = _get_record_from_springs(spring_possibile_order)
        #     if curr_record == self.record:
        #         num_arrangements += 1
        
        return num_arrangements


def main():
    with open("example.txt", "r") as f:
        # First read in our file data for the universe
        condition_records = [ConditionRecord.load(row)  for row in f.read().split("\n")]

    # Unfold our condition records
    unfolded_condition_records = []
    for cr in condition_records:
        unfolded_springs = Spring.UNKNOWN.join([cr.springs]*_UNFOLD_AMOUNT)
        unfolded_record = cr.record*_UNFOLD_AMOUNT
        unfolded_condition_records.append(ConditionRecord(unfolded_springs, unfolded_record))
    
    # Compute our total number of arrangements
    num_arrangements = 0
    for cr in unfolded_condition_records:
        num_arrangements += cr.get_num_arrangements()
    
    # Output the result
    print(f"Total number of arrangements for the unfolded condition records is: {int(num_arrangements)}")

if __name__ == "__main__":
    main() 