"""
Advent of Code 2024
Day: 12
Problem: 01
Author: Nathan Rand
Date: 12.13.24
"""
_INPUT_FILE_NAME = "example.txt"


def main():
    """Advent of Code - Day 12 - Part 01 [Garden Groups]"""
    # Read in our garden grid
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        garden_grid = f.read().split("\n")

    # Load it into our default dict struct
    garden = {}
    for row, garden_plots in enumerate(garden_grid):
        for col, plot in enumerate(garden_plots):
            garden[(row, col)] = plot

    # For each plot in our garden, perform a BFS to determine all regions
    visited_plots = set()
    regions = []
    for (row, col), plot in garden.items():
        print(plot)


if __name__ == "__main__":
    main()
