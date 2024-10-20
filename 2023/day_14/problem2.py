"""
Advent of Code 2023
Day: 14
Problem: 02
Author: Nathan Rand
Date: 10.19.2024
"""
from copy import deepcopy
from enum import Enum, StrEnum
import time
import numpy as np

_EMPTY = "."

class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4

class Rock(StrEnum):
    ROUND = "O"
    CUBE = "#"

def main():
    start_time = time.time()
    with open("example.txt", "r") as f:
        platform = np.array([list(row) for row in f.read().split("\n")])
    
    total_load = 0
    # Planks are our columns, but this name is more fun
    first_cycle = True
    tilt = 1
    cycle = 0
    original_platform = deepcopy(platform)
    while not np.array_equal(original_platform, platform) or first_cycle:
        first_cycle = False
        platform = platform.T if tilt in [Direction.NORTH.value, Direction.SOUTH.value] else platform
        for i, plank in enumerate(platform):
            slide_spot = 0
            for j in range(len(plank)):
                match plank[j]:
                    case Rock.CUBE:
                        slide_spot = i+1
                    case Rock.ROUND:
                        print(platform)
                        print(" ")
                        print([i, slide_spot])
                        platform[i, slide_spot] = Rock.ROUND
                        if slide_spot != j:
                            platform[i, j] = _EMPTY
                        print(platform)
                        slide_spot += 1
        if tilt < 4:
            tilt += 1
            continue
        cycle += 1
        tilt = 1
        if cycle == 3:
            break
    # print(original_platform)
    # print(" ")
    # print(platform)
    
    # Output our results
    print(f"Total load on the North Support Beams: {total_load}")
    print(f"Time for computation: {time.time() - start_time} s")

if __name__ == "__main__":
    main() 