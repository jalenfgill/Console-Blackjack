from Deck import Deck
from Player import Player
from Dealer import Dealer

def get_valid_input(prompt, valid_range):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print(f"Input must be between {valid_range.start} and {valid_range.stop - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def initial_deal(deck, player, dealer):
    for _ in range(2):
        player.hit(deck.deal_card())
        dealer.hit(deck.deal_card())

def player_turn(deck, player, dealer):
    results = []
    index = 0
    while True:
        while index < len(player.get_hands()):
            player.show_hand(index)
            dealer.show_initial_hand()
            if player.calculate_hand_value(player.get_hand(index)) == 21:
                if (
                    index == 0 and
                    len(player.get_hands()) == 1 and
                    len(player.get_hand(index)) == 2 and
                    dealer.get_hand()[0] != "A" and
                    dealer.calculate_hand_value(dealer.get_hand()) != 21
                    ):
                    results.append("blackjack")
                    index+=1
                    break
                else:
                    results.append("draw")
                    index+=1
                    continue

            if len(player.get_hand(index)) == 2 and dealer.get_hand()[0] == "A":
                insurance_choice = input("Would you like to take insurance? (Insurance pays 2:1) Yes (Y) or No (N)").upper()
                if insurance_choice == "Y":
                    player.take_insurance()
                elif insurance_choice == "N":
                    print("Insurance has been declined.")
                else:
                    print("Invalid choice. Please choose again.")

                print("Checking dealer's hand...")
                if dealer.calculate_hand_value(dealer.get_hand(0)) == 21:
                    results.append("draw")
                    break
                else:
                    print("Dealer does not have blackjack, the game can continue.")

                player.show_hand(index)
                dealer.show_initial_hand()

            player_choice = input("Would you like to hit (H), stand (S), double (D), split (P), or surrender (F)? ").upper()

            if player_choice == 'H':
                player.hit(deck.deal_card(), index)
                if player.calculate_hand_value(player.get_hand(index)) > 21:
                    player.show_hand(index)
                    print("Bust! You lose.")
                    results.append("loss")
                    index+=1
            elif player_choice == 'S':
                print("You chose to stand.")
                results.append("draw")
                index+=1
            elif player_choice == 'D':
                if len(player.get_hand(index)) == 2:
                    player.double_bet(index)
                    player.hit(deck.deal_card(), index)
                    player.show_hand(index)
                    if player.calculate_hand_value(player.get_hand(index)) > 21:
                        player.show_hand(index)
                        print("Bust! You lose.")
                        results.append("loss")
                    else:
                        results.append("draw")
                    index+=1
                else:
                    print("You can only double your bet on the initial two cards.")
            elif player_choice == 'P':
                    if deck.card_values[player.get_hand(index)[0]] == deck.card_values[player.get_hand(index)[1]] and len(player.get_hand(index)) == 2:
                        player.split_hand(index)
                        player.hit(deck.deal_card(), index)
                        player.hit(deck.deal_card(), len(player.get_hands()) - 1)
                    else:
                        if deck.card_values[player.get_hand(index)[0]] != deck.card_values[player.get_hand(index)[1]]:
                            print("You can only split hands of equal value.")
                        elif len(player.get_hand(index)) > 2:
                            print("You can only split an initial hand of two cards.")
                        else:
                            print("Your balance is insufficient to split your hand.")

            elif player_choice == 'F':
                if len(player.get_hand(index)) == 2 and len(player.get_hands()) == 1:
                    print("You chose to surrender. Half your bet is returned.")
                    player.balance += player.total_bet // 2
                    results.append("loss")
                    index+=1
                else:
                    print("You can only surrender your initial hand.")
            else:
                print("Invalid choice. Please choose again.")
        if results:
            return results

def dealer_turn(deck, dealer):
    print("\nDealer's turn.")
    dealer.show_hand()

    while dealer.calculate_hand_value(dealer.get_hand()) < 17:
        dealer.hit(deck.deal_card())
        dealer.show_hand()

def determine_winner(player, dealer, result, index):
    player_value = player.calculate_hand_value(player.get_hand(index))
    dealer_value = dealer.calculate_hand_value(dealer.get_hand())
    if result == "blackjack":
        print("Blackjack! Player wins 3:2")
        player.balance += int(player.total_bet + (player.total_bet * 1.5))
    elif result == "draw":
        if dealer_value == 21 and player.insurance_bet > 0:
            print("Dealer has blackjack, insurance bet wins!")
            player.balance += player.insurance_bet*3
        elif player_value > 21:
            print("Dealer wins. Player busts.")
        elif dealer_value > 21 or player_value > dealer_value:
            print("Player wins!")
            player.balance += player.total_bet*2
        elif player_value == dealer_value:
            print("It's a tie!")
            player.balance += player.total_bet
        else:
            print("Dealer wins.")
    else:
        print("Dealer wins.")

    print(f"Player balance: {player.balance}")

def start_blackjack():
    print("Welcome to Blackjack!")

    player = Player(name="Player")
    dealer = Dealer()


    player.balance = get_valid_input("Please select your starting balance: (1000 - 1000000): ", range(1000, 1000001))
    play_blackjack(player, dealer)

def play_blackjack(player, dealer):
    deck = Deck(deck_count=6)
    initial_deck_count = len(deck.cards)
    while player.balance > 0 and len(deck.cards) > int(initial_deck_count * .33):

        player.place_bet(get_valid_input("Please select your bet size: (10 - 1000): ", range(10, 1001)))
        initial_deal(deck, player, dealer)

        player_result = player_turn(deck, player, dealer)

        for index in range(len(player_result)):
            if player_result[index] == "draw":
                dealer_turn(deck, dealer)

            determine_winner(player, dealer, player_result[index], index)
        player.reset_hand()
        dealer.reset_hand()

    print("The deck will be reshuffled")
    play_blackjack(player, dealer)


# Start the game
start_blackjack()
