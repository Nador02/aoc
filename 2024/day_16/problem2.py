"""
Advent of Code 2024
Day: 16
Problem: 02
Author: Nathan Rand
Date: 12.16.24
"""

from enum import Enum
import heapq


_INPUT_FILE_NAME = "input.txt"
_WALL = "#"
_START = "S"
_END = "E"


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


_TURN_CLOCKWISE = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

_TURN_COUNTER_CLOCKWISE = {
    start: end for end, start in _TURN_CLOCKWISE.items()
}

_DIRECTION_TO_MOVEMENT = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1)
}


class Reindeer():
    def __init__(self, initial_position: tuple, direction: Direction, initial_score: int = 0, visited: set = None):
        """Create a Reindeer that will compete in the Reindeer Olympics Maze Competition."""
        self.position = initial_position
        self.direction = direction
        self.score = initial_score
        self.visited = {initial_position} if visited is None else visited

    def __lt__(self, other):
        """Helper functionality so we can put our reindeer into a heap?"""
        return self.score < other.score

    def copy(self):
        """Make a copy of the current reindeer."""
        return Reindeer(
            tuple(list(self.position)),  # This performs a copy of a tuple
            self.direction,
            self.score,
            set(self.visited)
        )

    def directions_can_move(self, walls: set):
        """Returns the directions that the reindeer can move in its next step."""
        potential_directions = [
            self.direction,
            _TURN_CLOCKWISE[self.direction],
            _TURN_COUNTER_CLOCKWISE[self.direction]
        ]
        movable_directions = []
        for direction in potential_directions:
            next_potential_space = (
                self.position[0] + _DIRECTION_TO_MOVEMENT[direction][0],
                self.position[1] + _DIRECTION_TO_MOVEMENT[direction][1],
            )
            if next_potential_space not in walls:
                movable_directions.append(direction)

        return movable_directions

    def turn(self, direction: Direction):
        """Turn this reindeer"""
        self.score += 1000
        self.direction = direction

    def move(self):
        """Move this reindeer in the direction it is currently facing."""
        self.score += 1
        self.position = (
            self.position[0] + _DIRECTION_TO_MOVEMENT[self.direction][0],
            self.position[1] + _DIRECTION_TO_MOVEMENT[self.direction][1],
        )
        self.visited.add(self.position)


def main():
    """Advent of Code - Day 16 - Part 02 [Reindeer Maze]"""
    # Read in our maze
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        maze = f.read().split("\n")

    # Process our maze into a dictionary as well as grabbing our starting
    # and ending positions
    walls = set()
    end = None
    starting_reindeer = None
    for row, maze_row_str in enumerate(maze):
        for col, space in enumerate(maze_row_str):
            if space == _WALL:
                walls.add((row, col))
            elif space == _START:
                starting_reindeer = Reindeer((row, col), Direction.EAST)
            elif space == _END:
                end = (row, col)

    # Perform some bootleg form of Djikstra's algorithm to find the reindeer
    # which can finish the maze the fasted (by continuously advancing the ones with
    # the lowest score until one reaches the end).
    reindeer_heap = [starting_reindeer]
    finished_reindeer_heap = []
    visited = {}
    while reindeer_heap:
        # Get the next reindeer from the top of our heap to move
        curr_reindeer = heapq.heappop(reindeer_heap)

        # If the reindeer at the top of our heap is slower than our finished reindeer, then
        # we can stop as all reindeer left will be slower and we have found all best paths
        if finished_reindeer_heap and curr_reindeer.score >= finished_reindeer_heap[0].score:
            break

        # Get all of the directions this reindeer can go next
        next_directions = curr_reindeer.directions_can_move(walls)

        # Check if we are at a dead end (cannot go in any direction)
        if len(next_directions) == 0:
            continue

        # Create ghost reindeers for all valid turns available to us
        ghost_reindeers = []
        for direction in next_directions:
            # Create a copy of our current reindeer, turn (if needed), and move forward
            ghost_reindeer = curr_reindeer.copy()
            if direction != curr_reindeer.direction:
                ghost_reindeer.turn(direction)
            ghost_reindeer.move()

            # Check if we have been to this spot facing this direction before
            if (ghost_reindeer.position, ghost_reindeer.direction) in visited:
                # If we have been here before and this is a worse run, just continue
                if ghost_reindeer.score > visited[(ghost_reindeer.position, ghost_reindeer.direction)]:
                    continue
            else:
                # If we have not been here before, add it to our visited dict and track the score
                visited[(ghost_reindeer.position,
                         ghost_reindeer.direction)] = ghost_reindeer.score

            # Check if we are at the end of the maze for this reindeer
            if ghost_reindeer.position == end:
                heapq.heappush(finished_reindeer_heap, ghost_reindeer)

            # Otherwise add this reindeer to our list of ghost reindeers and continue
            ghost_reindeers.append(ghost_reindeer)

        # Add all new ghost reindeers to our heap and continue
        for reindeer in ghost_reindeers:
            heapq.heappush(reindeer_heap, reindeer)

    # Get the number of best path tiles based on the paths taken by all the
    # fastest reindeer in the maze
    best_path_tiles = set()
    for reindeer in finished_reindeer_heap:
        best_path_tiles = best_path_tiles.union(reindeer.visited)

    # Output the reindeer that finished with the lowest score
    print(
        "The number of best path tiles along any of the reindeer's fastest "
        f"paths was: {len(best_path_tiles)} tiles."
    )


if __name__ == "__main__":
    main()
