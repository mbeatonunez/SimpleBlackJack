#!usr/bin/env python3
'''
Milestone Project 2: Simple Black Jack game on python using OOP. 
Classes are based on example's from Jose Portilla's Python 3 Bootcamp Udemy course.
'''

import random
# enable this line if runing on Jupyter
#from IPython.display import clear_output

#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

# defines the minimum betting ammount, and dealer pot size, changing this changes the lenght of the game
min_bet = 5
dealer_pot = 100
dealer_name = 'The Dealer'

# define the components of a deck
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}

#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


# create a card class
class Card:
    '''Card Class Object containing the rank, suit and value of individual cards on a standard 52 card deck.'''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


# creat a Dec class
class Deck:
    '''Deck Class Object composed of a list of Card Class Objects'''
    def __init__(self):
        self.all_cards = []
        # create cards using the global variables defined above
        for suit in suits:
            for rank in ranks:
                # create the Card Object
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    # shuffles deck
    def shuffle(self):
        random.shuffle(self.all_cards)

    # deals one card
    def deal_one(self):
        return self.all_cards.pop(0)

    # deal the initial hand of 2 cards.
    def deal_hand(self):
        hand = []
        for i in range(2):
            hand.append(self.all_cards.pop(0))
        return hand

    # adds the discared cards to the bottom of the deck at the end of every round
    def add_to_bottom(self, discard):
        self.all_cards.extend(discard)


class Player:
    '''Player Class Object containing the player's name and available betting funds '''
    def __init__(self, name, funds):
        self.name = name.title()  # capitalize name. Using title in case of full name
        self.funds = funds  # initial funds for betting
        self.hand = []  # hand to be played
        self.hand_total = 0  # total value of hand
        self.bet = 0  # betting ammount
        self.stand = False  # refuses to add card to deck

    # displays the hand
    def print_hand(self):
        print(f"{self.name}'s hand: total {self.hand_total}", *self.hand,sep='\n    ')
    
    # adds up the total value of the hand in play        
    def get_total(self):
        self.hand_total = 0                 # resets the total to get new total
        has_ace = 0                         # number of Ace's in the hand
        for card in self.hand:
            self.hand_total += card.value  # add the value of the card to total
            if card.rank == 'Ace':
                has_ace += 1
        for i in range(has_ace):            # change the value of Ace from 11 to 1 if it makes the player bust.
            if self.hand_total > 21:        # The loop compensated for multiple Ace's
                self.hand_total -= 10

    # magic method to be displayed when the Player object is printed
    def __str__(self):
        return f'{self.name} has ${self.funds} in the pot.'


def create_player():
    '''Creates a Player object containing a name and funds'''
    p1_name = input("Hello Player, what is your name?: ")
    p1_funds = 0
    # ask for starting funds
    while True:
        try:
            p1_funds = int(input(f"OK, {p1_name.title()}. How much money is in your pot? "))
        except:
            print("Invalid entry. Please enter a proper ammount")
        else:
            break
    return Player(p1_name, p1_funds)


def get_bet(player):
    '''Asks player for betting ammount'''
    ammount = ''
    while True:
        try:
            ammount = abs(
                int(input(f"Enter a bet ammount no less than ${min_bet}: ")))
            if ammount > player.funds:
                print(f"Insuficient funds. You only have ${player.funds} in your pot")
                continue
            elif ammount < min_bet:
                print(f"Ammount is too low. Please enter an ammount of at least ${min_bet}.")
                continue
        except:
            print("Invalid entry. Try again.")
        else:
            break
    player.bet = ammount


def player_hit():
    '''Asks the player if he wants to be dealt another card'''
    print("Would you like to hit?")
    choise = ''
    while choise not in ["Y", "N"]:
        choise = input("Y or N: ").upper()
        if choise not in ["Y", "N"]:
            print("Invalid entry. Try again.")
        elif choise == 'Y':
            return True
    return False


def ai_hit(ai_player, player):
    '''defines AI behaviour. The choises are arbitrary, based on my own amateur playing style.'''
    if ai_player.hand_total < 20 and ai_player.hand_total >= 15:
        # don't hit if dealer is ahead of player
        if ai_player.hand_total > player.hand_total or player.hand_total == ai_player.hand_total:
            return False
    # don't hit if dealer is at 17 or greater (soft 17?)
    if ai_player.hand_total >= 17:
        return False
    # hit if total grater than 19 and the above is false
    return True

def keep_playing():
    '''Asks Player is they want to continue playing or end the game'''
    print("Keep playing? ")
    choise = ''
    while choise not in ["Y", "N"]:
        choise = input("Y or N: ").upper()
        if choise not in ["Y", "N"]:
            print("Invalid entry. Try again.")
        elif choise == 'Y':
            return True
    return False

