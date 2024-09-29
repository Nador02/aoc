"""
Advent of Code 2023
Day: 11
Problem: 02
Author: Nathan Rand
Date: 09.22.2024
"""
from typing import List
import numpy as np
from copy import deepcopy

_GALAXY_CHAR = "#"
_EMPTY_SPACE_CHAR = "."
_EXPANSION_FACTOR = 1e6

def main():
    with open("input.txt", "r") as f:
        # First read in our file data for the universe
        universe = np.array([list(universe_row) for universe_row in f.read().split("\n")])

    # First find the current position of all galaxies
    # with no current universe expansion
    galaxies = []
    for j, row in enumerate(universe):
        for i, spot in enumerate(row):
            if spot == _GALAXY_CHAR:
                galaxies.append([i,j])
    
    # Now go through each row and col, adjusting the position
    # of our galaxies with the expansion factor
    expanded_galaxies = deepcopy(galaxies)
    # First for all the rows (expanding pos. in the y-direction)
    for j, universe_row in enumerate(universe):
        if _GALAXY_CHAR in universe_row:
            continue
        
        for i in range(len(galaxies)):
            galaxy = galaxies[i]
            expanded_galaxy = expanded_galaxies[i]
            if galaxy[1] > j:
                expanded_galaxy[1] += _EXPANSION_FACTOR-1
    
    # Then for all the cols (expanding pos. in the x-direction)
    for i, universe_col in enumerate(universe.T):
        if _GALAXY_CHAR in universe_col:
            continue

        for j in range(len(galaxies)):
            galaxy = galaxies[j]
            expanded_galaxy = expanded_galaxies[j]
            if galaxy[0] > i:
                expanded_galaxy[0] += _EXPANSION_FACTOR-1

    # Finally, go through and sum all our lengths for each galaxy pair
    length_sum = 0
    for i in reversed(range(1, len(expanded_galaxies))):
        curr_galaxy = expanded_galaxies[i]
        for j in range(0, i):
            galaxy = expanded_galaxies[j]
            shortest_distance = abs(galaxy[0]-curr_galaxy[0]) + abs(galaxy[1]-curr_galaxy[1])
            length_sum += shortest_distance
    
    # Output our resulting sum
    print(f"The sum of all the shortest galaxy lengths is: {int(length_sum)} with an expansion factor of: {_EXPANSION_FACTOR}")

if __name__ == "__main__":
    main() 