"""
Advent of Code 2024
Day: 11
Problem: 01
Author: Nathan Rand
Date: 12.11.24
"""

_INPUT_FILE_NAME = "input.txt"
_NUM_BLINKS = 25


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


def main():
    """Advent of Code - Day 11 - Part 01 [Plutonian Pebbles]"""
    # Read in our pebbles
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        pebbles = [int(pebble) for pebble in f.read().split()]

    # Blink 25 times, each time updating our pebbles based on the defined rules
    for _ in range(_NUM_BLINKS):
        pebbles_after_blinking = []
        for pebble in pebbles:
            pebbles_after_blinking.extend(_get_pebble_after_blinking(pebble))

        pebbles = pebbles_after_blinking

    # Print the resulting number of pebbles after blinking 25 times
    print(
        f"After {_NUM_BLINKS} blinks the number of pebbles is: {len(pebbles)}"
    )


if __name__ == "__main__":
    main()
