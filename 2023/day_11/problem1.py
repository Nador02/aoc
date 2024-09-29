"""
Advent of Code 2023
Day: 11
Problem: 01
Author: Nathan Rand
Date: 09.22.2024
"""
import numpy as np

_GALAXY_CHAR = "#"
_EMPTY_SPACE_CHAR = "."

def expand_universe(universe: np.array):
    """Expands the provided universe"""
    expanded_universe = []
    for i, universe_strip in enumerate(universe):
        if _GALAXY_CHAR in universe_strip:
            expanded_universe.append(universe_strip)
            continue
            
        # If no universe is in this row/col, add a row below
        # with more empty space
        expanded_universe.extend([universe_strip, universe_strip])

    return np.array(expanded_universe)

def main():
    with open("input.txt", "r") as f:
        # First read in our file data for the universe
        universe = np.array([list(universe_row) for universe_row in f.read().split("\n")])

    # Expand our universe in both the column and row direction
    expanded_universe = expand_universe(universe) # <- First do it for rows
    expanded_universe = expand_universe(expanded_universe.T).T # <- then cols
    
    # Go through and find each galaxy, comparing to all previous 
    # galaxies to keep up our running sum
    length_sum = 0
    galaxies = []
    for i, row in enumerate(expanded_universe):
        for j, spot in enumerate(row):
            if spot != _GALAXY_CHAR:
                continue
            
            # If this is a galaxy, we compare to all previous and
            # add to our sum each time
            new_galaxy = (i,j)
            for galaxy in galaxies:
                shortest_distance = abs(galaxy[0]-new_galaxy[0]) + abs(galaxy[1]-new_galaxy[1])
                length_sum += shortest_distance
            
            # Then we add this galaxy to our list of galaxies
            # and continue iterating
            galaxies.append(new_galaxy)

    # Output our resulting sum
    print(f"The sum of all the shortest galaxy lengths is: {length_sum}")
if __name__ == "__main__":
    main() 