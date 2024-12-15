"""
Advent of Code 2024
Day: 14
Problem: 02
Author: Nathan Rand
Date: 12.14.24
"""
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

_INPUT_FILE_NAME = "input.txt"
_ROBOT_STR_PATTERN = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

# Define the dimensions of our space outside the bathroom
_HEIGHT = 103
_WIDTH = 101
_X_BOUNDS = (0, _WIDTH)
_Y_BOUNDS = (0, _HEIGHT)
_CONSECUTIVE_ROBOTS_LIMIT = 8
_WAIT_TIME = 10000


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
    """Advent of Code - Day 14 - Part 02 [Restroom Redoubt]"""
    # Read in and create our robots based on the input text
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        robots = [
            Robot((int(p_x), int(p_y)), (int(v_x), int(v_y)))
            for robot_str in f.read().split("\n")
            for p_x, p_y, v_x, v_y in re.findall(_ROBOT_STR_PATTERN, robot_str)
        ]

    images_dir = Path("images/")
    # Move forward in time to see how our robots move through the space
    for t in range(_WAIT_TIME):
        # Create our text based on all the robot positions
        grid = np.zeros((_HEIGHT, _WIDTH))
        for robot in robots:
            robot.move()
            grid[robot.position[1]][robot.position[0]] = 1

        # Only make the image if some condition is met that this *might* be a christmas tree
        # BRUTE FORCE TIME LETS FREAKING GO
        # NOTE: probably a better solution for this but I cannot be bothered rn
        might_be_a_christmas_tree = False
        running_total = 0
        for row in grid:
            for space in row:
                if space == 1:
                    running_total += 1
                    if running_total > _CONSECUTIVE_ROBOTS_LIMIT:
                        might_be_a_christmas_tree = True
                        break
                else:
                    running_total = 0

        # If we have arbitrarily determined that this might be a christmas tree so produce
        # the figure so we can visually confirm our downselected plots
        if might_be_a_christmas_tree:
            plt.imshow(
                grid,
                interpolation='nearest',
                cmap=matplotlib.cm.Greens,
                origin="lower"
            )
            plt.savefig(images_dir / f"robot_positions_{t+1}.png")


if __name__ == "__main__":
    main()
