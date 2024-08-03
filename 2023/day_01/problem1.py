"""
Advent of Code 2023
Day: 01
Problem: 01
Author: Nathan Rand
Date: 08.02.2024
"""
def main():
    sum = 0
    with open("input.txt", "r") as f:
        for line in f:
            sum += find_first_num(line)+find_last_num(line)
    print(f"The Sum of All of the Calibration Values for the Trebuchet is: {sum}")
    
def find_first_num(line):
    # Find the first num in the line
    for char in line:
        if char.isnumeric():
            return int(char)*10
    
def find_last_num(line):
    # Find the last num in the line
    for char in line[::-1]:
        if char.isnumeric():
            return int(char)

if __name__ == "__main__":
    main()