"""
Advent of Code 2023
Day: 02
Problem: 01
Author: Nathan Rand
Date: 08.03.2024
"""
import regex as re  

_PART_NUMBER_PATTERN = re.compile(r'\d{1,3}')
_SYMBOL_LIST = [r"#", r"/", r"@", r"\$", r"=", r"\+", r"%", r"\*", r"\&"]

def main():
    with open("input.txt", "r") as f:
        schematic = f.read().split("\n")
        part_number_sum = 0
        for i in range(len(schematic)):
            part_numbers_list = _PART_NUMBER_PATTERN.findall(schematic[i])
            part_numbers_positions = [(m.start(0), m.end(0)) for m in re.finditer(_PART_NUMBER_PATTERN, schematic[i])]
            part_numbers = {int(part_numbers_list[i]) : part_numbers_positions[i] for i in range(len(part_numbers_list))}
            symbol_positions = []
            for symbol in _SYMBOL_LIST:
                if i != 0:
                    symbol_positions.extend([m.start() for m in re.finditer(re.compile(symbol), schematic[i-1])])
                if i != len(schematic)-1:
                    symbol_positions.extend([m.start() for m in re.finditer(re.compile(symbol), schematic[i+1])])
                symbol_positions.extend([m.start() for m in re.finditer(re.compile(symbol), schematic[i])])
                
            for part_number, positions in part_numbers.items():
                if check_if_symbol_near_part_number(positions, symbol_positions):
                    part_number_sum += part_number
                
        print(f"Sum of all part numbers in engine schematic: {part_number_sum}")

def check_if_symbol_near_part_number(positions, symbol_positions):
    positional_range = range(positions[0]-1,positions[1]+2)
    for spot in positional_range:
        if spot in symbol_positions:
            return True

if __name__ == "__main__":
    main()