"""
Advent of Code 2024
Day: 01
Problem: 02
Author: Nathan Rand
Date: 12.01.2024
"""
import numpy as np

_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 01 - Part 02 [Historian Hysteria]"""
    # Load in our input file using numpy to get a list of our position lists
    pos_list1, pos_list2 = np.loadtxt(_INPUT_FILE_NAME).T.tolist()

    # Create a frequency dict to define how many time each number appears in list 2
    pos_list2_freq_dict = {}
    for position in pos_list2:
        if position in pos_list2_freq_dict:
            pos_list2_freq_dict[position] += 1
        else:
            pos_list2_freq_dict[position] = 1

    # Determine our similarity score accordingly
    similarity_score = 0
    for position in pos_list1:
        if position in pos_list2_freq_dict:
            similarity_score += pos_list2_freq_dict[position]*position

    # Output our results
    print(
        f"The similarity score between our two lists is: {int(similarity_score)}")


if __name__ == "__main__":
    main()
