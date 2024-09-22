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

def expand_galaxy(galaxy: np.array):
    """Expands the provided galaxy"""
    expanded_galaxy = []
    for i, galaxy_strip in enumerate(galaxy):
        if _GALAXY_CHAR in galaxy_strip:
            expanded_galaxy.append(galaxy_strip)
            continue
            
        # If no galaxy is in this row/col, add a row below
        # with more empty space
        expanded_galaxy.extend([galaxy_strip, galaxy_strip])

    return np.array(expanded_galaxy)

def main():
    with open("example1.txt", "r") as f:
        # First read in our file data for the galaxy
        galaxy = np.array([list(galaxy_row) for galaxy_row in f.read().split("\n")])

    # Expand our galaxy in both the column and row direction
    expanded_galaxy = expand_galaxy(galaxy) # <- First do it for rows
    expanded_galaxy = expand_galaxy(expanded_galaxy.T).T # <- then cols
    print(expanded_galaxy)
    
    # TODO: Find shorted path between all galaxies,
    # first identify where they are, and then apply distance formula
    # potentially while identifying where they are?? (Then we can 
    # do this in O(N))

if __name__ == "__main__":
    main() 