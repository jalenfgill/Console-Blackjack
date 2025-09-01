from Deck import Deck

class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.hands = [[]]
        self.balance = balance
        self.initial_bet = 0
        self.insurance_bet = 0
        self.total_bet = self.initial_bet

    def get_hands(self):
        return self.hands

    def get_hand(self, index=0):
        return self.hands[index]

    def place_bet(self, amount):
        if 10 <= amount <= 1000 and amount <= self.balance:
            self.initial_bet = amount
            self.total_bet = self.initial_bet
            self.balance -= amount
            print(f"{self.name} placed a bet of {amount}. Current balance: {self.balance}")
        else:
            print(f"Invalid bet amount: {amount}. Bet must be between 10 and 1000 and not exceed current balance.")

    def double_bet(self, index):
        if len(self.hands[index]) > 2:
            print("You can only double during your initial hand.")
        elif 10 <= self.initial_bet <= 1000 and self.initial_bet <= self.balance:
            self.balance -= self.initial_bet
            self.total_bet *= 2
            print(f"{self.name} doubled their bet. Current balance: {self.balance}")
        else:
            print("Your balance is insufficient to double your hand.")

    def take_insurance(self):
        if 10 <= self.initial_bet <= 1000 and self.initial_bet <= self.balance:
            self.insurance_bet = self.initial_bet / 2
            self.balance -= self.insurance_bet
            print(f"{self.name} has taken insurance. Current balance: {self.balance}")
        else:
            print("Your balance is insufficient to take insurance")

    def hit(self, card, index=0):
        self.hands[index].append(card)

    def split_hand(self, index):
        if Deck().card_values[self.hands[index][0]] != Deck().card_values[self.hands[index][1]]:
            print("You can only split hands of equal value.")
        elif len(self.hands[index]) != 2:
            print("You can only split an initial hand of two cards.")
        elif 10 <= self.initial_bet <= 1000 and self.initial_bet <= self.balance:
            self.balance -= self.initial_bet
            new_hand = self.hands[0].pop(1)
            self.hands.append([new_hand])
            print(f"{self.name} has split their hand. Current balance: {self.balance}")
        else:
            print("Your balance is insufficient to split your hand.")


    def calculate_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            if card == 'A':
                aces += 1
                value += 11
            else:
                value += Deck().card_values[card]

        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def show_hand(self, index=0):
        if len(self.hands) == 1:
            print(f"{self.name}'s hand: {self.hands[index]} (Value: {self.calculate_hand_value(self.hands[index])})")
        else:
            print(f"{self.name}'s hand #{index + 1}: {self.hands[index]} (Value: {self.calculate_hand_value(self.hands[index])})")

    def reset_hand(self):
        self.hands = [[]]
