import random

class Deck:
    def __init__(self, deck_count=1):
        self.card_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10, "A": 11,
            "10": 10, "A": 11
        }
        self.cards = self.create_deck(deck_count)
        self.shuffle()

    def create_deck(self, deck_count):
        deck = []
        for card, value in self.card_values.items():
            for _ in range(deck_count * 4):  # Each card appears 4 times per deck
                deck.append(card)
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
