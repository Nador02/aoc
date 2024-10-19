"""
Advent of Code 2023
Day: 12
Problem: 01
Author: Nathan Rand
Date: 10.12.2024
"""
from enum import StrEnum
import time
from typing import NamedTuple


class Spring(StrEnum):
    DAMAGED = "#"
    OPERATIONAL = "."
    UNKNOWN = "?"


class ConditionRecord(NamedTuple):
    springs: str
    record: str

    @classmethod
    def load(cls, row):
        springs, record_str = row.split(" ")
        record = [int(r) for r in record_str.split(",")]
        return cls(springs, record)
    
arrangements_cache = {}
    
def get_num_arrangements(springs, record):
    if not record:
        return 1 if Spring.DAMAGED not in springs else 0
    
    cache_key = springs + ','.join(str(x) for x in record)
    if cache_key in arrangements_cache:
        return arrangements_cache[cache_key]

    if len(springs) == 1:
        if len(record) > 1:
            arrangements_cache[cache_key] = 0
            return arrangements_cache[cache_key]
        arrangements_cache[cache_key] = 1 if springs in [Spring.DAMAGED, Spring.UNKNOWN] and record[0] == 1 else 0
        return arrangements_cache[cache_key]
    
    if not springs:
        return 0
    
    if springs[0] == Spring.OPERATIONAL:
        arrangements_cache[cache_key] = get_num_arrangements(springs[1:], record)
        return arrangements_cache[cache_key]
    
    if springs[0] == Spring.DAMAGED:
        if len(springs) < record[0]:
            arrangements_cache[cache_key] = 0
            return arrangements_cache[cache_key]
        
        if Spring.OPERATIONAL in springs[:record[0]]:
            arrangements_cache[cache_key] = 0
            return arrangements_cache[cache_key]
        
        if len(springs) > record[0]:
            if springs[record[0]] == Spring.DAMAGED:
                arrangements_cache[cache_key] = 0
                return arrangements_cache[cache_key]

        arrangements_cache[cache_key] = get_num_arrangements(springs[record[0]+1:], record[1:])
        return arrangements_cache[cache_key]
    
    arrangements_cache[cache_key] = get_num_arrangements(Spring.DAMAGED + springs[1:], record) + get_num_arrangements(Spring.OPERATIONAL + springs[1:], record)
    return arrangements_cache[cache_key]

def main():
    start_time = time.time()
    with open("input.txt", "r") as f:
        # First read in our file data for the universe
        condition_records = [ConditionRecord.load(row)  for row in f.read().split("\n")]
        
    
    # Compute our total number of arrangements
    num_arrangements = 0
    for cr in condition_records:
        num_arrangements += get_num_arrangements(cr.springs, cr.record)
    
    # Output the result
    print(f"Total number of arrangements for the condition records is: {int(num_arrangements)}")
    print(f"Computation Time: {time.time()-start_time} s")
if __name__ == "__main__":
    main() 