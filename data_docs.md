# Data Management and Simulation
### Authored by Mike Martinez, Annamarie Warnke, Zoe Cummings, David Cho

Documentation for functions in `simulation.py`:

## Main Functions

### `play`

**Parameters:**
- `n` (`int`): Number of simulations to run.

**Returns:**
- `np.ndarray`: An array of game results for each seed and pair of player sequences.

**Description:**
The `play` function is the main function for the user. It runs simulations for each shuffled deck in `deck_data` across all possible combinations of player sequences provided in `patterns` using the `generate_data(n)` function. For each deck, it iterates through every pair of Player 1 and Player 2 sequences, runs a game using `run_game`, and collects the results. The aggregated results are returned as a NumPy array, capturing outcomes for each game simulation, and are also stored in `"data/deck_data.npy"`. Finally, the function calls the `calculate_probabilities` function on the resulting array, which stores the final probabilities for the 64 outcomes in a `"results/results.json"` file within the `"results/"` directory. 

---

## Helper Functions from `simulation.py`:

### `generate_sequence`

**Parameters:**
- `seed` (`int`): The random seed to initialize the NumPy random number generator.
- `seq` (`list`): The unshuffled deck sequence represented as a list of integers (e.g., `[1]*26 + [0]*26`).

**Returns:**
- `str`: A string representing the shuffled deck.

**Description:**
The `generate_sequence` function takes an unshuffled deck as input, shuffles it using the provided seed, and returns a string representation of the shuffled deck. It ensures reproducibility by setting the NumPy random seed before shuffling.

### `generate_data`

**Parameters:**
- `n` (`int`): The number of simulations to run, indicating how many times the deck will be shuffled.

**Returns:**
- `np.ndarray`: An array containing the seed and corresponding shuffled deck data for each simulation.

**Description:**
The `generate_data` function generates shuffled deck data for a specified number of simulations (`n`). It checks if a data file (`deck_data.npy`) already exists; if so, it loads the existing data and appends new simulations. For each simulation, it shuffles a standard deck of 52 cards (26 represented by `1` and 26 by `0`) using a unique seed, and saves the shuffled sequence along with the seed. The resulting data is saved in the `data/` directory as a NumPy binary file as `deck_data.npy`.

---

## Helper functions from `processing_updated.py`:

### `run_game`

**Parameters:**
- `sequence` (`int`): The shuffled deck sequence represented as an integer (binary format).
- `p1_seq` (`str`): Player 1's chosen sequence of three cards (e.g., `'111'`, `'110'`).
- `p2_seq` (`str`): Player 2's chosen sequence of three cards.

**Returns:**
- `Tuple[int, int, str, int, int, str, int, int]`: A tuple containing:
  - `p1score_trick` (`int`): Player 1's score based on tricks.
  - `p2score_trick` (`int`): Player 2's score based on tricks.
  - `trick_outcome` (`str`): Outcome of trick scoring (`'p1'`, `'p2'`, or `'T'` for tie).
  - `p1score_cards` (`int`): Player 1's score based on cards.
  - `p2score_cards` (`int`): Player 2's score based on cards.
  - `cards_outcome` (`str`): Outcome of card scoring (`'p1'`, `'p2'`, or `'T'` for tie).
  - `tie_card` (`int`): Indicator if the card scoring resulted in a tie (`1`) or not (`0`).
  - `tie_trick` (`int`): Indicator if the trick scoring resulted in a tie (`1`) or not (`0`).

**Description:**
The `run_game` function simulates a single game of Penney's Game using a given shuffled deck sequence. It iterates through the deck, updating a stack of the last three cards to check for the players' sequences. If a player's sequence is detected, scores are updated accordingly, and the stack is cleared. After processing the entire deck, the function determines the outcome based on trick and card scores, indicating whether Player 1 wins, Player 2 wins, or if there's a tie.

### `calculate_probabilities`

**Parameters:**
- `results` (`np.ndarray`): Array containing game results, including player sequences and outcomes.

**Returns:**
- `dict`: A dictionary mapping each pair of player sequences to their respective win and tie probabilities.

**Description:**
The `calculate_probabilities` function processes the aggregated game results to compute probabilities of Player 2 winning based on tricks and cards, as well as tie probabilities for both scoring methods. It iterates through each game result, updates counts for Player 2 wins and ties for each sequence pair, and finally calculates the probabilities by dividing the counts by the total number of games for each pair. The resulting probabilities are organized in a dictionary for easy access and analysis.


<!-- **Usage Example:**

```python
import heatmap_visualization as hv
import numpy as np

# Sample data
data1 = np.random.rand(8, 8)
data2 = np.random.rand(8, 8)
data1_ties = np.random.rand(8, 8)
data2_ties = np.random.rand(8, 8)
labels1 = hv.make_annots(hv.format_data(data1), hv.format_data(data1_ties))
labels2 = hv.make_annots(hv.format_data(data2), hv.format_data(data2_ties))

# Generate bundled heatmaps in PNG format
fig, ax = hv.make_heatmap_package(
    data1=data1,
    data2=data2,
    title1="Heatmap for Dataset 1",
    title2="Heatmap for Dataset 2",
    n1=1000,
    n2=1000,
    win_type1='cards',
    win_type2='tricks',
    data1_ties=data1_ties,
    data2_ties=data2_ties,
    labels1=labels1,
    labels2=labels2,
    letters=True,
    format='png'
)

# Generate bundled heatmaps in HTML format
html_fig = hv.make_heatmap_package(
    data1=data1,
    data2=data2,
    title1="Heatmap for Dataset 1",
    title2="Heatmap for Dataset 2",
    n1=1000,
    n2=1000,
    win_type1='cards',
    win_type2='tricks',
    data1_ties=data1_ties,
    data2_ties=data2_ties,
    labels1=labels1,
    labels2=labels2,
    letters=True,
    format='html'
)
html_fig.show() -->