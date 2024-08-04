"""
Advent of Code 2023
Day: 03
Problem: 02
Author: Nathan Rand
Date: 08.04.2024
"""
import regex as re
import numpy as np

_PART_NUMBER_PATTERN = re.compile(r'\d{1,3}')
_GEAR_PATTERN = "[*]+"

def main():
    with open("input.txt", "r") as f:
        schematic = f.read().split("\n")
        gear_ratios_sum = 0
        for i in range(len(schematic)):
            # Get part numbers for the rows to consider
            part_numbers = get_part_numbers_in_row(schematic[i])
            if i != 0: # First row (no row above)
                part_numbers.extend(get_part_numbers_in_row(schematic[i-1]))
            if i != len(schematic)-1: # Last row (no row below)
                part_numbers.extend(get_part_numbers_in_row(schematic[i+1]))
            
            # Get gear positions `*`
            gear_positions = [m.start(0) for m in re.finditer(_GEAR_PATTERN, schematic[i])]
            
            # Check if a gear is a valid gear (2 adjacent numbers)
            for gear in gear_positions:
                 gear_ratios_sum += get_gear_ratio(gear, part_numbers)

        print(f"Sum of all part numbers in engine schematic: {gear_ratios_sum}")

def get_part_numbers_in_row(row):
    part_numbers_list = _PART_NUMBER_PATTERN.findall(row)
    part_numbers_positions = [(m.start(0), m.end(0)) for m in re.finditer(_PART_NUMBER_PATTERN, row)]
    part_numbers = [(int(part_numbers_list[i]), part_numbers_positions[i]) for i in range(len(part_numbers_list))]
    return part_numbers

def get_gear_ratio(gear, part_numbers):
    touching_nums = []
    for part_num, part_pos in part_numbers:
        part_range = range(part_pos[0]-1, part_pos[1]+1)
        if gear in part_range:
            touching_nums.append(part_num)
    if len(touching_nums) == 2:
        return np.prod(touching_nums)
    return 0

if __name__ == "__main__":
    main() 