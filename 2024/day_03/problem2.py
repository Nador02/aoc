"""
Advent of Code 2024
Day: 03
Problem: 02
Author: Nathan Rand
Date: 12.03.2024
"""
import re
import numpy as np
_INPUT_FILE_NAME = "input.txt"
_DO = "do()"
_DONT = "don't()"


def _more_concise_active_mem(corrupted_memory: str):
    """More concise method for getting the active memory based on stuff
    I realized after looking at some solutions on Reddit. Using `split()`
    is significantly faster for this task and creates a much more elegant
    solution compared to my original.
    """
    return "".join([
        interval[interval.index(_DO):]
        for interval in (_DO + corrupted_memory).split(_DONT)
        if _DO in interval
    ])


def main():
    """Advent of Code - Day 03 - Part 02 [Mull It Over]"""
    # Read in our corrupted memory data
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        corrupted_memory = f.read()

    # Find all indices of dos and don'ts
    do_start_indices = [do_match.start()
                        for do_match in re.finditer(r"do\(\)", corrupted_memory)]
    dont_start_indices = [dont_match.start()
                          for dont_match in re.finditer(r"don't\(\)", corrupted_memory)]

    # Determine inactive intervals based on this
    inactive_intervals = []
    for dont_start_idx in dont_start_indices:
        # If we hit a don't that is between our previous don't -> do inactive interval
        # then simply continue as this is a sub-interval
        if inactive_intervals and dont_start_idx < inactive_intervals[-1][1]:
            continue

        # Determine the idx of our next do and if it is behind our current don't
        # break out early cause everything left in memory is inactive
        next_do_idx = do_start_indices[np.argmax(
            np.array(do_start_indices) > dont_start_idx)]

        if dont_start_idx > next_do_idx:
            break

        # Otherwise, add the inactive interval to our list (between this don't and the next do)
        inactive_intervals.append([dont_start_idx, next_do_idx])

    # Trim our corrupted memory to only active mult instructions
    active_corrupted_memory = corrupted_memory[0:inactive_intervals[0][0]]
    for i in range(len(inactive_intervals)-1):
        active_corrupted_memory += corrupted_memory[inactive_intervals[i]
                                                    [1]:inactive_intervals[i+1][0]]
    active_corrupted_memory += corrupted_memory[inactive_intervals[-1][1]:-1]

    # More concise method based on solutions and realizations from Reddit Solutions
    # active_corrupted_memory = _more_concise_active_mem(corrupted_memory)

    # Get all matches for our given regex pattern
    matches = re.findall(
        r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", active_corrupted_memory)

    # Sum the matching multiplication instructions
    mul_instructions_sum = 0
    for match in matches:
        mul_instructions_sum += int(match[0])*int(match[1])

    # Output our result
    print(
        "The sum of all valid multiplication instructions in the "
        f"active corrupted memory is: {mul_instructions_sum}"
    )


if __name__ == "__main__":
    main()
