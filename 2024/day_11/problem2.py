"""
Advent of Code 2024
Day: 11
Problem: 02
Author: Nathan Rand
Date: 12.11.24
"""
from functools import cache
_INPUT_FILE_NAME = "input.txt"
_NUM_BLINKS = 75


@cache
def _get_pebble_after_blinking(pebble: int):
    # Edge case when pebble is 0
    if pebble == 0:
        return [1]

    # If it is not 0, we check if it has an even number of digits
    # through string comparison, if it does, we split in half and return
    pebble_str = str(pebble)
    if len(pebble_str) % 2 == 0:
        mid = int(len(pebble_str)/2)
        return [int(pebble_str[:mid]), int(pebble_str[mid:])]

    # Otherwise, if it has an odd number of digits, we return it multiplied by 2024
    return [pebble*2024]


@cache
def _get_num_pebbles_after_n_blinks(pebble: int, blinks: int):
    # If we have no more blinks to perform, just return 1 for this single pebble
    if blinks == 0:
        return 1

    # Otherwise, blink and return the num of pebbles after we do (N-1) more blinks
    return sum([
        _get_num_pebbles_after_n_blinks(new_pebble, blinks-1)
        for new_pebble in _get_pebble_after_blinking(pebble)
    ])


def main():
    """Advent of Code - Day 11 - Part 02 [Plutonian Pebbles]"""
    # Read in our pebbles
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        pebbles = [int(pebble) for pebble in f.read().split()]

    # Compute the number of pebbles after 75 blinks for each pebble in our starting group
    num_pebbles_after_all_blinks = 0
    for pebble in pebbles:
        num_pebbles_after_all_blinks += _get_num_pebbles_after_n_blinks(pebble, _NUM_BLINKS)

    # Print the resulting number of pebbles after blinking 75 times
    print(
        f"After {_NUM_BLINKS} blinks the number of pebbles is: {num_pebbles_after_all_blinks}"
    )


if __name__ == "__main__":
    main()