def intro():
  print("# # # # # # # # # # # # # # # # # # # # # #")
  print("#                                         #")
  print("#           Welcome to BlackJack          #")
  print("#                                         #")
  print("# Introduction:                           #")
  print("# 1)You play against an AI dealer.        #")
  print("# 2)The first one to get to 21 wins.      #")
  print("# 3)Or the one with the bigger hand wins. #")
  print("# 4)if you bust, you lose.                #")
  print("# 5)The game continues until you quit or  #")
  print("#   run out of funds.                     #")
  print("#                                 Enjoy!  #")
  print("# # # # # # # # # # # # # # # # # # # # # #")

def main():
    # display intro
    intro()
    # creates and shuffles a new deck of 52 cards
    new_deck = Deck()
    new_deck.shuffle()

    # create player
    player_one = create_player()

    # create dealer
    dealer = Player(dealer_name, dealer_pot)

    round_num = 0

    while True:

        print(" ")
        #clear_output()
        # track number of rounds
        round_num += 1
        print(f'Round {round_num}')

        # re-shuffle deck after 10 rounds
        if round_num % 10 == 0:
            print("Suffling Deck")
            new_deck.shuffle()

        # print player's current standing
        print(player_one)
        print(dealer)

        # check for funds to continue playing
        if player_one.funds < 5:
            print("Game Over!")
            print(f"{player_one.name} does not have the funds to continue.")
            break
        if dealer.funds < 5:
            print("Game Over!")
            print("The House does not have the funds to continue.")
            break

        # deal hand from deck
        player_one.hand = new_deck.deal_hand()
        dealer.hand = new_deck.deal_hand()

        # total value of deck
        player_one.get_total()
        dealer.get_total()

        # ask for bet
        get_bet(player_one)
        print("")

        # display initial hands
        print(f"{dealer.name}'s hand: ")
        print(f"    {dealer.hand[0]}\n    and a hidden card")
        print(f"{player_one.name}'s hand: total {player_one.hand_total}")
        print(f"    {player_one.hand[0]}\n    {player_one.hand[1]}")

        while True:
            # check if win
            if player_one.hand_total == 21:
                print(f"{player_one.name} wins with 21.")
                print(f"{player_one.name} gets ${player_one.bet}")
                # distribute the bet
                player_one.funds += player_one.bet
                dealer.funds -= player_one.bet
                break

            # ask player to hit
            if player_hit():
                player_one.hand.append(new_deck.deal_one())
                print(f"{player_one.name} gets a {player_one.hand[-1]}")
            else:
                print(f'{player_one.name} stands.')
                player_one.stand = True
            # get new total
            player_one.get_total()

            # check player bust
            if player_one.hand_total > 21:
                print(f"{player_one.name} has Busted! Total: {player_one.hand_total}")
                print(f"The House gets ${player_one.bet}")
                # distribute the bet
                player_one.funds -= player_one.bet
                dealer.funds += player_one.bet
                break

            # check if win
            if dealer.hand_total == 21:
                print(f"{dealer.name} wins with 21.")
                print(f"The House gets ${player_one.bet}")
                # distribute the bet
                player_one.funds -= player_one.bet
                dealer.funds += player_one.bet
                break

            # dealer hit logic
            if ai_hit(dealer, player_one):
                dealer.hand.append(new_deck.deal_one())
                print(f"{dealer.name} gets a {dealer.hand[-1]}")
            else:
                print(f"{dealer.name} stands.")
                dealer.stand = True
            input('Press Enter to continue...')

            # get new dealer total
            dealer.get_total()

            # clear screen and display the hand
            print(" ")
            #clear_output()
            dealer.print_hand()
            player_one.print_hand()
            print("")

            # check dealer bust
            if dealer.hand_total > 21:
                print(f"{dealer.name} has Busted! Total: {dealer.hand_total}")
                print(f"{player_one.name} gets ${player_one.bet}")
                # distribute the bet
                player_one.funds += player_one.bet
                dealer.funds -= player_one.bet
                break

            # check win conditions if both players stand
            if dealer.stand and player_one.stand:
                if dealer.hand_total > player_one.hand_total:
                    print(f"{dealer.name} wins, {dealer.hand_total} to {player_one.hand_total}.")
                    print(f"The House gets ${player_one.bet}")
                    # distribute the bet
                    player_one.funds -= player_one.bet
                    dealer.funds += player_one.bet
                    break
                elif dealer.hand_total < player_one.hand_total:
                    print(f"{player_one.name} wins, {player_one.hand_total} to {dealer.hand_total}.")
                    print(f"{player_one.name} gets ${player_one.bet}")
                    # distribute the bet
                    player_one.funds += player_one.bet
                    dealer.funds -= player_one.bet
                    break
                else:
                    print("Tie. No winner!")
                    break

        # return cards to the bottom of the deck
        new_deck.add_to_bottom(player_one.hand)
        new_deck.add_to_bottom(dealer.hand)

        if keep_playing():
            continue
        else:
            print("Good Bye!")
            break


if __name__ == '__main__':
    main()
