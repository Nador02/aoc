"""
Advent of Code 2024
Day: 18
Problem: 01
Author: Nathan Rand
Date: 12.21.24
"""
import heapq

_INPUT_FILE_NAME = "input.txt"
_NUM_BYTES_FALLEN = 1024
_MEMORY_BOUNDS = [0, 70]
_END = (_MEMORY_BOUNDS[1], _MEMORY_BOUNDS[1])


def _get_neighboring_spaces(spot: tuple, bytes: set):
    potential_neighbors = [
        (spot[0] + 1, spot[1]),
        (spot[0] - 1, spot[1]),
        (spot[0], spot[1] + 1),
        (spot[0], spot[1] - 1),
    ]

    return [
        neighbor for neighbor in potential_neighbors
        if _is_spot_in_memory_space(neighbor) and neighbor not in bytes
    ]


def _is_spot_in_memory_space(spot: tuple):
    return (
        spot[0] >= _MEMORY_BOUNDS[0] and
        spot[0] <= _MEMORY_BOUNDS[1] and
        spot[1] >= _MEMORY_BOUNDS[0] and
        spot[1] <= _MEMORY_BOUNDS[1]
    )


class HistorianSearchParty():
    def __init__(self, initial_position: tuple, steps_taken: int = 0):
        """Creates a Historian Search Party to traverse the North Pole
        Computer's Memory Space and escape!
        """
        self.position = initial_position
        self.steps_taken = steps_taken

    def __lt__(self, other):
        """Allows for heap comparison of two search parties."""
        return self.steps_taken < other.steps_taken

    def copy(self):
        """Create a deep copy of this search party (to search in a different
        direction for the exit).
        """
        return HistorianSearchParty(
            # This copies the pos tuple so we don't mutate it
            tuple(list(self.position)),
            self.steps_taken
        )

    def move(self, new_position: tuple):
        """Move this search party to a new space."""
        self.steps_taken += 1
        self.position = (new_position[0], new_position[1])


def main():
    """Advent of Code - Day 18 - Part 01 [RAM Run]"""
    # Read in our falling bytes file and grab only those that have fallen
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        bytes = set([
            tuple([int(pos) for pos in byte_str.split(",")])
            for byte_str in f.read().split("\n")
        ][:_NUM_BYTES_FALLEN])

    starting_historian_search_party = HistorianSearchParty((0, 0))
    historian_heap = [starting_historian_search_party]
    visited_memory_spaces = {(0, 0): 0}
    fastest_search_party = None
    while historian_heap:
        # Get the current fastest historian search party (min steps taken)
        curr_search_party = heapq.heappop(historian_heap)

        # Get all their possible next move spots
        next_move_spots = _get_neighboring_spaces(
            curr_search_party.position, bytes
        )

        # Check if any of our next spots are the end, if so, this
        # party after moving their has done it the fastest!
        if _END in next_move_spots:
            curr_search_party.move(_END)
            fastest_search_party = curr_search_party
            break

        for move_spot in next_move_spots:
            # A next move for a historian party is only valid if we have
            #    1. Never been to this space before
            #    2. Been to the space before but we are getting to it now with less steps
            # NOTE: not sure if 2 is ever hit cause of Djikstra's but meh...
            is_valid_next_move = (
                move_spot not in visited_memory_spaces
                or visited_memory_spaces[move_spot] > curr_search_party.steps_taken+1
            )
            if is_valid_next_move:
                # Add this space and steps taken to our visited dict
                visited_memory_spaces[move_spot] = curr_search_party.steps_taken+1

                # Create a copy of our party to branch off and take this next step
                ghost_historian_search_party = curr_search_party.copy()
                ghost_historian_search_party.move(move_spot)

                # Finally, add that copied new ghost party to our heap
                heapq.heappush(historian_heap, ghost_historian_search_party)

    # Output our result
    print(
        "The historian search party that found the exit "
        "first (with shortest number of steps) did it in: "
        f"{fastest_search_party.steps_taken} steps"
    )


if __name__ == "__main__":
    main()
