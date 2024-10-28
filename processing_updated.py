import numpy as np
import random
import json
from typing import List, Tuple
from itertools import product
import time
import os
import pandas as pd
from functools import wraps

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
    deck_data = np.array(deck_data, dtype=object)
    return deck_data

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

def play(n) -> np.ndarray:
    results = []
    patterns = ['111', '110', '101', '100', '011', '010', '001', '000']
    deck_data = generate_data(n)
    for seed, shuffled_deck in deck_data:
        for p1_seq in patterns:
            for p2_seq in patterns:
                result = run_game(int(shuffled_deck, 2), p1_seq, p2_seq)
                results.append([seed, shuffled_deck, p1_seq, p2_seq, *result])
    results= np.array(results, dtype=object)
    
    calculate_probabilities(results)

def calculate_probabilities(results: np.ndarray) -> dict:
    
    win_trick_counts = {}
    win_cards_counts = {}
    tie_trick_counts = {}
    tie_cards_counts = {}

    for row in results:
        p1_seq = row[2]
        p2_seq = row[3]
        p2_trick_outcome = row[6]
        p2_cards_outcome = row[9]
        
        key = f"{p1_seq}-{p2_seq}"
        
        if key not in win_trick_counts:
            win_trick_counts[key] = {'p2_wins': 0, 'total': 0}
            win_cards_counts[key] = {'p2_wins': 0, 'total': 0}
            tie_trick_counts[key] = 0
            tie_cards_counts[key] = 0

        # wins
        if p2_trick_outcome == 'p2':
            win_trick_counts[key]['p2_wins'] += 1
        if p2_cards_outcome == 'p2':
            win_cards_counts[key]['p2_wins'] += 1
        
        # ties
        if p2_trick_outcome == 'T':
            tie_trick_counts[key] += 1
        if p2_cards_outcome == 'T':
            tie_cards_counts[key] += 1
        
        win_trick_counts[key]['total'] += 1
        win_cards_counts[key]['total'] += 1  # Increment total for card outcomes

    # probabilities
    probabilities = {}
    for key in win_trick_counts.keys():
        total_trick_games = win_trick_counts[key]['total']
        total_card_games = win_cards_counts[key]['total']
        
        p2_win_trick_prob = win_trick_counts[key]['p2_wins'] / total_trick_games if total_trick_games > 0 else 0
        p2_win_card_prob = win_cards_counts[key]['p2_wins'] / total_card_games if total_card_games > 0 else 0
        
        #total_ties = tie_trick_counts[key] + tie_cards_counts[key]
        total_games = total_trick_games + total_card_games  # Total games is the sum of both

        tie_trick_prob = tie_trick_counts[key] / total_trick_games if total_games > 0 else 0
        tie_card_prob = tie_cards_counts[key] / total_card_games if total_games > 0 else 0

        probabilities[key] = {
            'p2_win_trick_probability': p2_win_trick_prob,
            'p2_win_card_probability': p2_win_card_prob,
            'tie_trick_probability': tie_trick_prob,
            'tie_card_probability': tie_card_prob
        }

    with open("player2_probabilities.json", "w") as prob_file:
        json.dump(probabilities, prob_file)



if __name__ == "__main__":
    play(10)
