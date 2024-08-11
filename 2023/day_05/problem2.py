"""
Advent of Code 2023
Day: 05
Problem: 02
Author: Nathan Rand
Date: 08.07.2024
"""
import regex as re
from FarmingMap import FarmingMap
import sys

_MAP_IDENTIFYING_STRING = "map:"

def main():
    with open("input.txt", "r") as f:
        farming_maps = []
        almanac = f.read().split("\n")

    # First, remove all blank lines that are stored in our
    # list as an empty string
    almanac = [line for line in almanac if line != ""]
    
    # Grab the first line of the file that contains our seed range nums
    seed_range_nums = [int(seed) for seed in re.findall(r'\d+', almanac.pop(0))]
    seed_ranges= []
    # Unpack our seed range nums in pairs to determine our total list of seeds
    for i in range(0, len(seed_range_nums), 2):
        seed_ranges.append(range(seed_range_nums[i], seed_range_nums[i]+seed_range_nums[i+1]))

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
    mapped_seed_ranges = seed_ranges
    for farming_map in farming_maps:
        mapped_seed_ranges = farming_map.map_ranges(mapped_seed_ranges)

        # Flatten out our mapped_seed_ranges to ensure it a list of ranges
        # (we need this in the case our ranges are split during mapping)
        mapped_seed_ranges = [range for ranges in mapped_seed_ranges for range in ranges]
    
    # Grab our lowest range value for each range
    low_location_numbers = [mapped_range[0] for mapped_range in mapped_seed_ranges]
        
    # Finally, print out the lowest location number
    print(f"Lowest Location Number: {min(low_location_numbers)}")


if __name__ == "__main__":
    main() 