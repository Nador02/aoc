"""
Advent of Code 2023
Day: 13
Problem: 02
Author: Nathan Rand
Date: 10.19.2024
"""
import time
from typing import NamedTuple
import numpy as np

class MirrorBound(NamedTuple):
    l: int
    r: int
    smudged: bool

def _get_num_differences(arr1, arr2):
    total_num = len(arr1)
    same = np.sum(arr1 == arr2)
    return total_num-same

def get_mirror_sum_contribution(puzzle: np.ndarray, vertical=False):
    # Go through our first row to determine any potential mirror lines
    first_row = puzzle[0]
    mirror_bounds = []
    for i in range(1, len(first_row)):
        closest_boundary = 0 if (2*i-1)/2 < len(first_row)/2 else len(first_row)-1

        if closest_boundary == 0:
            num_diff = _get_num_differences(first_row[:i], first_row[i:i+i][::-1])
            if num_diff < 2:
                mirror_bounds.append(MirrorBound(closest_boundary, i+i-1, num_diff==1))

        if closest_boundary == len(first_row)-1:
            num_diff = _get_num_differences(first_row[2*i-len(first_row):i], first_row[i:][::-1])
            if num_diff < 2:
                mirror_bounds.append(MirrorBound(2*i-len(first_row), closest_boundary, num_diff==1))

    # # Now remove mirror bounds if they do not work
    # for row in puzzle[1:]:
    #     if len(mirror_bounds) == 0:
    #         return 0
    #     new_mirror_bounds = []
    #     for mirror_bound in mirror_bounds:
    #         mid = int(np.ceil(sum(mirror_bound)/2))
    #         if np.array_equal(row[mirror_bound[0]:mid], row[mid:mirror_bound[1]+1][::-1]):
    #             new_mirror_bounds.append(mirror_bound)
    #     mirror_bounds = new_mirror_bounds

    # if len(mirror_bounds) == 0:
    #     return 0

    # scale_factor = 1 if vertical else 100
    # return scale_factor*(sum(mirror_bounds[0])//2+1)
    return 0
    


def main():
    start_time = time.time()
    with open("example.txt", "r") as f:
        puzzles = [np.array([list(row) for row in puzzle_str.split("\n")]) for puzzle_str in f.read().split("\n\n")]
    
    # Go through each puzzle and determine their sum contributions
    # based on their positions of a vertical or horizontal mirror line
    pattern_notes_sum = 0
    for puzzle in puzzles:
        pattern_notes_sum += get_mirror_sum_contribution(puzzle, vertical=True) + get_mirror_sum_contribution(puzzle.T, vertical=False)
    
    # Output our results
    print(f"Pattern Notes Summary after finding all Mirror Lines is: {pattern_notes_sum}")
    print(f"Time for computation: {time.time() - start_time} s")

if __name__ == "__main__":
    main() 