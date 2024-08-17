"""
Advent of Code 2023
Day: 07
Problem: 01
Author: Nathan Rand
Date: 08.11.2024
"""
from camel_cards import CamelHand, camel_quicksort
        
def main():
    with open("input.txt", "r") as f:
        # Extract our times and distance data
        card_hand_strings = f.read().split("\n")
        
        # Create card objects from our lines
        camel_hands = []
        for card_hand_string in card_hand_strings:
            hand, bid = card_hand_string.split(" ")
            camel_hands.append(CamelHand(hand, int(bid), jokers=True))
        
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