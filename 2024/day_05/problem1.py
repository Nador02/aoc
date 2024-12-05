"""
Advent of Code 2024
Day: 05
Problem: 01
Author: Nathan Rand
Date: 12.05.2024
"""
from collections import defaultdict
_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 05 - Part 01 [Print Queue]"""
    # Read in our rules and updates strings from the input file
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        rules_str, updates_str = f.read().split("\n\n")
        updates = [[int(num) for num in line.split(",")]
                   for line in updates_str.split("\n")]

    # Create our rules default dict
    rules = defaultdict(set)
    for rule_str in rules_str.split("\n"):
        left, right = rule_str.split("|")
        rules[int(right)].add(int(left))

    # Go through each update determining if it is correctly ordered or not
    valid_mid_sum = 0
    for update in updates:
        invalide_update = False
        ruled_out_set = set()
        for page in update:
            # If our page is not allowed to be after a previous element,
            # break out here and mark this update as invalid
            if page in ruled_out_set:
                invalide_update = True
                break

            # Otherwise expand our set of pages that cannot appear in the future for this update
            ruled_out_set.update(rules[page])

        # If this is an invalid update, just continue
        if invalide_update:
            continue
        valid_mid_sum += update[int(len(update)//2)]

    # Output our resulting sum
    print(
        "Sum of middle page #s for all "
        f"correctly-ordered updates: {valid_mid_sum}"
    )


if __name__ == "__main__":
    main()
