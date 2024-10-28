import numpy as np
import random
import json
from typing import List, Tuple
from itertools import product
##Using simulation functions, generate_sequence and generate_data
def generate_sequence(seed: int, seq: list) -> str:
    '''Takes unshuffled deck as input and outputs string version of shuffled deck.'''
    np.random.seed(seed)
    np.random.shuffle(seq)
    return ''.join(map(str,seq))

def generate_data(n):
    '''Takes in number of simulations to be run, and shuffles deck n times'''
    if(os.path.exists("data/deck_data.npy")):
        deck_data = np.load("data/deck_data.npy", allow_pickle = True)
    else:
        deck_data = np.zeros((0, 2))
    seed = deck_data.shape[0] # seeds = run number (i.e. length)
    sequence = [1] * 26 + [0] * 26 # 26 black and red cards
    
    for x in range(n):
        np.random.seed(seed)

        shuffled_deck = generate_sequence(seed, sequence)
        
        new_row = np.array([seed, shuffled_deck], dtype=object)
        deck_data = np.vstack([deck_data, new_row])
        seed+=1

    np.save("data/deck_data.npy", deck_data)
    return np.array(deck_data, dtype=object)

def run_game(sequence: int, p1_seq: str, p2_seq: str) -> Tuple[int, int, str, int, int, str, int, int]:
    if p1_seq == p2_seq:
        return 0, 0, 'T', 0, 0, 'T', 0, 0  # if both players guess the same, return tie
    stack = ''
    p1score_trick, p1score_cards, p2score_trick, p2score_cards = 0, 0, 0, 0

    for card in format(sequence, '052b'):
        stack += card
        curstack = stack[-3:]  # Check the last 3 cards
        if curstack == p1_seq:
            p1score_trick += 1
            p1score_cards += len(stack)
            stack = ''
        elif curstack == p2_seq:
            p2score_trick += 1
            p2score_cards += len(stack)
            stack = ''

    trick_outcome = 'p1' if p1score_trick > p2score_trick else 'p2' if p2score_trick > p1score_trick else 'T'
    cards_outcome = 'p1' if p1score_cards > p2score_cards else 'p2' if p2score_cards > p1score_cards else 'T'

    tie_card = 1 if cards_outcome == 'T' else 0
    tie_trick = 1 if trick_outcome == 'T' else 0

    return p1score_trick, p2score_trick, trick_outcome, p1score_cards, p2score_cards, cards_outcome, tie_card, tie_trick

def by_decks(deck_data: np.ndarray, patterns: List[str]) -> np.ndarray:
    results = []

    for seed, shuffled_deck in deck_data:
        for p1_seq in patterns:
            for p2_seq in patterns:
                result = run_game(int(shuffled_deck, 2), p1_seq, p2_seq)
                results.append([seed, shuffled_deck, p1_seq, p2_seq, *result])

    return np.array(results, dtype=object)