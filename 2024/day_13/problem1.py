"""
Advent of Code 2024
Day: 13
Problem: 01
Author: Nathan Rand
Date: 12.14.24
"""

from dataclasses import dataclass
import numpy as np
import re
_INPUT_FILE_NAME = "input.txt"
_COST_TO_PRESS = np.array([[3], [1]])
_INT_TOLERANCE = 1e-6
_OW_MY_FINGERS_HURT = 100  # Total press limit


def _get_two_nums_from_str(claw_machine_str_row: str):
    """This just takes a single row and grabs the 2 numbers
    and tosses them into a np column vector.
    """
    return np.array(
        [[int(num) for num in re.findall(r"\d+", claw_machine_str_row)]]
    ).T


def _is_almost_int(num: float):
    """Return true if a number is almost an integer (accounts for
    floating point nonsense).
    """
    return abs(num - np.round(num)) < _INT_TOLERANCE


def _is_invalid_presses(presses: np.ndarray):
    return (
        np.any(presses > _OW_MY_FINGERS_HURT)
        or np.any(presses < 0)
        or np.any([not _is_almost_int(press) for press in presses])
    )


@dataclass
class ClawMachine():
    buttons: np.ndarray
    prize: np.ndarray

    @classmethod
    def from_input(cls, claw_machine_str: str):
        """Create a claw machine from input string.

        Parameters
        ----------
        claw_machine_str: str
            The input str representing this claw machine

        Returns
        -------
        ClawMachine
        """
        # Grab the numbers for the buttons and prize from each row
        # and put them into numpy column vectors
        claw_machine_str_rows = claw_machine_str.split("\n")
        button_A = _get_two_nums_from_str(claw_machine_str_rows[0])
        button_B = _get_two_nums_from_str(claw_machine_str_rows[1])
        prize = _get_two_nums_from_str(claw_machine_str_rows[2])

        # Create the matrices needed for solving our system later (Ax=b)
        return cls(
            np.hstack((button_A, button_B)),
            prize
        )

    def get_min_cost_for_prize(self):
        """Solve our linear system of equations and return the min
        cost to get the prize.

        Returns
        -------
        int
            Total cost if it is possible to get to the prize in whole button
            presses. Otherwise returns zero.

        """
        # Solve our linear system of equations and return the cost
        # IF we got there with button presses (answer is an int)
        presses = np.linalg.solve(self.buttons, self.prize)
        if _is_invalid_presses(presses):
            return 0

        cost = np.sum(presses*_COST_TO_PRESS)
        return int(np.round(cost))


def main():
    """Advent of Code - Day 13 - Part 01 [Claw Contraption]"""
    # Read in our input file
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        claw_machines = [
            ClawMachine.from_input(claw_machine_str)
            for claw_machine_str in f.read().split("\n\n")
        ]

    # Go through each claw machine determining the min cost to get the prize
    total_cost = 0
    for claw_machine in claw_machines:
        total_cost += claw_machine.get_min_cost_for_prize()

    # Output our result
    print(f"Total min cost to get all possible prizes: {total_cost}")


if __name__ == "__main__":
    main()
