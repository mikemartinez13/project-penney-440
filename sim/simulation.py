import time
import numpy as np
import random

from typing import List, Tuple
from itertools import product
import pandas as pd
from functools import wraps

# Decorator to time the function execution
def time_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the actual function
        end_time = time.time()  # Record the end time
        elapsed_time = round(end_time - start_time, 4)
        print(f"Function '{func.__name__}' executed in {elapsed_time} seconds.")
        return result  # Return the result of the original function
    return wrapper

# Function to take in a sequence of cards and return the scores for both players
def run_game(sequence:List[str], p1_seq:str, p2_seq:str) -> Tuple[int,int]: 
    if p1_seq == p2_seq:
        return 0, 0, 'T', 0, 0, 'T' # if both players guess the same, return tie
    stack = ''
    p1score_trick,p1score_cards,p2score_trick,p2score_cards = 0,0,0,0

    for card in format(sequence, '052b'):
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

    trick_outcome = 'p1' if p1score_trick > p2score_trick else 'p2' if p2score_trick > p1score_trick else 'T'
    cards_outcome = 'p1' if p1score_cards > p2score_cards else 'p2' if p2score_cards > p1score_cards else 'T'
    
    return p1score_trick, p2score_trick, trick_outcome, p1score_cards, p2score_cards, cards_outcome # (if positive, p1 won. If negative, p2 won. If 0, tie)


# Function to simulate a number of games, ngames.
def sim(ngames: int, seed: int) -> pd.DataFrame:

    # Store the deck as a string of 1s and 0s or an integer. 
    # 1s represent red cards and 0s represent black cards.
    # Test at larger scale and see if it can handle the operations. 

    random.seed(seed)
    
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
    # results = np.empty((ngames * len(patterns) ** 2, 8), dtype=object)
    results = np.empty((ngames * len(patterns) ** 2, 10), dtype=object)
    
    index = 0
    for _ in range(ngames):

        ndeck = int(''.join(random.sample(cards, len(cards), )), 2)  # Use cards.copy() to keep the original list intact
        
        for p1guess, p2guess in product(patterns, patterns):
            result = run_game(ndeck, p1guess, p2guess)
            results[index] = [seed, ndeck, p1guess, p2guess, *result]
            index += 1
    
    return results

def make_database(simulation):
    db = DB()
    db.connect_db()
    db.insert_results(simulation)
    return db.get_database_file()


##########################
######## Testing #########
##########################

if __name__ == "__main__":
    # final_old = sim(ngames = 1000)
    # final_new = optimized_sim(ngames = 1000)
    res = time_function(sim)(ngames=1000, seed=0)  # Call the sim function with timing

    print(res[0])
