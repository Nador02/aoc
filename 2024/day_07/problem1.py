"""
Advent of Code 2024
Day: 07
Problem: 01
Author: Nathan Rand
Date: 12.07.24
"""
from enum import Enum
import re
from itertools import product
_INPUT_FILE_NAME = "input.txt"


class Operand(Enum):
    """Supported operands for repairing the bridge."""
    ADD = 0
    MULTIPLY = 1


def apply_operand(operand, num1, num2):
    """Apply a given operand two the 2 provided numbers"""
    return num1+num2 if operand == Operand.ADD else num1*num2


def solve_equation_given_operands(operands, equation):
    """Solve an equation given a set of operands"""
    total = equation[0]
    for i in range(len(equation)-1):
        # No PEMDAS! Just L -> R
        total = apply_operand(operands[i], total, equation[i+1])

    return total


def main():
    """Advent of Code - Day 07 - Part 01 [Bridge Repair]"""
    # Read in our calibration equations
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        calibrations = f.read().split("\n")

    # Lets brute force the living shit out of this
    total_calibration_result = 0
    for calibration in calibrations:
        calibration_nums = [int(num) for num in re.findall(r"\d+", calibration)]
        test_value, equation = calibration_nums[0], calibration_nums[1:]

        # This is gonna break my computer
        possible_operand_combos = product([Operand.ADD, Operand.MULTIPLY], repeat=len(equation)-1)
        for operands in possible_operand_combos:
            if test_value == solve_equation_given_operands(operands, equation):
                total_calibration_result += test_value
                break

    # Output our result
    print(
        "The total calibration result from all calibration equations "
        f"that were valid with some operand combo is: {total_calibration_result}"
    )


if __name__ == "__main__":
    main()
