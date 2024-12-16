"""
Advent of Code 2024
Day: 15
Problem: 02
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

    def move(self, direction: tuple, boxes: list, walls: set):
        """Move the robot. If any boxes are encountered and can be moved
        they will be moved (this will manipulate `boxes`in place).

        Parameters
        ----------
        direction: tuple
            The direction to move the robot
        boxes: list
            Current boxes in the warehouse
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
        future_robot = Robot(next_position)
        collided_box = [
            box for box in boxes if box.robot_collides(future_robot)
        ]
        if len(collided_box) == 0:
            self.position = next_position
            return
        else:
            collided_box = collided_box[0]

        # Otherwise we are about to try and push a box, so check if we can and grab all
        # boxes we might push as a result
        box_queue = [collided_box]
        boxes_to_move = []
        while box_queue:
            # Get the next box from the queue
            curr_box = box_queue.pop(0)

            # Check if we can move this box in the given direction (no walls).
            # If we cannot, we cannot move any of the boxes so we return
            if not curr_box.can_move(direction, walls):
                return

            # See what boxes we will hit as a result of moving this box
            boxes_hit = curr_box.get_boxes_hit_if_moved(direction, boxes)
            box_queue.extend(boxes_hit)

            # Add our boxes to move to the list so we can move them at the end
            # if we are succesful
            boxes_to_move.append(curr_box)

        # Move all our boxes that need to be moved now that we know they all CAN be moved
        for box in boxes_to_move:
            box.move(direction)

        # Finally, we move the robot to the now available space where the original box was
        self.position = next_position


class Box():
    def __init__(self, initial_position: tuple):
        """Creates a box based on the initial position of its leftmost edge"""
        self.position = (
            initial_position,
            (initial_position[0], initial_position[1]+1)
        )

    @property
    def gps_location(self):
        """Current GPS location for the box."""
        return self.position[0][0]*100 + self.position[0][1]

    def robot_collides(self, robot: Robot):
        """Check if a robot collides with this box."""
        return robot.position == self.position[0] or robot.position == self.position[1]

    def other_box_collides(self, other_box):
        """Check if another box collides with this box."""
        return (
            self.position[0] == other_box.position[1] or
            self.position[0] == other_box.position[0] or
            self.position[1] == other_box.position[1] or
            self.position[1] == other_box.position[0]
        )

    def _get_next_box_position(self, direction: tuple):
        return (
            (self.position[0][0] + direction[0],
             self.position[0][1] + direction[1]),
            (self.position[1][0] + direction[0],
             self.position[1][1] + direction[1]),
        )

    def can_move(self, direction: tuple, walls: set):
        """Check if this box can be moved in a direction."""
        next_box_position = self._get_next_box_position(direction)

        return not (next_box_position[0] in walls or next_box_position[1] in walls)

    def get_boxes_hit_if_moved(self, direction: tuple, boxes: list):
        """Get the boxes that would be hit if this box moved in a direction."""
        potential_moved_box = Box(self._get_next_box_position(direction)[0])
        boxes_hit = []

        for other_box in boxes:
            if other_box == self:
                continue

            if potential_moved_box.other_box_collides(other_box):
                boxes_hit.append(other_box)
                if len(boxes_hit) == 2:
                    # Break out early cause we have found the max number of boxes we can
                    # hit as a result of a move
                    break

        return boxes_hit

    def move(self, direction: tuple):
        """Assuming we have confirmed we can move, move the box in the given direction."""
        self.position = self._get_next_box_position(direction)


def main():
    """Advent of Code - Day 15 - Part 02 [Warehouse Woes]"""
    # Read in our input file containing the warehouse map and movement instructions
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        warehouse_str, movements_str = f.read().split("\n\n")

    # Parse the warehouse string
    boxes = []
    walls = set()
    robot = None
    for i, warehouse_row in enumerate(warehouse_str.split("\n")):
        for j, space in enumerate(warehouse_row):
            if space == _WALL:
                walls.add((i, j*2))
                walls.add((i, (j*2)+1))
            elif space == _BOX:
                boxes.append(Box((i, j*2)))
            elif space == _ROBOT:
                robot = Robot((i, j*2))

    # Move while we still have moves to do in our queue
    movement_queue = list(str.replace(movements_str, "\n", ""))
    while movement_queue:
        direction = _MOVEMENTS[movement_queue.pop(0)]
        robot.move(direction, boxes, walls)

    # Finally, compute the GPS location of all of our boxes
    GPS_location_sum = 0
    for box in boxes:
        GPS_location_sum += box.gps_location

    # Output our result
    print(f"The resulting sum of all box GPS locations is: {GPS_location_sum}")


if __name__ == "__main__":
    main()
