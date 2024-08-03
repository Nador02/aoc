"""
Advent of Code 2023
Day: 02
Problem: 01
Author: Nathan Rand
Date: 08.03.2024
"""
import regex as re
import numpy as np

_COLOR_RE_PATTERNS = {
    "red": re.compile(r'(\d{1,2}) red'),
    "green": re.compile(r'(\d{1,2}) green'),
    "blue": re.compile(r'(\d{1,2}) blue'),
}

def main():
    with open("input.txt", "r") as f:
        games = f.read().split("\n")

    overall_power = 0
    for i in range(len(games)):
        overall_power += get_game_power(games[i])

    print(f"The sum of all game's power: {overall_power}")


def get_game_power(game):
    rounds = game.split(";")
    min_needed_cube_counts = {
        "red": 0,
        "blue": 0,
        "green": 0,
    }
    for round in rounds:
        cube_counts = get_cube_counts_for_round(round)
        for color, count in cube_counts.items():
            if count > min_needed_cube_counts[color]:
                min_needed_cube_counts[color] = count
    return np.prod([min_needed for _, min_needed in min_needed_cube_counts.items()])

def get_cube_counts_for_round(round):
    cube_counts = {}
    for color, pattern in _COLOR_RE_PATTERNS.items():
        search_result = pattern.search(round)
        if search_result is None:
            continue

        cube_counts[color] = int(search_result.groups()[0])
    return cube_counts

        
if __name__ == "__main__":
    main()