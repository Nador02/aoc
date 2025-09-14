"""
Advent of Code 2024
Day: 20
Problem: 01
Author: Nathan Rand
Date: 12.24.24
"""

_INPUT_FILE_NAME = "input.txt"
_WALL = "#"
_START = "S"
_END = "E"
_TRACK = "."
_NUM_TIME_SAVED_LIMIT = 100


def _get_surrounding_spaces(spot: tuple):
    return [
        (spot[0] + 1, spot[1]),
        (spot[0] - 1, spot[1]),
        (spot[0], spot[1] + 1),
        (spot[0], spot[1] - 1),
    ]


def _get_cheat_positions_from_position(position: tuple, time_history: dict, walls: set, track: set):
    cheat_positions = set()
    for neighbor in _get_surrounding_spaces(position):
        if neighbor not in walls:
            continue

        neighbor_neighbors = _get_surrounding_spaces(neighbor)
        for neighbor_neighbor in neighbor_neighbors:
            if neighbor_neighbor == position:
                continue

            if neighbor_neighbor in time_history:
                cheat_positions.add(neighbor_neighbor)

    return cheat_positions


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
    """Advent of Code - Day 20 - Part 01 [Race Condition]"""
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
            elif space == _START:
                race_program = RaceProgram((i, j))

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
            # Cursed formatting
            time_saved = (
                race_program.time_history[cheat_position]
                # Bruh wtf is this -2
                - race_program.time_history[position] - 2
            )
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
