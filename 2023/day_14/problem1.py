"""
Advent of Code 2023
Day: 14
Problem: 01
Author: Nathan Rand
Date: 10.19.2024
"""
from enum import StrEnum
import time
import numpy as np

_EMPTY = "."

class Rock(StrEnum):
    ROUND = "O"
    CUBE = "#"

def main():
    start_time = time.time()
    with open("input.txt", "r") as f:
        platform = np.array([list(row) for row in f.read().split("\n")])
    
    total_load = 0
    # Planks are our columns, but this name is more fun
    for plank in platform.T:
        slide_spot = 0
        for i in range(len(plank)):
            match plank[i]:
                case Rock.CUBE:
                    slide_spot = i+1
                case Rock.ROUND:
                    total_load += len(plank)-slide_spot
                    slide_spot += 1
    
    # Output our results
    print(f"Total load on the North Support Beams: {total_load}")
    print(f"Time for computation: {time.time() - start_time} s")

if __name__ == "__main__":
    main() 