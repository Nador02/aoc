"""
Advent of Code 2023
Day: 09
Problem: 02
Author: Nathan Rand
Date: 08.17.2024
"""
import re
from typing import List

_HISTORY_PATTERN = r'-?\d+'

def gen_pyramid_from_history(history: List[int]):
    history_pyramid = [history]
    while not all(v==0 for v in history_pyramid[-1]):
        next_row = []
        for i in range(1,len(history_pyramid[-1])):
            next_row.append(history_pyramid[-1][i]-history_pyramid[-1][i-1])
        history_pyramid.append(next_row)

    return history_pyramid

def main():
    with open("input.txt", "r") as f:
        # First read in our ecological value history data
        history_strings = f.read().split("\n")
        histories = []
        for history_string in history_strings:
            histories.append([int(value) for value in re.findall(_HISTORY_PATTERN, history_string)])

    # Then march through creating our history pyramids
    history_pyramids = []
    for history in histories:
        history_pyramids.append(gen_pyramid_from_history(history))
    
    # Now we go through all of our pyramids and extrapolate our history
    extrapolated_sum = 0
    for history_pyramid in history_pyramids:
        # Add a zero to the end of the bottom of our pyramid
        history_pyramid[-1].insert(0,0)

        # Go from the bottom to the top of our upside down pyramid
        # to extrapolate our previous history values
        for i in reversed(range(len(history_pyramid)-1)):
            history_pyramid[i].insert(0,history_pyramid[i][0]-history_pyramid[i+1][0])
    
        # Add the resulting extrapolated value to our sum and continue
        extrapolated_sum += history_pyramid[0][0]

    # Output our result
    print(f"The sum of the extrapolated ecological history values is: {extrapolated_sum}")

if __name__ == "__main__":
    main() 