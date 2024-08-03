"""
Advent of Code 2023
Day: 02
Problem: 01
Author: Nathan Rand
Date: 08.03.2024
"""
import regex as re

_COLOR_RE_PATTERNS = {
    "red": re.compile(r'(\d{1,2}) red'),
    "green": re.compile(r'(\d{1,2}) green'),
    "blue": re.compile(r'(\d{1,2}) blue'),
}
_COLOR_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def main():
    with open("input.txt", "r") as f:
        games = f.read().split("\n")

    possible_games = []
    for i in range(len(games)):
        if is_game_possible(games[i]):
            possible_games.append(i+1) # Add one cause game ids are 1-indexed

    print(f"The sum of the impossible game IDs is: {sum(possible_games)}")

def is_game_possible(game):
    rounds = game.split(";")
    for round in rounds:
        cube_counts = get_cube_counts_for_round(round)
        for color, count in cube_counts.items():
            if count > _COLOR_LIMITS[color]:
                return False
    return True

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