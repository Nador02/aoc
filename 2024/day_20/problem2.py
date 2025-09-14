"""
Advent of Code 2024
Day: 20
Problem: 02
Author: Nathan Rand
Date: 12.25.24
"""

_INPUT_FILE_NAME = "input.txt"
_WALL = "#"
_START = "S"
_END = "E"
_TRACK = "."
_NUM_TIME_SAVED_LIMIT = 100


def _get_surrounding_spaces(spot: tuple):
    """Get surrounding spaces in the racetrack map."""
    return [
        (spot[0] + 1, spot[1]),
        (spot[0] - 1, spot[1]),
        (spot[0], spot[1] + 1),
        (spot[0], spot[1] - 1),
    ]


def _get_cheat_positions_from_position(position: tuple, walls: set, track: set):
    """BFS around our given position to get all potential cheat locations
    within 6 picosends of range.
    """
    cheat_positions = set()
    visited_positions = set()
    neighboring_positions_queue = [(position, 0)]
    while neighboring_positions_queue:
        # Get our next position from the queue
        curr_position, picoseconds = neighboring_positions_queue.pop(0)

        # Define conditions for if we should skip over this point
        outside_racetrack = curr_position not in walls and curr_position not in track
        exceeding_cheat_time = picoseconds == 21
        already_visited = curr_position in visited_positions
        if outside_racetrack or exceeding_cheat_time or already_visited:
            continue

        # Otherwise add to visited and get its neighbors to add into the queue
        visited_positions.add(curr_position)

        # Only add our value to the cheat positions if it is a part of our track
        if curr_position in track and curr_position != position:
            cheat_positions.add(curr_position)

        # Add neighbors to the queue and increment our picoseconds
        neighboring_positions_queue.extend(
            [(neighbor, picoseconds+1)
             for neighbor in _get_surrounding_spaces(curr_position)]
        )

    return cheat_positions


def _get_manhattan_distance(position_1: tuple, position_2: tuple):
    """Get the manhattan (or taxicab) distance between 2 positions."""
    return abs(position_1[0]-position_2[0]) + abs(position_1[1]-position_2[1])


class RaceProgram():
    def __init__(self, initial_position: tuple, time: int = 0, visited: set = None, time_history: dict = None):
        """Define a race program that can traverse the racetrack map."""
        self.position = initial_position
        self.time = time
        self.visited = visited
        self.time_history = time_history

        # Define mutable defaults if no value is provided
        if self.visited is None:
            self.visited = {initial_position}

        if self.time_history is None:
            self.time_history = {self.position: self.time}

    def is_finished(self, end_position: tuple):
        """Check if this race program has finished or not."""
        return self.position == end_position

    def move(self, walls: set):
        """Move forward on the track."""
        # Get our next space on the track
        next_track_space = [
            neighbor for neighbor in _get_surrounding_spaces(self.position)
            if neighbor not in self.visited and neighbor not in walls
        ][0]

        # Update our RaceProgram attributes
        self.time += 1
        self.time_history[next_track_space] = self.time
        self.visited.add((tuple(list(next_track_space))))
        self.position = next_track_space


def main():
    """Advent of Code - Day 20 - Part 02 [Race Condition]"""
    # Read in our racetrack map
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        racetrack_map_str = f.read()

    # Sort each space in our racetrack map into its correct category
    walls = set()
    track = set()
    end = None
    race_program = None
    for i, racetrack_row_str in enumerate(racetrack_map_str.split("\n")):
        for j, space in enumerate(racetrack_row_str):
            if space == _WALL:
                walls.add((i, j))
            elif space == _TRACK:
                track.add((i, j))
            elif space == _END:
                end = (i, j)
                track.add((i, j))
            elif space == _START:
                race_program = RaceProgram((i, j))
                track.add((i, j))

    # March our main race program through the racetrack
    while not race_program.is_finished(end):
        race_program.move(walls)

    # Check all our positions to see if we can cheat at them, and how many
    # seconds it would save us
    cheats_saving_enough_time = 0
    for position, _ in sorted(race_program.time_history.items(), key=lambda item: item[1]):
        cheat_positions = _get_cheat_positions_from_position(
            position,
            race_program.time_history,
            walls,
            track
        )

        for cheat_position in cheat_positions:
            # Determine the manhattan (or taxicab) distance between
            # two points in our racetrack map
            manhattan_distance = _get_manhattan_distance(
                position,
                cheat_position
            )
            # Determine the amount of time we saved
            position_time = race_program.time_history[position]
            cheat_time = race_program.time_history[cheat_position]
            time_saved = cheat_time - position_time - manhattan_distance

            # If we saved enough time we add to our sum
            if time_saved >= _NUM_TIME_SAVED_LIMIT:
                cheats_saving_enough_time += 1

    # Output our result
    print(
        "The number of cheats that save the desired amount of time: "
        f"{_NUM_TIME_SAVED_LIMIT} based on the provided racetrack map is: "
        f"{cheats_saving_enough_time} cheats."
    )


if __name__ == "__main__":
    main()
