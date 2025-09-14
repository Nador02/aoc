"""
Advent of Code 2024
Day: 15
Problem: 01
Author: Nathan Rand
Date: 12.15.24
"""

_INPUT_FILE_NAME = "input.txt"

# Define characters we can find in the warehouse map
_WALL = "#"
_BOX = "O"
_ROBOT = "@"

# Map our movement instruction symbols to grid movements
_MOVEMENTS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}


class Robot():
    def __init__(self, initial_position: tuple):
        """Creates a new robot that can move around and rearrange
        boxes inside of a warehouse.
        """
        self.position = initial_position

    def move(self, direction: tuple, boxes: set, walls: set):
        """Move the robot. If any boxes are encountered and can be moved
        they will be moved (this will manipulate `boxes`in place).

        Parameters
        ----------
        direction: tuple
            The direction to move the robot
        boxes: set
            Current positions of all boxes in the warehouse
        walls:
            Current positions of all walls in the warehouse
        """
        # Define our next position for the robot if we are unobstructed
        next_position = (
            self.position[0] + direction[0],
            self.position[1] + direction[1]
        )

        # Check if there is a wall in our way, if so, do nothing
        if next_position in walls:
            return

        # If there is nothing at our next position (no box) just update our pos and continue
        if next_position not in boxes:
            self.position = next_position
            return

        # Otherwise we are about to try and push a box, so check if we can and grab all
        # boxes we might push as a result
        box_next_position = (
            next_position[0] + direction[0],
            next_position[1] + direction[1]
        )
        if box_next_position in walls:
            return

        # Basically just keep checking for if we can shift all the boxes over one
        # by iterating till we find an empty space. If we hit a wall at anypoint
        # we cannot slide the boxes over so just return
        while box_next_position in boxes:
            box_next_position = (
                box_next_position[0] + direction[0],
                box_next_position[1] + direction[1]
            )
            if box_next_position in walls:
                return

        # Instead of updating all the boxes we just teleport the first box to the
        # end of the line of boxes (the next position)
        boxes.remove(next_position)
        boxes.add(box_next_position)

        # Finally, we move the robot to the now available space where the first box was
        self.position = next_position


def main():
    """Advent of Code - Day 15 - Part 01 [Warehouse Woes]"""
    # Read in our input file containing the warehouse map and movement instructions
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        warehouse_str, movements_str = f.read().split("\n\n")

    # Parse the warehouse string
    boxes = set()
    walls = set()
    robot = None
    for i, warehouse_row in enumerate(warehouse_str.split("\n")):
        for j, space in enumerate(warehouse_row):
            if space == _WALL:
                walls.add((i, j))
            elif space == _BOX:
                boxes.add((i, j))
            elif space == _ROBOT:
                robot = Robot((i, j))

    # Move while we still have moves to do in our queue
    movement_queue = list(str.replace(movements_str, "\n", ""))
    while movement_queue:
        direction = _MOVEMENTS[movement_queue.pop(0)]
        robot.move(direction, boxes, walls)

    # Finally, compute the GPS location of all of our boxes
    GPS_location_sum = 0
    for box in boxes:
        GPS_location_sum += box[0]*100 + box[1]

    # Output our result
    print(f"The resulting sum of all box GPS locations is: {GPS_location_sum}")


if __name__ == "__main__":
    main()
