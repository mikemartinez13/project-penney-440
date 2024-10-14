import numpy as np
import time
import os

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
    
##########################
######## Testing #########
##########################

if __name__ == "__main__":
    start_time = time.time()
    generate_data(1000000)
    end_time = time.time()
    print(start_time - end_time)
