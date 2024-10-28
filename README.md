# Project Penny
### Authored by Mike Martinez, Annamarie Warnke, Zoe Cummings, David Cho, Claire Kolman, Kirin Mackey

**The main-updated branch is the most up to date branch, other branches were used for development.**

Project Penney is a project designed to simulate Penney's Game, a game played between two players where each player chooses a sequence of three card colors (e.g. Red, Black, Black). Points are awarded to players if their sequence appears when pulling cards sequentially from a well-shuffled deck. Penney's Game is of interest because the probability of winning is not equal; if the second player learns the sequence chosen by the first player, they can follow a rule to optimize their chances of winning. More information can be found in [the Wikipedia page](https://en.wikipedia.org/wiki/Penney%27s_game). 

Note that our simulation runs two variations of Penney's Game, which have different rules: 
1. For version 1, players are scored based on the number of "tricks" they earn. For example, if a player's sequence "Red, Black, Black" appears, the deck is cleared and the player earns 1 point. 
2. For version 2, players are scored based on the number of cards they earn. If a player's sequence "Red, Black, Black" appears, the deck is cleared and the player earns _all_ the cards in the deck. 

To run the simulation, first clone the repository: 

```git clone https://github.com/mikemartinez13/project-penney-440.git```

Next, open "main.ipynb" and run all of the cells. Below is a list of functions and their parameters:

### `play(path, n, seed=0)` 
**Parameters:** 
- `path (str)` String of the path of where you would like to store your data
- `n (int)`, The number of games you would like to run,
- `seed (int)` The random seed to use. If none set, defaults to 0.

 The function stores data in a database format. If the database file already exists, the function will append to the existing database. For our structure, the data is stored in a `“data/”` folder. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck.

For more information on what exactly goes into the `play` function, check out the [data management documentation](data_mgmt.md)

### `heatmap(path)`
**Parameters:**
- `path (str)` String of the path where the database of decks is located. 



<!-- To run this simulation and visualization you must download `main.ipynb`, `penney_db1.py`, `visualization.py`, `simulation.py`, and `play.py` from the main branch. In the same directory, you must have a folder named `data` to hold the database files, and a folder named `figures` that stores visualizations depicting simulation results. In `main.ipynb`, we used 30,000 decks. We found that 100,000 decks leads to the most accurate results, but GitHub cannot handle that size data file. The figure with 100,000 decks has been uploaded, but if the FLB would like the data with 100,000 decks he should contact Annamarie directly.

In our game, a **red card is denoted as 1 and a black card is denoted as 0**. The final visualization depicts the probabilities of Player 1 winning based on each unique combination of their guess and Player 2’s guess. It also accounts for the methods of winning, those being by card amount and trick amount.

To start the game with no prior data, the user must use the function `play(path, n, seed=0)`. The variable `path` is a string representing the path to the database. If the file already exists, the function will append to the existing database. For our structure, the path must start with “data/”. The variable `n` is the number of iterations of the game to be played, and `seed` is an integer describing which random seed to use. Our implementation has seed = 0, so if the user does not specify a seed, they can replicate our results. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck.  -->