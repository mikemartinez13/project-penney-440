import time
import numpy as np
import random
import re
from typing import List, Tuple
from itertools import product
import pandas as pd

# Function to take in a sequence of cards and return the scores for both players
def run_game(sequence:List[str], p1_seq:str, p2_seq:str) -> Tuple[int,int]: 
    if p1_seq == p2_seq:
        return 0, 0, 0, 0
    stack = ''
    p1score_trick,p1score_cards,p2score_trick,p2score_cards = 0,0,0,0

    for card in bin(sequence)[2:]:
        stack+=card
        curstack = stack[-3:]
        if curstack == p1_seq:
            p1score_trick+=1 # using "trick" method to count
            p1score_cards+=len(stack)
            stack = ''
        elif curstack == p2_seq:
            p2score_trick+=1
            p2score_cards+=len(stack)
            stack = ''
    
    return p1score_trick, p2score_trick, p1score_cards, p2score_cards # (if positive, p1 won. If negative, p2 won. If 0, tie)


# Function to simulate a number of games, ngames.
def sim(ngames: int) -> pd.DataFrame:
    start = time.time()

    # Store the deck as a string of 1s and 0s or an integer. 
    # 1s represent red cards and 0s represent black cards.
    # Test at larger scale and see if it can handle the operations. 

    patterns = [
        '111',
        '110',
        '101',
        '100',
        '011',
        '010',
        '001',
        '000'
    ]
    
    rcards = '1' * 26 
    bcards = '0' * 26
    cards = rcards+bcards # total 52 cards
    results = np.empty((ngames * len(patterns) ** 2, 8), dtype=object)
    
    
    index = 0
    for seed in range(ngames):
        random.seed(seed)

        ndeck = ''.join(random.sample(cards, len(cards)))  # Use cards.copy() to keep the original list intact
        
        for p1guess, p2guess in product(patterns, patterns):
            result = run_game(ndeck, p1guess, p2guess)
            results[index] = [seed, ndeck, p1guess, p2guess, *result]
            index += 1
    
    end = time.time()
    print(round((end - start),4))
    
    return results


##########################
######## Testing #########
##########################

if __name__ == "__main__":
    # final_old = sim(ngames = 1000)
    # final_new = optimized_sim(ngames = 1000)
    final_test = sim(ngames = 10000)
    print(final_test[0])

