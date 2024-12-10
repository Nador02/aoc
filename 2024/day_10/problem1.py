"""
Advent of Code 2024
Day: 10
Problem: 02
Author: Nathan Rand
Date: 12.10.24
"""
from collections import defaultdict


_INPUT_FILE_NAME = "input.txt"
_OVERLOOK_HEIGHT = 9


def _get_neighboring_trail_spaces(topographic_dict: defaultdict, trail_pos: tuple):
    # Define our potential neighboring spaces (indifferent to height)
    potential_neighbors = [
        (trail_pos[0]-1, trail_pos[1]),
        (trail_pos[0]+1, trail_pos[1]),
        (trail_pos[0], trail_pos[1]-1),
        (trail_pos[0], trail_pos[1]+1),
    ]

    # Return the filtered version of our neighbors based on if their height is +1 our current
    return [
        neighbor for neighbor in potential_neighbors
        if topographic_dict[neighbor] - topographic_dict[trail_pos] == 1
    ]


def main():
    """Advent of Code - Day 10 - Part 02 [Hoof It]"""
    # Read in our topographic map of the hiking area
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        topographic_map = f.read()

    # Process our topographic_map into a dict structure for easier access
    topographic_dict = defaultdict(lambda: float('inf'))
    trailheads = set()
    for row, map_row_str in enumerate(topographic_map.split("\n")):
        for col, height in enumerate(map_row_str):
            topographic_dict[(row, col)] = int(height)
            if int(height) == 0:
                trailheads.add((row, col))

    overlooks_reached = defaultdict(list)
    # NOTE: we can probably use memoization here somehow, need to add
    for trailhead in trailheads:
        trail_stack = [trailhead]
        while trail_stack:
            # Grab the next trail position from our stack
            # and determine its height
            trail_pos = trail_stack.pop()
            height = topographic_dict[trail_pos]

            # If we are at a unique overlook add it to our reach dict and continue
            if height == _OVERLOOK_HEIGHT and trail_pos not in overlooks_reached[trailhead]:
                overlooks_reached[trailhead].append(trail_pos)
                continue

            # Otherwise get valid neighboring spaces and continue marching through
            # the topographic graph
            trail_stack.extend(_get_neighboring_trail_spaces(
                topographic_dict,
                trail_pos
            ))

    # Output our result
    total_trailhead_score = sum([
        len(overlooks)
        for overlooks in overlooks_reached.values()
    ])
    print(
        "The total score of all trailheads in the provided topographic "
        f"map is: {total_trailhead_score}"
    )


if __name__ == "__main__":
    main()
