"""
Advent of Code 2023
Day: 07
Problem: 01
Author: Nathan Rand
Date: 08.11.2024
"""
from enum import IntEnum
from typing import List

class HandPowerRanking(IntEnum):
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

    def compare(self, other_camel_hand: "CamelHand"):
        """Compare two camel hands.
        Returns true if greater than, false otherwise.
        """
        if self.hand_type != other_camel_hand.hand_type:
            return self.hand_type > other_camel_hand.hand_type
        
        # Now go through the cards in each hand to compare
        for i in range(len(self.hand)):
            # Check if our cards are the same, if so, continue
            # to find a difference on a later card
            if self.hand[i] == other_camel_hand.hand[i]:
                continue
            
            # Convert our face cards based on the defined dictionary,
            # if not a face card, convert to an int directly
            this_card = int(self.hand[i]) if self.hand[i].isnumeric() else _FACE_CARD_VALUES[self.hand[i]]
            other_card = int(other_camel_hand.hand[i]) if other_camel_hand.hand[i].isnumeric() else _FACE_CARD_VALUES[other_camel_hand.hand[i]]

            return this_card > other_card
        
        # If for some reason we have hands that are equal
        # (we shouldn't, but idfk) return None
        return None

def camel_quicksort(hands: List[CamelHand]):
    """Applies quicksort based on the CamelHand.compare()
    functionality. Sorts from least to greatest.
    """
    if len(hands) <= 1:
        return hands

    pivot = hands[0]
    left = [hand for hand in hands[1:] if pivot.compare(hand)]
    right = [hand for hand in hands[1:] if hand.compare(pivot)]
    return camel_quicksort(left) + [pivot] + camel_quicksort(right)
        

def main():
    with open("input.txt", "r") as f:
        # Extract our times and distance data
        card_hand_strings = f.read().split("\n")
        
        # Create card objects from our lines
        camel_hands = []
        for card_hand_string in card_hand_strings:
            hand, bid = card_hand_string.split(" ")
            camel_hands.append(CamelHand(hand, int(bid)))
        
        # Apply our custom quicksort to sort our camel hands
        sorted_camel_hands = camel_quicksort(camel_hands)

        # Compute the total winnings
        total_winnings = 0
        for i in range(len(sorted_camel_hands)):
            total_winnings += sorted_camel_hands[i].bid*(i+1)
        
        # Output our result
        print(f"Total Winnings of the set of Camel Card Hands: {total_winnings}")

if __name__ == "__main__":
    main() 