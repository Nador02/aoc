"""
Advent of Code 2023
Day: 05
Problem: 01
Author: Nathan Rand
Date: 08.07.2024
"""
import regex as re
from FarmingMap import FarmingMap

_MAP_IDENTIFYING_STRING = "map:"

def main():
    with open("input.txt", "r") as f:
        farming_maps = []
        almanac = f.read().split("\n")

    # First, remove all blank lines that are stored in our
    # list as an empty string
    almanac = [line for line in almanac if line != ""]
    
    # Grab the first line of the file that contains our seeds
    seeds = [int(seed) for seed in re.findall(r'\d+', almanac.pop(0))]

    # Iterate through the remaining lines, making our maps
    for line in almanac:
        # If we find the ``map:`` string in our line, make a new map,\
        # append our old one to our list, and continue
        if _MAP_IDENTIFYING_STRING in line:
            curr_farming_map = FarmingMap()
            farming_maps.append(curr_farming_map)
            continue
    
        # Otherwise, grab this line's values and add the corresponding
        # range to our current farming map
        dest, source, range_length = [int(val) for val in re.findall(r'\d+', line)]
        curr_farming_map.add_range(
            range(source,source+range_length), 
            range(dest, dest+range_length)
        )
    
    # Now iterate through our maps, changing our seeds values each time
    mapped_seed_vals = seeds
    for farming_map in farming_maps:
        mapped_seed_vals = farming_map.map_values(mapped_seed_vals)

    # Print out all of our seeds and their mapped locations
    for i in range(len(seeds)):
        print(f"Seed: {seeds[i]} -> Location : {mapped_seed_vals[i]}")
    
    # Finally, print out the lowest location number
    print(f"\nLowest Location Number: {min(mapped_seed_vals)}")


if __name__ == "__main__":
    main() 