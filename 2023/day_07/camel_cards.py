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

_JOKER_CARD = "J"

# Define's a Camel Cards game hand
class CamelHand():
    def __init__(self, hand: str, bid: int, jokers: bool = False):
        self.hand = hand
        self.bid = bid
        self.hand_type = self.find_hand_type()
        self.jokers = jokers

        # Evaluate jokers if we set the flag to do so
        if jokers:
            self.evaluate_jokers()
    
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
            this_card = self.get_face_card_value(self.hand[i])
            other_card = self.get_face_card_value(other_camel_hand.hand[i])

            return this_card > other_card
        
        # If for some reason we have hands that are equal
        # (we shouldn't, but idfk) return None
        return None
    
    def evaluate_jokers(self):
        """Evaluate jokers in our hand and modify our hand type to be
        the highest possible hand based on our jokers
        """
        # Check if we have no jokers, if so, just return early
        if _JOKER_CARD not in self.hand:
            return

        # If we have jokers, get the other cards in our hands 
        possible_hands = []
        for card in self.hand:
            if card == _JOKER_CARD:
                continue

            possible_hands.append(CamelHand(self.hand.replace("J", card), bid=self.bid))
        
        # Go through and compare all of the possible hands to determine
        # the greatest hand, and set our hand type accordingly
        greatest_hand = self
        for possible_hand in possible_hands:
            if possible_hand.compare(greatest_hand):
                greatest_hand = possible_hand
        self.hand_type = greatest_hand.hand_type
    
    def get_face_card_value(self, card):
        """Gets the value of a card."""
        # If our card is a number already
        # just return the number
        if card.isnumeric():
            return int(card)
        
        # If we are using jokers, check for that,
        # and return a super low val
        if self.jokers and card == _JOKER_CARD:
            return 1
        
        # Otherwise we have a facecard, so return 
        # its value based on the defined map
        return _FACE_CARD_VALUES[card]
        
        

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