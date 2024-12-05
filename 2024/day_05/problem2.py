"""
Advent of Code 2024
Day: 05
Problem: 02
Author: Nathan Rand
Date: 12.05.2024
"""
from collections import defaultdict
from typing import List
_INPUT_FILE_NAME = "input.txt"


class EqualPagesError(Exception):
    """Exception for when we find 2 equal pages. This is bad cause
    then we have multiple potential orders which can give non-deterministic
    results to the problem. Assuming this won't be triggered in the correct run.
    """

    pass


def compare_pages(page1: int, page2: int, rules: defaultdict):
    """Compares 2 pages

    Returns
    -------
    bool
        True if page1 > page 2, and False if page1 < page2.
        Raises an exception if page1 == page2.
    """
    if page1 in rules[page2]:
        return True
    elif page2 in rules[page1]:
        return False
    else:
        raise EqualPagesError(
            f"Uhoh page1 [{page1}] and page2[{page2}] appear to be equal..."
        )


def correct_update(update: List[int], rules: defaultdict):
    """Creates a new sorted (corrected) form of the provided update."""
    # TODO: can probably do this better by applying like quicksort,
    # can try later if I have the time but this works so meh
    corrected_update = []
    for page_to_sort in update:
        if not corrected_update:
            corrected_update.append(page_to_sort)
            continue

        found_spot = False
        for i, sorted_page in enumerate(corrected_update):
            if compare_pages(page_to_sort, sorted_page, rules):
                found_spot = True
                corrected_update.insert(i, page_to_sort)
                break

        if not found_spot:
            corrected_update.append(page_to_sort)

    return corrected_update


def main():
    """Advent of Code - Day 05 - Part 02 [Print Queue]"""
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
    # We now want to store the incorrect updates
    incorret_updates = []
    for update in updates:
        ruled_out_set = set()
        for page in update:
            # If we have an incorrect update, store it for correcting
            if page in ruled_out_set:
                incorret_updates.append(update)
                break

            ruled_out_set.update(rules[page])

    # Correct our updates and grab the middle pages once sorted
    corrected_updates_mid_page_sum = 0
    for update in incorret_updates:
        # Correct our update by sorting it based on the rules
        corrected_update = correct_update(update, rules)

        # Grab the middle element from our corrected update and add to the sum
        middle_page = corrected_update[int(len(corrected_update) // 2)]
        corrected_updates_mid_page_sum += middle_page

    # Output our resulting sum
    print(
        "Sum of middle page #s for all "
        f"correctly-ordered updates: {corrected_updates_mid_page_sum}"
    )


if __name__ == "__main__":
    main()
