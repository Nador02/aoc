"""
Advent of Code 2024
Day: 06
Problem: 02
Author: Nathan Rand
Date: 12.06.2024
"""
from copy import deepcopy
from typing import List
_INPUT_FILE_NAME = "input.txt"
_OBSTACLE = r"#"
_GUARD = "^"

_TURN_RIGHT = {
    (0, -1): (-1, 0),
    (1, 0): (0, -1),
    (0, 1): (1, 0),
    (-1, 0): (0, 1)
}


def _is_position_in_map(lab_map: List[str], guard_pos: tuple):
    return (
        guard_pos[0] >= 0 and guard_pos[0] < len(lab_map)
        and guard_pos[1] >= 0 and guard_pos[1] < len(lab_map[0])
    )


def _space_in_front(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def _obstacle_on_space(lab_map, position):
    return lab_map[position[0]][position[1]] == _OBSTACLE


def _check_if_cycle(
        lab_map,
        visited,
        guard_pos,
        direction,
        cycle_obstruction
):
    while _is_position_in_map(lab_map, _space_in_front(guard_pos, direction)):
        # If this is an obstacle, turn ourselves to the right (and keep turning
        # to the right till we are no longer moving into an obstacle)
        guard_next_pos = _space_in_front(guard_pos, direction)
        while _obstacle_on_space(lab_map, guard_next_pos) or guard_next_pos == cycle_obstruction:
            direction = _TURN_RIGHT[direction]
            guard_next_pos = _space_in_front(guard_pos, direction)

        # If this is a unique spot, add it to our set
        if guard_next_pos not in visited:
            visited[guard_next_pos] = [direction]
        else:
            if direction in visited[guard_next_pos]:
                return True
            else:
                visited[guard_next_pos].append(direction)

        # Take our step
        guard_pos = guard_next_pos

    return False


def main():
    """Advent of Code - Day 06 - Part 02 [Guard Gallivant]"""
    # Read in our input file (the suit factory lab map)
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        lab_map = f.read().split("\n")

    # Find our guard's starting position
    guard_pos = None
    direction = (-1, 0)
    for i, row in enumerate(lab_map):
        if _GUARD in row:
            guard_pos = (i, row.find(_GUARD))
            break

    # Move our guard through the lab till he leaves, counting his steps
    # while he bumps into obstacles and turns right over and over
    visited = {guard_pos: [direction]}
    cycle_obstructions = set()
    while _is_position_in_map(lab_map, _space_in_front(guard_pos, direction)):
        # If this is an obstacle, turn ourselves to the right (and keep turning
        # to the right till we are no longer moving into an obstacle)
        guard_next_pos = _space_in_front(guard_pos, direction)
        while _obstacle_on_space(lab_map, guard_next_pos):
            direction = _TURN_RIGHT[direction]
            guard_next_pos = _space_in_front(guard_pos, direction)

        # If we have a valid obstruction, check if it induces a cycle
        if (guard_next_pos not in visited and _check_if_cycle(
            lab_map,
            deepcopy(visited),
            guard_pos,
            _TURN_RIGHT[direction],
            guard_next_pos
        )):
            cycle_obstructions.add(guard_next_pos)

        # If this is a new spot, add it and our current facing direction to our dict
        if guard_next_pos not in visited:
            visited[guard_next_pos] = [direction]
        # Otherwise, check if this direction is in our visited, if not, add it
        elif direction not in visited[guard_next_pos]:
            visited[guard_next_pos].append(direction)
        # If we hit this we are fucked, we have our main guard in a cycle
        else:
            raise ValueError(
                "Uh your main guard is in a cycle? "
                "Your CPU may set on fire soon... 🔥"
            )

        # Take our step
        guard_pos = guard_next_pos

    # Output our result
    print(
        f"Number of potential cycle inducing obstructions: {len(cycle_obstructions)}"
    )


if __name__ == "__main__":
    main()
