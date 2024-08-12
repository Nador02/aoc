"""
Advent of Code 2023
Day: 07
Problem: 01
Author: Nathan Rand
Date: 08.11.2024
"""
from enum import Enum

class HandPowerRanking(Enum):
    FIVEOFAKIND = 7
    FOUROFAKIND = 6
    FULLHOUSE = 5
    THREEOFAKIND = 4
    TWOPAIR = 3
    ONEPAIR = 2
    HIGHCARD = 1

_FACE_CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10
}

# Define's a Camel Cards game hand
class CamelHand():
    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.hand_type = self.find_hand_type()
    
    def find_hand_type(self):
        # Go through and count our cards in a dict
        card_counts = {}
        for card in self.hand:
            if card in card_counts.keys():
                card_counts[card] += 1
                continue
            card_counts[card] = 1

        # Check for each type of card hand and return the
        # corresponding Enum value
        card_count_values = card_counts.values()
        if 5 in card_count_values:
            return HandPowerRanking.FIVEOFAKIND
        elif 4 in card_count_values:
            return HandPowerRanking.FOUROFAKIND
        elif 3 in card_count_values:
            if 2 in card_count_values:
                return HandPowerRanking.FULLHOUSE
            return HandPowerRanking.THREEOFAKIND
        elif 2 in card_count_values:
            num_pairs = list(card_count_values).count(2)
            if num_pairs == 2:
                return HandPowerRanking.TWOPAIR
            return HandPowerRanking.ONEPAIR
        return HandPowerRanking.HIGHCARD

def compare_camel_hands(camel_hand_1 : CamelHand, camel_hand_2: CamelHand):
    print("Test for now")

def main():
    with open("example.txt", "r") as f:
        # Extract our times and distance data
        card_hand_strings = f.read().split("\n")
        
        # Create card objects from our lines
        camel_hands = []
        for card_hand_string in card_hand_strings:
            hand, bid = card_hand_string.split(" ")
            camel_hands.append(CamelHand(hand, bid))
        
        # Binary search for our insert location


if __name__ == "__main__":
    main() 