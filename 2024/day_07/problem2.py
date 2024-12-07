"""
Advent of Code 2024
Day: 07
Problem: 02
Author: Nathan Rand
Date: 12.07.24
"""
from enum import Enum
import re
from itertools import product
import numpy as np
_INPUT_FILE_NAME = "input.txt"


class Operand(Enum):
    """Supported operands for repairing the bridge."""
    ADD = 0
    MULTIPLY = 1
    CONCATENATE = 2


def apply_operand(operand, num1, num2):
    """Apply a given operand two the 2 provided numbers"""
    match operand:
        case Operand.ADD:
            return num1 + num2
        case Operand.MULTIPLY:
            return num1 * num2
        case Operand.CONCATENATE:
            # This log floor stuff gets the number of places to the LEFT
            # of the decimal place so we can append num1 onto num 2
            # (I also did this with string stuff originally, but... MATH :D)
            return (10**np.floor(np.log10(num2) + 1))*num1 + num2
        case _:
            raise ValueError(f"Unsupported operand provided: {operand}.")


def solve_equation_given_operands(operands, equation):
    """Solve an equation given a set of operands"""
    total = equation[0]
    for i in range(len(equation)-1):
        # No PEMDAS! Just L -> R
        total = apply_operand(operands[i], total, equation[i+1])

    return total


def main():
    """Advent of Code - Day 07 - Part 02 [Bridge Repair]"""
    # Read in our calibration equations
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        calibrations = f.read().split("\n")

    # Lets brute force the living shit out of this
    total_calibration_result = 0
    for calibration in calibrations:
        calibration_nums = [int(num) for num in re.findall(r"\d+", calibration)]
        test_value, equation = calibration_nums[0], calibration_nums[1:]

        # This is gonna break my computer (aw shit it really is now... 3^n :o)
        possible_operand_combos = product(
            [Operand.ADD, Operand.MULTIPLY, Operand.CONCATENATE],
            repeat=len(equation)-1
        )
        for operands in possible_operand_combos:
            if test_value == solve_equation_given_operands(operands, equation):
                total_calibration_result += test_value
                break

    # Output our result
    print(
        "The total calibration result from all calibration equations "
        f"that were valid (including concat. now) is: {total_calibration_result}"
    )


if __name__ == "__main__":
    main()
