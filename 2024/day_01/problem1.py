"""
Advent of Code 2024
Day: 01
Problem: 01
Author: Nathan Rand
Date: 12.01.2024
"""
import heapq
import numpy as np

_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 01 - Part 01 [Historian Hysteria]"""
    # Load in our input file using numpy to get a list of our position lists
    # and then heapify them
    position_heaps = np.loadtxt(_INPUT_FILE_NAME).T.tolist()
    for pos_list in position_heaps:
        heapq.heapify(pos_list)  # This function operates in place

    # Pop min values off of each heap and add their abs val diff to our accumulator
    total_distance = 0
    while position_heaps[0]:
        total_distance += abs(heapq.heappop(
            position_heaps[0]) - heapq.heappop(position_heaps[1]))

    # Output our results
    print(f"Total distance between the two lists is: {int(total_distance)}")


if __name__ == "__main__":
    main()
