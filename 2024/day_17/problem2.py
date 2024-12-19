"""
Advent of Code 2024
Day: 17
Problem: 01
Author: Nathan Rand
Date: 12.18.24
"""
import re
_INPUT_FILE_NAME = "corrupted_example.txt"

_REGISTERS = ["A", "B", "C"]


def _combo_operand(operand: int, registers: dict):
    """Apply combo operand logic."""
    if operand == 7:
        raise ValueError(
            "Tried to do a combo operand on reserved operand [7]."
        )

    return operand if operand <= 3 else registers[_REGISTERS[operand-4]]


def _adv_instruction(operand: int, registers: dict):
    """Instruction for opcode 0"""
    registers["A"] = int(
        registers["A"]/2**(_combo_operand(operand, registers))
    )
    return None


def _bxl_instruction(operand: int, registers: dict):
    """Instruction for opcode 1"""
    registers["B"] = registers["B"] ^ operand
    return None


def _bst_instruction(operand: int, registers: dict):
    """Instruction for opcode 2"""
    registers["B"] = _combo_operand(operand, registers) % 8
    return None


def _jnz_instruction(operand: int, registers: dict):
    """Instruction for opcode 3"""
    return None if registers["A"] == 0 else operand


def _bxc_instruction(operand: int, registers: dict):
    """Instruction for opcode 4"""
    registers["B"] = registers["B"] ^ registers["C"]
    return None


def _out_instruction(operand: int, registers: dict):
    """Instruction for opcode 5"""
    return _combo_operand(operand, registers) % 8


def _bdv_instruction(operand: int, registers: dict):
    """Instruction for opcode 6"""
    registers["B"] = int(
        registers["A"]/2**(_combo_operand(operand, registers))
    )
    return None


def _cdv_instruction(operand: int, registers: dict):
    """Instruction for opcode 7"""
    registers["C"] = int(
        registers["A"]/2**(_combo_operand(operand, registers))
    )
    return None


_INSTRUCTIONS = [
    _adv_instruction,
    _bxl_instruction,
    _bst_instruction,
    _jnz_instruction,
    _bxc_instruction,
    _out_instruction,
    _bdv_instruction,
    _cdv_instruction
]


def main():
    """Advent of Code - Day 17 - Part 01 [Chronospatial Computer]"""
    # Read in our input file with the given registers and program
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        registers_str, program_str = f.read().split("\n\n")

    # Process our input strings into registers and program for easier use
    registers = {
        register: int(val) for register, val in
        zip(["A", "B", "C"], re.findall(r"(\d+)", registers_str))
    }
    program = [int(num) for num in re.findall(r"(\d)", program_str)]

    # NOTE: Going to brute force this first cause I am lazy
    solution_not_found = True
    registers["A"] = 0
    while solution_not_found:
        # Update our registry trying again with a new value for A
        registers["A"] += 1

        # Go through our programs performing the instructed actions
        instruction_ptr = 0
        program_output = []
        invalid = True
        while instruction_ptr < len(program)-1 and invalid:
            # Grab our opcode and operand based on the position of the instruction ptr
            opcode, operand = program[instruction_ptr:instruction_ptr+2]

            # Get the instruction corresponding to this opcode and run it
            opcode_instruction = _INSTRUCTIONS[opcode]
            instruction_output = opcode_instruction(operand, registers)

            # Mutate stuff in our program space based on the output if we have certain op codes
            jumped = False
            if opcode == 3:  # jnz instruction, sets ptr
                if instruction_output is not None:
                    instruction_ptr = instruction_output
                    jumped = True
            elif opcode == 5:  # out instruction, adds output to our program
                program_output.append(instruction_output)

            # Advance the instruction ptr if we did not jump
            if not jumped:
                instruction_ptr += 2

            if program_output:
                for i, out in enumerate(program_output):
                    if out != program[i]:
                        invalid = True
                        break

        if not invalid:
            if len(program_output) != program:
                continue

            for i, out in enumerate(program):
                if out != program_output[i]:
                    invalid = True
                    break

        solution_not_found = invalid

    # Form our program output string
    program_output_str = ",".join([str(num) for num in program_output])
    print(registers["A"])
    # Output our result
    print(
        "The resulting output once the program halts is: "
        f"{program_output_str}"
    )


if __name__ == "__main__":
    main()
