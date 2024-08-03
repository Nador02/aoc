"""
Advent of Code 2023
Day: 01
Problem: 02
Author: Nathan Rand
Date: 08.02.2024
"""
import math

_SPELLED_OUT_NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def main():
    sum = 0
    with open("input.txt", "r") as f:
        for line in f:
            sum += find_first_num(line)+find_last_num(line)
    print(f"The Sum of All of the Calibration Values for the Trebuchet is: {sum}")
    
def find_first_num(line):
    first_num_idx = None
    for i in range(len(line)):
        if line[i].isnumeric():
            first_num_idx = i
            break

    spelled_out_idx, spelled_out_val = get_first_spelled_out_num(line)

    return int(line[first_num_idx])*10 if first_num_idx < spelled_out_idx else spelled_out_val*10
    
def find_last_num(line):
    # Find the last num in the line
    last_num_idx = None
    for i in reversed(range(len(line))):
        if line[i].isnumeric():
            last_num_idx = i
            break

    spelled_out_idx, spelled_out_val = get_last_spelled_out_num(line)

    return int(line[last_num_idx]) if last_num_idx > spelled_out_idx else spelled_out_val
        
def get_first_spelled_out_num(line):
    # Get first spelled out num index and value
    lowest_idx = math.inf # big number
    value = -1
    for spelled_out_num, val in _SPELLED_OUT_NUMS.items():
        curr_idx = line.find(spelled_out_num)
        if curr_idx != -1 and curr_idx < lowest_idx:
            lowest_idx = curr_idx
            value = val
    return lowest_idx, value

def get_last_spelled_out_num(line):
    # Get last spelled out num index and value
    lowest_idx = math.inf # super negative number time
    value = -1
    for spelled_out_num, val in _SPELLED_OUT_NUMS.items():
        # Reverse our line and spelled out num to find the last item first
        curr_idx = line[::-1].find(spelled_out_num[::-1])
        if curr_idx != -1 and curr_idx < lowest_idx:
            lowest_idx = curr_idx
            value = val
    # We subtract the length of the line and 1 to get the true index of the last num
    high_idx = (len(line)-1-lowest_idx)
    return high_idx, value

if __name__ == "__main__":
    main()