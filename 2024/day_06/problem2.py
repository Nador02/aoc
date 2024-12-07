"""
Advent of Code 2024
Day: 06
Problem: 01
Author: Nathan Rand
Date: 12.06.2024
"""
from typing import List
_INPUT_FILE_NAME = "input.txt"
_OBSTACLE = r"#"
_GUARD = "^"


def _is_guard_in_map(lab_map: List[str], guard_pos: tuple):
    return (
        guard_pos[0] >= 0 and guard_pos[0] < len(lab_map)
        and guard_pos[1] >= 0 and guard_pos[1] < len(lab_map[0])
    )


def main():
    """Advent of Code - Day 06 - Part 02 [Guard Gallivant]"""
    # Read in our input file (the suit factory lab map)
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        lab_map = f.read().split("\n")

    # Find our guard's starting position
    guard_pos = None
    step = (-1, 0)
    # TODO: use like unit circle or something for this idfk
    next_step = {
        (0, -1): (-1, 0),
        (1, 0): (0, -1),
        (0, 1): (1, 0),
        (-1, 0): (0, 1)
    }
    for i, row in enumerate(lab_map):
        if _GUARD in row:
            guard_pos = (i, row.find(_GUARD))
            break

    # Move our guard through the lab till he leaves, counting his steps
    # while he bumps into obstacles and turns right over and over
    cycle_obstructions = 0
    visited = {guard_pos: [step]}
    while True:
        # Look at the guards next position after taking a step
        guard_next_pos = (guard_pos[0]+step[0], guard_pos[1]+step[1])
        if not _is_guard_in_map(lab_map, guard_next_pos):
            break

        # If this is an obstacle, turn ourselves to the right
        if lab_map[guard_next_pos[0]][guard_next_pos[1]] == _OBSTACLE:
            step = next_step[step]
            guard_next_pos = (guard_pos[0]+step[0], guard_pos[1]+step[1])

        # If this is a unique spot, add it to our set
        if guard_next_pos not in visited:
            visited[guard_next_pos] = [step]

        # Look right and see if we can see a previous path unobstructed
        look_pos = guard_next_pos
        look_dir = next_step[step]
        while True:
            look_next_pos = (look_pos[0] + look_dir[0], look_pos[1] + look_dir[1])
            if not _is_guard_in_map(lab_map, look_next_pos) or lab_map[look_next_pos[0]][look_next_pos[1]] == _OBSTACLE:
                break

            if look_next_pos in visited and look_dir in visited[look_next_pos]:
                cycle_obstructions += 1
                break

            look_pos = look_next_pos

        if step not in visited[guard_next_pos]:
            visited[guard_next_pos].append(step)

        # Take our step
        guard_pos = guard_next_pos

    # Output our result
    print(
        "Number of potential obstructions we can add to create "
        f"cycles: {cycle_obstructions} obstructions."
    )


if __name__ == "__main__":
    main()
