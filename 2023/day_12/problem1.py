"""
Advent of Code 2023
Day: 12
Problem: 01
Author: Nathan Rand
Date: 10.12.2024
"""
import itertools
from enum import StrEnum
import re
from typing import List, NamedTuple


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

def _find_trimmed_possibilities(springs, idx, record):
    possible_indices = [m.start() for m in re.finditer(
    f"(?={f"\\{Spring.UNKNOWN}|{Spring.DAMAGED}"}){{{record[idx]}}}", 
    springs)
    ]
    trimmed_possibilities = [springs[i+2:] for i in possible_indices]
    min_length = sum(record[idx+1:]) + (len(record)-idx-2)

    return [poss for poss in trimmed_possibilities if len(poss) >= min_length]

def _find_possibilities(springs, idx, record):
    possible_indices = []
    first_dmg_spring_idx = springs.find(Spring.DAMAGED)+1 if Spring.DAMAGED in springs else float('inf')

    for i in range(min(first_dmg_spring_idx, len(springs)-record[idx])):
        if i + record[idx] < len(springs):
            if springs[i + record[idx]] == Spring.DAMAGED:
                continue
        if Spring.OPERATIONAL not in springs[i:i+record[idx]]:
            possible_indices.append(i)
    min_length = sum(record[idx+1:]) + (len(record)-idx-2)
    possibilities = [springs[i+record[idx]+1:] for i in possible_indices]
    possibilities = [poss for poss in possibilities if len(poss) >= min_length]
    return possibilities


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

        num_arrangements = 0
        for possibility in possibilities:
            spring_possibile_order = _map_possibility_to_springs(possibility, self.springs)
            curr_record = _get_record_from_springs(spring_possibile_order)
            if curr_record == self.record:
                num_arrangements += 1
        
        return num_arrangements

    def get_num_arrangements_faster(self):
        """Determines the number of possible arrangements for a condition record."""
        # Create all possibilities for the first case
        trimmed_possibilities = _find_possibilities(self.springs, 0, self.record)
        
        # Iterate through the remaining to trim our possibilities down to the remaining possibilities
        for i in range(1, len(self.record)-1):
            new_trimmed_possibilities = []
            for possibility in trimmed_possibilities:
                new_trimmed_possibilities.extend(_find_possibilities(possibility, i, self.record))
            trimmed_possibilities = new_trimmed_possibilities
        
        # Final step
        num_arrangements = 0
        for poss in trimmed_possibilities:
            possible_indices = [m.start() for m in re.finditer(
                f"(?={f"[\\{Spring.UNKNOWN}|{Spring.DAMAGED}]{{{self.record[-1]}}}"})", 
                poss)
            ]
            for idx in possible_indices:
                temp_poss = poss[:idx] + self.record[-1]*Spring.DAMAGED + poss[idx+self.record[-1]:]
                if temp_poss.count(Spring.DAMAGED) != self.record[-1]:
                    continue
                num_arrangements += 1
        return num_arrangements

def main():
    with open("input.txt", "r") as f:
        # First read in our file data for the universe
        condition_records = [ConditionRecord.load(row)  for row in f.read().split("\n")]
        
    
    # Compute our total number of arrangements
    num_arrangements = 0
    for cr in condition_records:
        num_arrangements += cr.get_num_arrangements_faster()
    
    # Output the result
    print(f"Total number of arrangements for the condition records is: {int(num_arrangements)}")

if __name__ == "__main__":
    main() 