"""
Advent of Code 2024
Day: 13
Problem: 02
Author: Nathan Rand
Date: 12.14.24
"""

from dataclasses import dataclass
import numpy as np
import re
_INPUT_FILE_NAME = "input.txt"
_COST_TO_PRESS = np.array([[3], [1]])
_INT_TOLERANCE = 1e-12
_PRIZE_UNIT_CONVERSION = np.ones((2, 1), dtype=np.float64)*1e13


def _get_two_nums_from_str(claw_machine_str_row: str):
    """This just takes a single row and grabs the 2 numbers
    and tosses them into a np column vector.
    """
    return np.array(
        [[int(num) for num in re.findall(r"\d+", claw_machine_str_row)]],
        dtype=np.float64
    ).T


def _is_almost_int(num: float):
    """Return true if a number is almost an integer (accounts for
    floating point nonsense).
    """
    return abs(num - np.round(num)) < _INT_TOLERANCE


def _is_invalid_presses(presses: np.ndarray):
    return (
        np.any(presses < 0)
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
        # print((self.prize + _PRIZE_UNIT_CONVERSION).astype('str'))
        presses = np.linalg.solve(
            self.buttons, self.prize + _PRIZE_UNIT_CONVERSION)
        if _is_invalid_presses(presses):
            return 0
        cost = np.sum(presses*_COST_TO_PRESS)
        return int(np.round(cost))

    def get_cost_with_cramers(self):
        """Trying a different approach with Cramer's rule based
        on solutions from subreddit :)
        """
        # Apply Cramer's rule to solve the system of equations with
        # less floating point precision error (only one division)
        button_determinant = (
            self.buttons[0, 0]*self.buttons[1, 1] -
            self.buttons[1, 0]*self.buttons[0, 1]
        )
        press_A = (
            (self.prize[0]+1e13)*self.buttons[1, 1] -
            (self.prize[1]+1e13)*self.buttons[0, 1]
        )/button_determinant
        press_B = (
            (self.prize[1]+1e13)*self.buttons[0, 0] -
            (self.prize[0]+1e13)*self.buttons[1, 0]
        )/button_determinant

        # Determine the cost and return it if it is almost an int
        cost = press_A*_COST_TO_PRESS[0] + press_B*_COST_TO_PRESS[1]
        return int(cost[0]) if _is_almost_int(cost) else 0


def main():
    """Advent of Code - Day 13 - Part 02 [Claw Contraption]"""
    # Read in our input file
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        claw_machines = [
            ClawMachine.from_input(claw_machine_str)
            for claw_machine_str in f.read().split("\n\n")
        ]

    # Go through each claw machine determining the min cost to get the prize
    total_cost = 0
    total_cost_w_cramers = 0
    for claw_machine in claw_machines:
        total_cost += claw_machine.get_min_cost_for_prize()
        total_cost_w_cramers += claw_machine.get_cost_with_cramers()

    # Output our result
    print(
        f"Total min cost to get all possible prizes: {total_cost}\n"
        "NOTE: Wrong at higher int tolerances (< 1e-3) due to floating point precision!\n"
    )

    # Output our result as computed with Cramer's rule
    print(
        "Correct total cost as computed with "
        f"Cramer's rule: {total_cost_w_cramers}"
    )


if __name__ == "__main__":
    main()
