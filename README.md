# Project Penny
## Mike Martinez, Annamarie Warnke, Zoe Cummings, David Cho, Claire Kolman, Kirin Mackey

**The main branch is the most up to date branch, other branches were used for development.**

To run this simulation and visualization you must download `main.ipynb`, `penney_db1.py`, `visualization.py`, `simulation.py`, and `play.py` from the main branch. In the same directory, you must have a folder named `data` to hold the database files, and a folder named `figures` that stores visualizations depicting simulation results. In `main.ipynb`, we used 30,000 decks. We found that 100,000 decks leads to the most accurate results, but GitHub cannot handle that size data file. The figure with 100,000 decks has been uploaded, but if the FLB would like the data with 100,000 decks he should contact Annamarie directly.

In our game, a **red card is denoted as 1 and a black card is denoted as 0**. The final visualization depicts the probabilities of Player 1 winning based on each unique combination of their guess and Player 2’s guess. It also accounts for the methods of winning, those being by card amount and trick amount.

To start the game with no prior data, the user must use the function `play(path, n, seed=0)`. The variable `path` is a string representing the path to the database. If the file already exists, the function will append to the existing database. For our structure, the path must start with “data/”. The variable `n` is the number of iterations of the game to be played, and `seed` is an integer describing which random seed to use. Our implementation has seed = 0, so if the user does not specify a seed, they can replicate our results. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck. 

In `play(path, n_games, seed=0)`:
* The function `sim(n, seed)` is called. A “deck of cards” is instantiated, where red cards are represented by “1"s and black cards are represented by “0”s. The first deck is instantiated with 26 “1”s and 26 “0”s as a string.
* Variable `n` decides the number of decks, and each deck is shuffled according to the seed.
* For every deck created, the function `run_game(sequence, p1_seq, p2_seq)` is played for each combination of guesses possible, where a winner is determined and listed in an array. If the guesses for Player 1 and Player 2 are the same the game results in an immediate tie. 
* The function `sim(n, seed)` then returns a list of lists. Each list contains data for columns. They describe the random seed number, the deck used (stored as an integer), Player 1’s guess, Player 2’s guess, number of tricks Player 1 won, number of tricks Player 2 won, the outcome of playing the game based on tricks, number of cards Player 1 won, number of cards Player 2 won, and the outcome of playing the game based on cards.
* A function called `make_database(results, path)` is called on the lists of lists (passed in as `results`), where it is translated into a pandas dataframe. A database named using the user-specified path (passed in as `path`) is then created and added to the folder called `data`. If the database has already been created it appends the data from the pandas dataframe into the existing database.

To visualize all the data from all the iterations, or decks, played, the user must call the function `heatmap('data/database_name.db')`, where `'data/database_name.db'` is the path to the database. If the user has different data than the database file created by `sim(n, seed)` they must have a database file located in the `data` folder where the columns are named and have data as follows:
* The table name must be named ‘win_results’
* `seed`: An integer describing the random seed used to shuffle the decks
* `deck`: An integer representation of the deck used for each game 
* `p1_seq`: A string of 3 characters either 1 or 0 (ex. 111) representing Player 1’s guess
* `p2_seq`: A string of 3 characters either 1 or 0 (ex. 111) representing Player 2’s guess
* `p1_num_tricks`: An integer describing how many tricks Player 1 won
* `p2_num_tricks`: An integer describing how many tricks Player 2 won
* `win_tricks`: A string either ‘p1,’ ‘p2,’ or ‘T’ denoting who won the individual game using trick amounts to determine a winner
* `p1_num_cards`: An integer describing how many cards Player 1 won
* `p2_num_cards`: An integer describing how many cards Player 2 won
* `win_cards`: A string either ‘p1,’ ‘p2,’ or ‘T’ denoting who won the individual game using card amounts to determine a winner

By executing `heatmap(‘data/database_name.db’)`:
* The function connects to the database file whose path was passed in.
* The probabilities of Player 1 winning either by card amount or trick amount are calculated for each possible combination of guesses from Player 1 and Player 2.
* The number of iterations, or decks, is found. 
* Two 8 x 8 arrays are created, each pertaining to a win method. These hold the probabilities of Player 1 winning for each combination of guesses between Player 1 and Player 2.
* A dictionary is made holding an 8 x 8 array with probabilities of Player 1 winning by trick amount, an 8 x 8 array with the probabilities of Player 1 winning by card amount, and n amount of times the simulation has been run.
* The `create_viz(dict)` function is called on the dictionary created, where 2 subplots are made corresponding to the different variations of Player 1 winning. It shows and creates an image named ‘heatmap_n(number of decks).png’ where (number of decks) is the number n passed in by the dictionary. This image file is then moved to the folder named `figures`.
