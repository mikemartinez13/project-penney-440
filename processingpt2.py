import numpy as np
import pandas as pd
import time
from itertools import product
import random
import os
from typing import List, Tuple

def generate_sequence(seed: int, seq: list) -> str:
    '''Takes unshuffled deck as input and outputs string version of shuffled deck.'''
    np.random.seed(seed)
    np.random.shuffle(seq)
    return ''.join(map(str, seq))

def generate_data(n):
    '''Takes in number of simulations to be run, and shuffles deck n times'''
    if(os.path.exists("data/deck_data.npy")):
        deck_data = np.load("data/deck_data.npy", allow_pickle=True)
    else:
        deck_data = np.zeros((0, 2))
    seed = deck_data.shape[0]  # seeds = run number (i.e. length)
    sequence = [1] * 26 + [0] * 26  # 26 black and red cards
    
    for x in range(n):
        np.random.seed(seed)
        shuffled_deck = generate_sequence(seed, sequence)
        new_row = np.array([seed, shuffled_deck], dtype=object)
        deck_data = np.vstack([deck_data, new_row])
        seed += 1

    np.save("data/deck_data.npy", deck_data)
    
##########################
######## Testing #########
##########################

if __name__ == "__main__":
    start_time = time.time()
    generate_data(1000000)
    end_time = time.time()
    print(end_time - start_time)


# Function to take in a sequence of cards and return the scores for both players
def run_game(sequence:List[str], p1_seq:str, p2_seq:str) -> Tuple[int, int]:
    if p1_seq == p2_seq:
        return 0, 0, 0, 0
    stack = ''
    p1score_trick, p1score_cards, p2score_trick, p2score_cards = 0, 0, 0, 0

    for card in bin(sequence)[2:]:
        stack += card
        curstack = stack[-3:]
        if curstack == p1_seq:
            p1score_trick += 1
            p1score_cards += len(stack)
            stack = ''
        elif curstack == p2_seq:
            p2score_trick += 1
            p2score_cards += len(stack)
            stack = ''

    return p1score_trick, p2score_trick, p1score_cards, p2score_cards


# Function to simulate a number of games, ngames.
def sim(ngames: int) -> pd.DataFrame:
    start = time.time()

    patterns = [
        '111', '110', '101', '100', '011', '010', '001', '000'
    ]
    
    rcards = '1' * 26 
    bcards = '0' * 26
    cards = rcards + bcards  # total 52 cards
    results = np.empty((ngames * len(patterns) ** 2, 8), dtype=object)
    
    index = 0
    for seed in range(ngames):
        random.seed(seed)
        ndeck = ''.join(random.sample(cards, len(cards)))  
        
        for p1guess, p2guess in product(patterns, patterns):
            result = run_game(ndeck, p1guess, p2guess)
            results[index] = [seed, ndeck, p1guess, p2guess, *result]
            index += 1
    
    end = time.time()
    print(f"Simulation time: {round((end - start), 4)} seconds")
    
    return results
