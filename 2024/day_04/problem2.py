"""
Advent of Code 2024
Day: 04
Problem: 02
Author: Nathan Rand
Date: 12.04.2024
"""
from typing import List


_INPUT_FILE_NAME = "input.txt"


def _is_pos_outside_grid(word_search: List[List[str]], new_pos: tuple):
    return (
        new_pos[0] > len(word_search)-1 or new_pos[0] < 0
        or new_pos[1] > len(word_search[0])-1 or new_pos[1] < 0
    )


def _check_for_mas_diagonal(word_search: List[List[str]], a_pos: tuple, positive_slope: bool = True):
    slope = 1 if positive_slope else -1
    end_positions = [(a_pos[0] + -1*slope, a_pos[1]-1),
                     (a_pos[0] + 1*slope, a_pos[1] + 1)]
    if any(_is_pos_outside_grid(word_search, pos) for pos in end_positions):
        return False

    return {word_search[pos[0]][pos[1]] for pos in end_positions} == {"M", "S"}


def main():
    """Advent of Code - Day 04 - Part 02 [Ceres Search]"""
    # Read in our word search as a 2D numpy array
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        word_search = [list(line) for line in f.read().split("\n")]

    # Find where all of our x values in the word search (starting positions)
    a_indices = [
        (i, j) for i, line in enumerate(word_search)
        for j, letter in enumerate(line) if letter == "A"
    ]

    # For each starting X, perform a DFS to find all matching paths to "XMAS"
    total_xmas_found = 0
    for a_pos in a_indices:
        valid_x_mas = (
            _check_for_mas_diagonal(word_search, a_pos, positive_slope=True) and
            _check_for_mas_diagonal(word_search, a_pos, positive_slope=False)
        )
        total_xmas_found += 1 if valid_x_mas else 0

    print(f"Total \"X-MAS\" matches found in word search: {total_xmas_found}")


if __name__ == "__main__":
    main()
