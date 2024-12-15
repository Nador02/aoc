"""
Advent of Code 2024
Day: 14
Problem: 01
Author: Nathan Rand
Date: 12.14.24
"""
from collections import defaultdict
import re
_INPUT_FILE_NAME = "input.txt"
_ROBOT_STR_PATTERN = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

# Define the dimensions of our space outside the bathroom
_HEIGHT = 103
_WIDTH = 101
_X_BOUNDS = (0, _WIDTH)
_Y_BOUNDS = (0, _HEIGHT)

# Define how long we wait before analyzing the robots' positions
_WAIT_TIME = 100  # [s]


class Robot():
    def __init__(self, position: tuple, velocity: tuple):
        self.position = position
        self.velocity = velocity

    def move(self):
        """Move this robot"""
        next_x = self.position[0] + self.velocity[0]
        next_y = self.position[1] + self.velocity[1]

        # Check if we need to teleport relative to the x boundaries
        if next_x <= _X_BOUNDS[0]:
            next_x = _X_BOUNDS[1] + next_x

        if next_x >= _X_BOUNDS[1]:
            next_x = next_x - _X_BOUNDS[1]

        # Similarly, check if we need to teleport relative to the y boundaries
        if next_y <= _Y_BOUNDS[0]:
            next_y = _Y_BOUNDS[1] + next_y

        if next_y >= _Y_BOUNDS[1]:
            next_y = next_y - _Y_BOUNDS[1]

        # NOTE: I hope we cannot have velocity that is > 2*width or height ...

        # Update our robots position
        self.position = (
            next_x,
            next_y
        )

    def get_quadrant(self):
        # If we are in the middle of quadrants return -1 (not in any quadrant)
        x_midline = int((_X_BOUNDS[1]-1)/2)
        y_midline = int((_Y_BOUNDS[1]-1)/2)
        if self.position[0] == x_midline or self.position[1] == y_midline:
            return -1

        # Otherwise, return the quadrant we are in
        if self.position[0] < x_midline and self.position[1] > y_midline:
            return 1
        elif self.position[0] < x_midline and self.position[0] < y_midline:
            return 2
        elif self.position[0] > x_midline and self.position[1] < y_midline:
            return 3
        else:
            return 4


def main():
    """Advent of Code - Day 14 - Part 01 [Restroom Redoubt]"""
    # Read in and create our robots based on the input text
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        robots = [
            Robot((int(p_x), int(p_y)), (int(v_x), int(v_y)))
            for robot_str in f.read().split("\n")
            for p_x, p_y, v_x, v_y in re.findall(_ROBOT_STR_PATTERN, robot_str)
        ]

    # Move forward in time to see how our robots move through the space
    for _ in range(_WAIT_TIME):
        for robot in robots:
            robot.move()

    # Compile the quadrants all our robots end in
    quadrants = defaultdict(lambda: 0)
    for robot in robots:
        quadrants[robot.get_quadrant()] += 1

    # Get the safety factor and provide it as our result
    safety_factor = quadrants[1]*quadrants[2]*quadrants[3]*quadrants[4]
    print(
        "Our safety factor based on the ending positions of all "
        f"robots outside the bathroom is: {safety_factor}"
    )


if __name__ == "__main__":
    main()
