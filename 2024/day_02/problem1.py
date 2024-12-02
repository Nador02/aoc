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


def main():
    """Advent of Code - Day 02 - Part 01 [Red-Nosed Reports]"""
    # Read in our reports
    with open(_INPUT_FILE_NAME, "r") as f:
        report_data = f.read().split("\n")
        fission_reports = [[int(level) for level in report.split()]
                           for report in report_data]

    # Determine how many reports are safe
    safe_reports = 0
    for report in fission_reports:
        if is_report_safe(report):
            safe_reports += 1

    # Output our result
    print(
        "The number of safe rudolf nuclear fission reports is: "
        f"{int(safe_reports)} reports"
    )


if __name__ == "__main__":
    main()
