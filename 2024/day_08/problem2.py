"""
Advent of Code 2024
Day: 08
Problem: 02
Author: Nathan Rand
Date: 12.08.24
"""
import re
from typing import List
_INPUT_FILE_NAME = "input.txt"


def _is_antinode_in_map(antenna_map: List[str], antinode_pos: tuple):
    return (
        antinode_pos[0] >= 0 and antinode_pos[0] < len(antenna_map)
        and antinode_pos[1] >= 0 and antinode_pos[1] < len(antenna_map[0])
    )


def _find_resonant_antinodes_for_antennas_pair(antenna_map, antenna1, antenna2):
    antinodes = [antenna1, antenna2]
    distance = (antenna1[0]-antenna2[0], antenna1[1]-antenna2[1])

    # March in the `antenna1` direction till out of the map
    antinode = (antenna1[0] + distance[0], antenna1[1] + distance[1])
    while _is_antinode_in_map(antenna_map, antinode):
        antinodes.append(antinode)
        antinode = (antinode[0] + distance[0], antinode[1] + distance[1])

    # Do the same in the `antenna2` direction till we fall out of the map
    antinode = (antenna2[0] - distance[0], antenna2[1] - distance[1])
    while _is_antinode_in_map(antenna_map, antinode):
        antinodes.append(antinode)
        antinode = (antinode[0] - distance[0], antinode[1] - distance[1])

    return antinodes


def _find_resonant_antinodes_for_frequency(antenna_map, antennas):
    antinodes = set()
    for i in range(len(antennas)-1):
        for j in range(i+1, len(antennas)):
            antenna1, antenna2 = antennas[i], antennas[j]
            antinodes.update(_find_resonant_antinodes_for_antennas_pair(
                antenna_map, antenna1, antenna2))
    return antinodes


def main():
    """Advent of Code - Day 08 - Part 02 [Resonant Collinearity]"""
    # Read in our antenna map
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        antenna_map = f.read().split("\n")

    # Find the positions of all of our antenna's and their
    # corresponding frequencies
    antennas = {}
    for row, map_row_str in enumerate(antenna_map):
        antenna_matches = re.finditer(r"[0-9a-zA-Z]{1}", map_row_str)
        for antenna in antenna_matches:
            # Unpack our antenna match info
            frequency = antenna.group(0)
            col = antenna.start()

            # Add it to our antennas dictionary
            if frequency in antennas:
                antennas[frequency].append((row, col))
            else:
                antennas[frequency] = [(row, col)]

    # Find the position of antinodes and add them to our running sum
    # if they are within the bounds of the map
    antinodes = set()
    for frequency, antenna_positions in antennas.items():
        antinodes.update(_find_resonant_antinodes_for_frequency(antenna_map, antenna_positions))

    # Output the resulting number of unique antinode locations
    print(
        "The numer of unique antinode locations that fall within "
        f"our antenna map is: {len(antinodes)} antinodes"
    )


if __name__ == "__main__":
    main()
