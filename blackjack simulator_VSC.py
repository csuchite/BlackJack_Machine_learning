# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random 
import multiprocessing
import math
import time

simulations = 900000
num_decks = 4
shuffle_percent = 75

# Create the loop for multiple decks

def simulate(queue, batch_size):
    deck = []
    
    def new_deck():
        std_deck = [
            # 2 3 4 5 6 7 8 9 10 10 10 10 11
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        ]
        
        std_deck = std_deck * num_decks
        
        random.shuffle(std_deck)
        
        return std_deck[:]
    
        def play_hand():
            dealer_cards = []
            player_cards = []

# The initial cards dealt to player and dealer

        player_cards.append(deck.pop(0))
        dealer_cards.append(deck.pop(0))
        player_cards.append(deck.pop(0))
        dealer_cards.append(deck.pop(0))

# Dealt cards to players that amount to 12 or higher

        while sum(player_cards) < 12:
            player_cards.append(deck.pop(0))

# The dealer got dealt cards that is soft 17 means: dealer has to get another card

        while sum(dealer_cards) < 18:
            exit = False
            if sum(dealer_cards) == 17:
                exit = True
                
                for i, card in enumerate(dealer_cards):
                    if card == 11:
                        exit = False
                        dealer_cards[i] = 1
                        
            if exit:
                break
                
            dealer_cards.append(deck.pop(0))

#  The sum of the card values for the player and dealer

        player_sum = sum(player_cards)
        dealer_sum = sum(dealer_cards)

# The dealer bust and player wins when the values of the cards are over 21 (dealer bust/loss)

        if dealer_sum > 21:
            return 1;

#  The sum of the dealer cards' value are tied or push with player (dealer tie)

        if dealer_sum == player_sum:
            return 0;

#  The sum of the dealer cards' value are greater that the player (dealer win)

        if dealer_sum > player_sum:
            return -1;
        
# The sum of the dealer cards' value are less that the player dealer loss)
        if dealer_sum < player_sum:
            return 1

# Start a new deck

    deck = new_deck()
    
    win = 0
    tie = 0
    lose = 0
    
    for i in range(0, batch_size):

# Shuffle the cards when the percentage of cards are at 25% or less

        if (float(len(deck)) / (52 * num_decks)) * 100 < shuffle_percent:
            deck = new_deck()

# Play the hand randomly dealt

            result = play_hand()

# Save the results 

            if result == 1:
                win += 1
            if result == 0:
                tie += 1
            if result == -1:
                lose +=1
                
    queue.put([win, draw, lose])
    
start_time = time.time()

cpus = multiprocessing.cpu_count()
batch_size = int(math.ceil(simulations / float(cpus)))

queue = multiprocessing.Queue()

processes = []

for i in range(0, cpus):
    process = multiprocessing.Process(target=simulate, args=(queue, batch_size))
    processes.append(process)
    process.start()
    
for proc in processes:
    proc.join()
    
finish_time = time.time() - start_time

win = 0
tie = 0
lose = 0

for i in range(0, cpus):
    results = queue.get()
    win += results[0]
    tie += results[1]
    lose += results[2]
    
print(f'Cores used: %d' % cpus)
print(f'Total simulations: %d' % simulations)
print(f'Total simulations / time: %d' % (float(simulations) / finish_time))
print(f'execution time : %.2fs' % finish_time)
print(f'Win Percentage: %.2fs%%' % ((win / float(simulations)) * 100))
print(f'Tie Percentage: %.2fs%%' % ((tie / float(simulations)) * 100))
print(f'Loss Percentage: %.2fs%%' % ((loss / float(simulations)) * 100))