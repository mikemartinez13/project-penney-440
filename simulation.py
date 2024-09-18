import time
import numpy as np
import random
import re
from typing import List, Tuple
from itertools import product
import pandas as pd

def run_game(sequence:List[str], p1_seq:str, p2_seq:str) -> Tuple[int,int]: 
    if p1_seq == p2_seq:
        return 0, 0, 'T', 0, 0, 'T'
    stack = ''
    p1score_trick,p1score_cards,p2score_trick,p2score_cards = 0,0,0,0

    for card in sequence:
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

def sim(ngames: int) -> pd.DataFrame:
    start = time.time()

    rcards = ['1'] * 26 
    bcards = ['0'] * 26
    cards = rcards+bcards # total 52 cards
    #total = np.empty((ngames, 52), dtype='<U1')
    #seeds = np.empty((ngames,52))
    total = []
    for gamenum in range(ngames):
        random.seed(gamenum)
        #seeds[gamenum] = gamenum
        total.append(random.sample(cards, len(cards)))  # Use cards.copy() to keep the original list intact
    
    df = pd.DataFrame({'Decks':total})
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
    type = [
        'trick',
        'cards'
    ]
    
    p_df = pd.DataFrame(patterns, columns=['patterns'])
    pattern_df = p_df.merge(p_df, how = 'cross')
    pattern_df.rename(columns={'patterns_x':'p1guess','patterns_y':'p2guess'},inplace=True)
    game_df = df.merge(pattern_df, how = 'cross')
    
    scores_series = game_df.apply(lambda x: run_game(x.Decks,x.p1guess,x.p2guess), axis=1)
    scores_df = pd.DataFrame(scores_series.to_list(), columns = ['p1tricks','p2tricks',
                                                                 'trick_outcome','p1score_cards', 
                                                                 'p2score_cards', 'cards_outcome'])
    
    final_df = pd.concat([game_df,scores_df], axis=1)
    
    end = time.time()
    print(round((end - start),4))

    return final_df

    
def optimized_sim(ngames: int) -> pd.DataFrame:
    start = time.time()
    
    rcards = ['1'] * 26 
    bcards = ['0'] * 26
    cards = rcards+bcards # total 52 cards
    #total = np.empty((ngames, 52), dtype='<U1')
    #seeds = np.empty((ngames,52))
    results = []
    
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
    
    for gamenum in range(ngames):
        random.seed(gamenum)
        #seeds[gamenum] = gamenum
        ndeck = random.sample(cards, len(cards))  # Use cards.copy() to keep the original list intact
        
        for p1guess, p2guess in product(patterns, patterns):
            result = run_game(ndeck, p1guess, p2guess)
            results.append((ndeck, p1guess, p2guess, *result))
    
    final_df = pd.DataFrame(results, columns=['Deck', 'p1guess', 'p2guess',
                                              'p1tricks', 'p2tricks', 'trick_outcome',
                                              'p1cards', 'p2cards', 'cards_outcome'])
    
    end = time.time()
    print(round((end - start),4))
    
    return final_df

def test_sim(ngames: int) -> pd.DataFrame:
    start = time.time()

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
    results = np.empty((ngames * len(patterns) ** 2, 9), dtype=object)
    #seeds = np.empty((ngames,52))
    #results = []
    
    
    index = 0
    for gamenum in range(ngames):
        random.seed(gamenum)
        #seeds[gamenum] = gamenum
        ndeck = random.sample(cards, len(cards))  # Use cards.copy() to keep the original list intact
        
        for p1guess, p2guess in product(patterns, patterns):
            result = run_game(ndeck, p1guess, p2guess)
            results[index] = [ndeck, p1guess, p2guess, *result]
            index += 1
    
    # final_df = pd.DataFrame(results, columns=['Deck', 'p1guess', 'p2guess',
    #                                           'p1tricks', 'p2tricks', 'trick_outcome',
    #                                           'p1cards', 'p2cards', 'cards_outcome'])
    
    end = time.time()
    print(round((end - start),4))
    
    return results


##########################
######## Testing #########
##########################

if __name__ == "__main__":
    final_old = sim(ngames = 100)
    final_new = optimized_sim(ngames = 100)
    final_test = test_sim(ngames = 100)

    print(final_test)

