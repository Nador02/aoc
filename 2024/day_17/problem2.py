"""
Advent of Code 2024
Day: 17
Problem: 02
Author: Nathan Rand
Date: 12.18.24
"""
import re
from chronospatial_computer import get_chrono_computer_output
_INPUT_FILE_NAME = "input.txt"


def main():
    """Advent of Code - Day 17 - Part 02 [Chronospatial Computer]"""
    # Read in our input file with the given registers and program
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        _, program_str = f.read().split("\n\n")

    # Process our input string and grab the program to use for determining
    # the corresponding register
    program = [int(num) for num in re.findall(r"(\d)", program_str)]

    # Display some example outputs while changing register A's value to try
    # and detect patterns in our program's output
    for test_reg_A in range(int(8e3)):
        curr_output = get_chrono_computer_output(
            program,
            {
                "A": test_reg_A,
                "B": 0,
                "C": 0
            }
        )
        print(curr_output)

    # NOTE: this solves the example, but my input is more complicated :(
    # register_A = 0
    # for i, num in enumerate(program[::-1]):
    #     register_A += num*8**(len(program)-i)

    # NOTE: this is just testing stuff out, not working
    # program_stack = list(program)
    # searching_for_num = program_stack.pop()
    # curr_power = 0
    # test_reg_A = 0
    # depth_stack = []
    # depth = 0
    # while program_stack:
    #     test_registers = {
    #         "A": test_reg_A,
    #         "B": 0,
    #         "C": 0
    #     }
    #     output = get_chrono_computer_output(program, test_registers)
    #     print(output)
    #     prev_output = get_chrono_computer_output(
    #         program, {"A": test_reg_A-1, "B": 0, "C": 0})
    #     print(prev_output)
    #     print("")
    #     if output[0] == searching_for_num:
    #         # bad = False
    #         # for i, num in enumerate(output[1:]):
    #         #     print(output)
    #         #     print(program[len(program)-len(output)+i])
    #         #     if num != program[len(program)-len(output)+i]:
    #         #         bad = True
    #         # if bad:
    #         #     test_reg_A += 1
    #         #     depth += 1
    #         #     continue
    #         # curr_power += 1
    #         # test_reg_A = int(8**curr_power)
    #         searching_for_num = program_stack.pop()
    #         depth_stack.append(depth)
    #         curr_power += 1
    #         test_reg_A = sum([depth*8**(len(depth_stack)-curr_power)
    #                          for curr_power, depth in enumerate(depth_stack)])
    #         depth = 0
    #     else:
    #         test_reg_A += 1
    #         depth += 1


if __name__ == "__main__":
    main()
