# Project Penny
## Mike Martinez, Annamarie Warnke, Zoe Cummings, David Cho, Claire Kolman, Kirin Mackey

** The main branch is the most up to date branch, other branches were used for development **

To run this simulation and visualization you must download main.ipynb, penney_db1.py, visualization.py, simulation.py, and play.py. In this same directory, you must have a folder named ‘data’ to hold the database files, and a folder named ‘figures’ that stores the images depicting the results of Penney’s Game.

In our game, a **red card is denoted as 1 and a black card is denoted as 0**. The final visualization depicts the probabilities Player 1 wins based on each unique combination of their guess and Player 2’s guess. It also accounts for the methods of winning, those being by card amount and trick amount.

To start the game with no prior data, the user must use the function `play(path, n, seed=0)`. The variable `path` is a string representing the path to the database. If the file already exists, the function will append to the existing database. For our structure, the path must start with “data/”. The variable `n` is the number of iterations of the game to be played, and `seed` is an integer describing which random seed to use. Our implementation has the seed = 0, so if the user does not specify a seed, they can replicate our results. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated.
In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck. 

In `play(path, n_games, seed=0)`:
In `sim(n, seed)`:
* A “deck of cards” is instantiated, where red cards are represented by “1’s” and black cards are represented by “0’s”. The first deck is instantiated with 26 “1”s + 26 “0”s as a string
* Variable n decides the number of “games” played, and the deck is shuffled according to the seed.
* For every deck created, the function `run_game()` is played for each combination of guesses possible, where a winner is determined and listed in an array. If the guesses for Player 1 and Player 2 are the same the game results in an immediate tie. 
* sim(n, seed) then returns a list of lists. Each lists contains data for columns describing random seed number, the deck used (stored as an integer), Player 1’s guess, Player 2’s guess, p1_num_tricks, p2_num_tricks, win_tricks, and then same for cards
* A function called make_database() is called on the lists of lists, where it is translated into a pandas dataframe. A database named using the user-specified path is then created by the `make_database()` function and added to the folder called data. If the database has already been created it appends the data from the pandas dataframe into the existing database.

To visualize all the data from all the iterations, or decks, played, the user then must call the function `heatmap('data/database_name.db')`, where `'data/database_name.db'` is the path to the database to be modeled in a string format.  If the user has different data than the database file created by `sim(n, seed)` they must have a database file located in the data folder where the columns are named and have data as follows:
* The table name must be named ‘win_results’
* seed: an integer describing the random seed used to shuffle the decks
*deck: integer representation of the deck used for each game 
* p1_seq: A string of 3 characters either 1 or 0 (ex. 111) representing Player 1’s guess.
* p2_seq: A string of 3 characters either 1 or 0 (ex. 111) representing Player 2’s guess.
* p1_num_tricks: An integer describing how many tricks Player 1 won.
* p2_num_trickst: An integer describing how many tricks Player 2 won.
* win_tricks: A string either ‘p1,’ ‘p2,’ or ‘T’ denoting who won the individual game using trick amounts to determine a winner.
* p1_num_cards: An integer describing how many cards Player 1 won.
* p2_num_cards: An integer describing how many cards Player 2 won.
* win_cards: A string either ‘p1,’ ‘p2,’ or ‘T’ denoting who won the individual game using trick amounts to determine a winner.

By executing `heatmap(‘data/database_name.db’)`:
* The function connects to the database file whose path was passed in a string.
* The probabilities of Player 1 winning either by card amount or trick amount are calculated for each possible combination of guesses from Player 1 and Player 2. The number of iterations, or decks, is also found. 
* Two 8 x 8 arrays are created, each pertaining to a win method. These hold the probabilities Player 1 wins corresponding to each combination of guesses between Player 1 and Player 2.
* A dictionary is made holding the 8 x8 array pertaining to Player 1 winning by trick amount probabilities , the 8 x 8 holding the array pertaining to Player 1 winning by card amount probabilities, and n amount of times the simulation has been run.
* The `create_viz()` function is called on the dictionary created, where 2 subplots are made corresponding to the different variations of winning for Player 1. It shows and creates an image named ‘heatmap_n(number of decks).png’ where (number of decks) is the number n passed in by the dictionary. This image file is then moved to the folder named figures.
