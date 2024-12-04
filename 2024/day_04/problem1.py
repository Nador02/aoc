"""
Advent of Code 2024
Day: 04
Problem: 01
Author: Nathan Rand
Date: 12.01.2024
"""
from typing import List


_INPUT_FILE_NAME = "input.txt"

_DIRECTIONS = [
    [0, -1],
    [0, 1],
    [-1, 0],
    [1, 0],
    [1, 1],
    [-1, 1],
    [1, -1],
    [-1, -1]
]

_XMAS_STR = "XMAS"


def _is_pos_outside_grid(word_search: List[List[str]], new_pos: tuple):
    return (
        new_pos[0] > len(word_search)-1 or new_pos[0] < 0
        or new_pos[1] > len(word_search[0])-1 or new_pos[1] < 0
    )

# RIP I accidentally wrote a more complicated solution that performs a full DFS


def get_neighboring_letter_positions(word_search: List[List[str]], curr: tuple, next_letter: str):
    """Get neighboring letter positions that are valid based on the assigned next letter
    and bounds of the word search in our 2D grid.

    [Extra Solution, Not Needed]
    """
    xmas_neighboring_positions = []
    for direction in _DIRECTIONS:
        neighbor_pos = (curr[0]+direction[0], curr[1]+direction[1])
        # If our neighbor is outside the word search grid, skip over it
        if _is_pos_outside_grid(word_search, neighbor_pos):
            continue

        # If our neighboring letter is our next one in "XMAS", add it to our list
        neighboring_letter = word_search[neighbor_pos[0]][neighbor_pos[1]]
        if neighboring_letter == next_letter:
            xmas_neighboring_positions.append(neighbor_pos)

    return xmas_neighboring_positions


def xmas_dfs(word_search: List[List[str]], x_indices: List[tuple]):
    """Perform DFS to find all valid XMAS strings from a given list of starting Xs
    Aw shit I solved this TOO good lol, we do not actually need a DFS with defined directions.

    [Extra Solution, Not Needed]
    """
    letter_pos_stack = x_indices
    xmas_counter = 0
    while letter_pos_stack:
        curr_pos = letter_pos_stack.pop(0)
        curr_letter = word_search[curr_pos[0]][curr_pos[1]]

        if curr_letter == "S":
            xmas_counter += 1
            continue

        next_letter = _XMAS_STR[_XMAS_STR.index(curr_letter)+1]
        letter_pos_stack.extend(
            get_neighboring_letter_positions(word_search, curr_pos, next_letter)
        )

    return xmas_counter

# Actual solution


def get_xmas_count_for_starting_x(word_search: List[List[str]], x_pos: tuple):
    """Check in all 8 directions from a given X for matching XMAS strings"""
    xmas_counter = 0
    for direction in _DIRECTIONS:
        # Check if we will fall outside the grid, if so, skip this direction
        word_end_pos = (x_pos[0]+direction[0]*3, x_pos[1]+direction[1]*3)
        if _is_pos_outside_grid(word_search, word_end_pos):
            continue

        word_in_direction = "".join([
            word_search[x_pos[0]+direction[0]*i][x_pos[1]+direction[1]*i] for i in range(1, 4)
        ])
        xmas_counter += 1 if word_in_direction == _XMAS_STR[1:] else 0

    return xmas_counter


def main():
    """Advent of Code - Day 04 - Part 01 [Ceres Search]"""
    # Read in our word search as a 2D numpy array
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        word_search = [list(line) for line in f.read().split("\n")]

    # Find where all of our x values in the word search (starting positions)
    x_indices = [
        (i, j) for i, line in enumerate(word_search)
        for j, letter in enumerate(line) if letter == "X"
    ]

    # For each starting X, perform a DFS to find all matching paths to "XMAS"
    total_xmas_found = 0
    for x_pos in x_indices:
        total_xmas_found += get_xmas_count_for_starting_x(word_search, x_pos)

    print(f"Total \"XMAS\" matches found in word search: {total_xmas_found}")
    print(f"My wild Graph DFS all directions \"XMAS\" count: {xmas_dfs(word_search, x_indices)}")


if __name__ == "__main__":
    main()
