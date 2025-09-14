"""
Advent of Code 2024
Day: 19
Problem: 02
Author: Nathan Rand
Date: 12.24.24
"""
from functools import cache
_INPUT_FILE_NAME = "input.txt"


def num_possible_towel_combos_cache_wrapper(towels: set, longest_towel_length: int):
    """Wrapper for our cache function do allow us to provide towels set (non-hashable and
    constant) to our caching recursive function."""

    @cache
    def num_possible_towel_combos(design: str):
        """Determine the number of possible towel combos"""
        # If we get to a point where our design is completable
        # by a single towel (and we can add 1 automatically)
        design_completed_increment = 1 if design in towels else 0

        # Otherwise get all branching nodes for connected designs
        possible_designs = []
        for i in range(1, longest_towel_length+1):
            if design[:i] in towels:
                possible_designs.append(design[i:])

        # Base case if we have no other possible designs
        if len(possible_designs) == 0:
            return design_completed_increment

        # And recursively check if any of them can be completed by our towels
        return design_completed_increment + sum([
            num_possible_towel_combos(design)
            for design in possible_designs
        ])

    return num_possible_towel_combos


def main():
    """Advent of Code - Day 19 - Part 02 [Linen Layout]"""
    # Read in our towels and designs input file
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        towels_str, designs_str = f.read().split("\n\n")

    # Process our input strings into towels and designs
    towels = set(towels_str.split(", "))
    designs = designs_str.split("\n")
    longest_towel_length = max([len(towel) for towel in towels])

    # Get our cache wrapped recursive function for determining valid designs
    num_possible_towel_combos_func = num_possible_towel_combos_cache_wrapper(
        towels,
        longest_towel_length
    )

    # Determine if each design is possible
    possible_designs = 0
    for design in designs:
        possible_designs += num_possible_towel_combos_func(design)

    # Output our result
    print(
        "The number of possible design combos based on "
        f"the infinite towels we have is: {possible_designs}"
    )


if __name__ == "__main__":
    main()
