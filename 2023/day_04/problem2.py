"""
Advent of Code 2023
Day: 04
Problem: 02
Author: Nathan Rand
Date: 08.05.2024
"""
import regex as re

_SCRATCHCARD_PATTERN = re.compile(r'\d+')

def main():
    with open("input.txt", "r") as f:
        scratchcards = f.read().split("\n")
        scratchcard_pile = {}
        for i in range(len(scratchcards)):
            # Add the current card to the dictionary if it does not already exist
            if (i+1) not in scratchcard_pile.keys():
                scratchcard_pile[i+1] = 1

            # Extract the winning and scratched nums for the card
            card_nums = ''.join(scratchcards[i].split(":")[1])
            winning_nums_string, scratched_nums_string = card_nums.split("|")
            winning_nums = _SCRATCHCARD_PATTERN.findall(winning_nums_string)
            scratched_nums = _SCRATCHCARD_PATTERN.findall(scratched_nums_string)

            # Count how many number matches are found
            num_matched_numbers = 0
            for num in winning_nums:
                if num in scratched_nums:
                    num_matched_numbers += 1

            # Update future cards quantities in the dict
            for j in range(1,num_matched_numbers+1):
                if i+j+1 in scratchcard_pile.keys():
                    scratchcard_pile[i+j+1] += scratchcard_pile[i+1]
                else:
                    scratchcard_pile[i+j+1] = 1+scratchcard_pile[i+1]

        print(f"Total scratchcards: {sum(scratchcard_pile.values())}")
            
if __name__ == "__main__":
    main() 