"""
Advent of Code 2024
Day: 02
Problem: 02
Author: Nathan Rand
Date: 12.02.2024
"""
from typing import List
import numpy as np
_INPUT_FILE_NAME = "input.txt"


def is_report_safe(report: List[float]):
    # Get the diff between elements in our report
    report_diff = np.diff(report)

    # Determine if our report is monotonic (only increasing or decreasing),
    # then return the safe report status based on this and diff magnitude
    is_monotonic = np.all(report_diff > 0) or np.all(report_diff < 0)
    return is_monotonic and np.all(abs(report_diff) <= 3)


def is_report_safe_w_problem_dampener(report: List[float]):
    # Check if our report is safe without the dampener
    if is_report_safe(report):
        return True

    # NOTE: Brute Force, can improve
    # If not safe, apply the dampener by removing each element
    # in order and checking if removing any will allow for a safe report.
    for i in range(len(report)):
        trimmed_report = (
            report[:i] + report[i+1:]
            if i < len(report)-1 else report[:-1]
        )
        if is_report_safe(trimmed_report):
            return True

    return False


def main():
    """Advent of Code - Day 02 - Part 02 [Red-Nosed Reports]"""
    # Read in our reports
    with open(_INPUT_FILE_NAME, "r") as f:
        report_data = f.read().split("\n")
        fission_reports = [[int(level) for level in report.split()]
                           for report in report_data]

    # Determine how many reports are safe
    safe_reports = 0
    for report in fission_reports:
        if is_report_safe_w_problem_dampener(report):
            safe_reports += 1

    # Output our result
    print(
        "The number of safe rudolf nuclear fission reports "
        f"with the problem dampener is: {int(safe_reports)} reports"
    )


if __name__ == "__main__":
    main()
