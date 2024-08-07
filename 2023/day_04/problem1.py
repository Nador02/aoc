"""
Advent of Code 2023
Day: 04
Problem: 01
Author: Nathan Rand
Date: 08.04.2024
"""
import regex as re

_SCRATCHCARD_PATTERN = re.compile(r'\d+')

def main():
    with open("input.txt", "r") as f:
        scratchcards = f.read().split("\n")
        points = 0
        for card in scratchcards:
            # Extract the winning and scratched nums for the card
            card_nums = ''.join(card.split(":")[1])
            winning_nums_string, scratched_nums_string = card_nums.split("|")
            winning_nums = _SCRATCHCARD_PATTERN.findall(winning_nums_string)
            scratched_nums = _SCRATCHCARD_PATTERN.findall(scratched_nums_string)

            # Count how many number matches are found
            num_matched_numbers = 0
            for num in winning_nums:
                if num in scratched_nums:
                    num_matched_numbers += 1
            points += 2**(num_matched_numbers - 1) if num_matched_numbers != 0 else 0

        print(f"Total points on scratchcards: {points}")
            
if __name__ == "__main__":
    main() 