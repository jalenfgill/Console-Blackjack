from Player import Player

class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer")

    def show_initial_hand(self):
        print(f"Dealer's hand: [{self.hands[0][0]}, '?']")
