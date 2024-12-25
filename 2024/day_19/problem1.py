"""
Advent of Code 2024
Day: 19
Problem: 01
Author: Nathan Rand
Date: 12.24.24
"""
from functools import cache
_INPUT_FILE_NAME = "input.txt"


def is_design_possible_with_towels_cache_wrapper(towels: set, longest_towel_length: int):
    """Wrapper for our cache function do allow us to provide towels set (non-hashable and
    constant) to our caching recursive function."""

    @cache
    def is_design_possible_with_towels(design: str):
        """Determine if a design is possible with the given set of towels."""
        # Base case for if we get to a point where our design is completable
        # by a single towel
        if design in towels:
            return True

        # Otherwise get all branching nodes for connected designs
        possible_designs = []
        for i in range(1, longest_towel_length+1):
            if design[:i] in towels:
                possible_designs.append(design[i:])

        # And recursively check if any of them can be completed by our towels
        return any([
            is_design_possible_with_towels(design)
            for design in possible_designs
        ])

    return is_design_possible_with_towels


def main():
    """Advent of Code - Day 19 - Part 01 [Linen Layout]"""
    # Read in our towels and designs input file
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        towels_str, designs_str = f.read().split("\n\n")

    # Process our input strings into towels and designs
    towels = set(towels_str.split(", "))
    designs = designs_str.split("\n")
    longest_towel_length = max([len(towel) for towel in towels])

    # Get our cache wrapped recursive function for determining valid designs
    is_design_possible_with_towels_func = is_design_possible_with_towels_cache_wrapper(
        towels,
        longest_towel_length
    )

    # Determine if each design is possible
    possible_designs = 0
    for design in designs:
        if is_design_possible_with_towels_func(design):
            possible_designs += 1

    # Output our result
    print(
        "The number of designs that are possible based on "
        f"the infinite towels we have is: {possible_designs}"
    )


if __name__ == "__main__":
    main()
