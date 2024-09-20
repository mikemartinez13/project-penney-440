import pandas as pd
from itertools import product
from simulation import sim

# Function to calculate win probabilities for all 64 combinations
def calculate_probabilities():
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

    # Loop through all combinations of Player 1 and Player 2 guesses
    for p1guess, p2guess in product(patterns, patterns):
        # Run the simulation for each combination
        sim_results = sim(ngames=1000)
        
        # Convert the results into a DataFrames its easier to process and view the results
        columns = ['Seed', 'Deck', 'P1_Guess', 'P2_Guess', 'P1_Trick_Score', 'P2_Trick_Score',
                   'Trick_Outcome', 'P1_Card_Score', 'P2_Card_Score', 'Card_Outcome']
        df = pd.DataFrame(sim_results, columns=columns)
        
        # Get only the results I want (probability)
        filtered_df = df[(df['P1_Guess'] == p1guess) & (df['P2_Guess'] == p2guess)]
        
        # Calculate Probabilities for Card Amount
        p1probcards = filtered_df['Card_Outcome'].value_counts().get('p1', 0) / len(filtered_df)
        p2probcards = filtered_df['Card_Outcome'].value_counts().get('p2', 0) / len(filtered_df)
        tieprobcards = filtered_df['Card_Outcome'].value_counts().get('T', 0) / len(filtered_df)
        
        # Calculate Probabilities for Trick Amount
        p1probtricks = filtered_df['Trick_Outcome'].value_counts().get('p1', 0) / len(filtered_df)
        p2probtricks = filtered_df['Trick_Outcome'].value_counts().get('p2', 0) / len(filtered_df)
        tieprobtricks = filtered_df['Trick_Outcome'].value_counts().get('T', 0) / len(filtered_df)
        
        results.append({
            'P1_Guess': p1guess,
            'P2_Guess': p2guess,
            'V1 P1 Win Probability': p1probcards,
            'V1 P2 Win Probability': p2probcards,
            'V1 Tie Probability': tieprobcards,
            'V2 P1 Win Probability': p1probtricks,
            'V2 P2 Win Probability': p2probtricks,
            'V2 Tie Probability': tieprobtricks
        })
    
    return pd.DataFrame(results)
    #return results

# Calculating probabilities for all 64 combinations
calculate_probabilities()
