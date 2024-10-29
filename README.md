# Project Penny
### Authored by Mike Martinez, Annamarie Warnke, Zoe Cummings, David Cho, Claire Kolman, Kirin Mackey

**The main-updated branch is the most up to date branch, other branches were used for development.**

Project Penney is a project designed to simulate Penney's Game, a game played between two players where each player chooses a sequence of three card colors (e.g. Red, Black, Black). Points are awarded to players if their sequence appears when pulling cards sequentially from a well-shuffled deck. Penney's Game is of interest because the probability of winning is not equal; if the second player learns the sequence chosen by the first player, they can follow a rule to optimize their chances of winning. More information can be found in [the Wikipedia page](https://en.wikipedia.org/wiki/Penney%27s_game). 

Note that our simulation runs two variations of Penney's Game, which have different rules: 
1. For version 1, players are scored based on the number of "tricks" they earn. For example, if a player's sequence "Red, Black, Black" appears, the deck is cleared and the player earns 1 point. 
2. For version 2, players are scored based on the number of cards they earn. If a player's sequence "Red, Black, Black" appears, the deck is cleared and the player earns _all_ the cards in the deck. 

For mathematical explanation for why Penney's Game works, see [Nishiyama's paper](https://www.ijpam.eu/contents/2010-59-3/10/10.pdf)

---

To run the simulation, first clone the repository: 

```git clone https://github.com/mikemartinez13/project-penney-440.git```

Next, you can get all the necessary imports from the `env.yml` file. If you have conda installed, run

`conda env create -f env.yml -n penney`

in your command line to get the necessary environment (here we name it "penney"). Run

`conda activate penney` to activate your environment.

Next, open "main.ipynb" and run all of the cells. You may have to select a kernel, which you'll select the "penney" environment we just created. Below is a list of functions and their parameters:

### `play` 
**Parameters:** 
- `path (str)` String of the path of where you would like to store your data
- `n (int)`, The number of games you would like to run,
- `seed (int)` The random seed to use. If none set, defaults to 0.

 The function stores data in a database format. If the database file already exists, the function will append to the existing database. For our structure, the data is stored in a `“data/”` folder. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck.

For more information on what exactly goes into the `play` function, check out the [data management documentation](data_mgmt.md)

### make_heatmap() and make_heatmap package()

If the user wants to create visualizations from the data stored in `results/results.json` or data they have already created and stored as arrays, they can call either `make_heatmap` if they want one visualization or `make_heatmap_package` if they want a bundled version of 2 heatmaps displayed side by side. The arrays are in the format: Opponent’s Guess (y-axis) ordered from RRR(111) to BBB(000) top to bottom (rows 0-7 = 111-000), and My Guess (x-axis) ordered from BBB(000) to RRR(111) from left to right (columns 0-7 = 000-111). Files with the resulting visualizations will be saved in a `figures` folder and can only be stored as `.png` or `.html` files, with `.png` being the default. It should be noted that the visualizations use card encoding in which red = R = 1 and black = B = 0. 

To use the data stored in a `results/results.json` file the user can call:
- `make_heatmap(win_type=None, format=’png’, letters=True)` where the user can specify `win_type` as either ‘cards’, ‘tricks’, or not specify at all to receive and save the associated visualizations. They can also specify if they want the `format=’png’` (the default) or `format=’html’`, and if they want letters (`letters=True`) to represent the card sequences or numbers (`letters=False`). A visualization will be saved according to the `win_type` and be named “heatmap_[win_type]_n[n specified in results/results.json]” followed by “.png” or “.html”. In the case the user does not specify `win_type`, all three separate files (cards individually, tricks individually, both of them bundled using the `make_heatmap_package` function) will be created and saved but only the bundled figure is returned.
- `make_heatmap_package(format=’png’, letters=True)` results in a visualization displaying the ‘win by cards’ heatmap next to the ‘win by tricks’ heatmap. The user can specify `format=’png’` or `format=’html’` for how they want the image to be saved, as well as if they want letters (`letters=True`) to represent the card sequences or numbers (`letters=False`). The resulting visualization will be saved as “heatmap_packaged_cards_tricks_n[n specified in results/results.json]” followed by “.png” or “.html”. To get a bundled heatmap visualization saved as a png with letters representing the card sequences, the user just has to call `make_heatmap_package()`.
- Note: If `results/results.json` does not exist an error message will appear.

To use data the user has made separate from the results/results.json file the user must have data representing win probabilities at the minimum. If this is not given, the win probability data and its associated arguments from the `results/results.json` file will be used. The user's data must be in raw probability format (0,1) and must follow the array structure described above.

If the user has data representing win probabilities and want one visualization they can call `make_heatmap(data, data_ties, annots, n, win_type, title=”My Chance of Winning”, letters=True, format=’png’)`:


- `data (np.ndarray)`: is an 8 x 8 array detailing the win probabilities and is in the range [0,1]. If the size or numbers are in the wrong format, an error message will appear.
- `data_ties (np.ndarray)`: is an 8 x8 array detailing the tie probabilities and is in the range [0,1]. It is optional parameter in the case the user already has information stored in `annots` describing what they want displayed in each cell of the resulting heatmap. If the user wants to save the heatmap as a html, this is required. Error messages will be displayed accordingly.
- `annots (np.ndarray)`: is an 8 x8 array representing the labels (in strings) for each cell in the 8 x 8 heatmap. It is in the form “win (tie)” where the win and tie probabilities are rounded to the nearest integer and when using the data stored in `results/results.json`. This is an optional parameter in the case the user has information for `data_ties`. If only 'data_ties', rather than 'annots' is passed in, new labels for each cell in the 8 x 8 heatmap will be made in the form “win (tie)." If the user passes in both `data_ties` and `annots,` the `annots` passed in will be overwritten, as the most accurate will be those using `data` and `data_ties`.
- Note: if the user wants a .png, they must either have `data_ties` or `annots` to represent the existence of tie probabilities.
- Note: For `data`, `data_ties`, and `annots`, each row, going top down, should represent the associated probabilities where “Opponent’s” guesses are in descending order (RRR - BBB or 111 - 000). Each column, going left to right across should represent “My” guesses in ascending order (BBB - RRR or 000 - 111). The probabilities all relate to the user (represented by “My Guesses” and the x axis).
- `n (int)`: is an integer describing how many decks the win probability data stored in `data` represents. Adjusts the title in the final visualization and the name of the file storing the visualization.
- `win_type (str)`: is a string and is either ‘cards’ or ‘tricks’ to describe the winning method for probabilities in `data`. This argument is used to adjust the title of the final visualization and the name of the visualization file saved.
- `letters (bool)`: is a boolean and is set to `True` by default to indicate the card sequences are to be represented with letters (R for red, B for black). The user can specify `letters=False` if they want numbers to represent the card sequences (1 for red, 0 for black).
- `format (str)`: is a string and by default is set to ‘png’ to describe how the final visualization should be saved. The user can set `format =’html’` if they want a html file to be saved.
- Note: If the user specifies data and is missing any of the required fields or has any issues with regards to the format error messages will appear.


If the user has data from two different sets representing win probabilities they can call `make_heatmap_package(data1, data2, title1="My Chance of Winning", title2="My Chance of Winning", n1, n2, win_type1,  win_type2, data1_ties, data2_ties, labels1, labels2, letters=True, format = 'png'`):

- `data1 (np.ndarray)`: 8 x 8 array detailing the win probabilities from dataset 1 and is in the range [0,1]. If the size or numbers are in the wrong format, an error message will appear.
- `data2 (np.ndarray)`: 8 x 8 array detailing the win probabilities from dataset 2 and is in the range [0,1]. If the size or numbers are in the wrong format, an error message will appear.
- `title1 (str)`: a string set by default to “My Chance of Winning” to describe the title of the first heatmap. The user can define it further such as “My Chance of Winning Team 1,” and `win_type1` and `n1` will be used to adjust it in the final visualization.
- `title2 (str)`: a string set by default to “My Chance of Winning” to describe the title of the second heatmap. The user can define it further such as “My Chance of Winning Team 2,” and `win_type2` and `n2` will be used to adjust it in the final visualization.
- `n1 (int)`: an integer describing how many decks the win_probability data stored in `data1` represents. Adjusts the title for the first heatmap in the final visualization and the name of the file storing the visualization.
- `n2 (int)`: an integer describing how many decks the win_probability data stored in `data2` represents. Adjusts the title for the second heatmap in the final visualization and the name of the file storing the visualization.
- `win_type1 (str)`:  a string and either ‘cards’ or ‘tricks’ to describe the winning method for  probabilities in `data1`. This argument is used to adjust the title for the first heatmap of the final visualization and the name of the visualization file saved.
- `win_type2 (str)`: a string and either ‘cards’ or ‘tricks’ to describe the winning method for  probabilities in “data2”. This argument is used to adjust the title for the second heatmap of the final visualization and the name of the visualization file saved.
- `data1_ties (np.ndarray)`:  8 x8 array detailing the tie probabilities from dataset 1 and is in the range [0,1]. It is optional parameter in the case the user already has information stored in `labels1` describing what they want displayed in each cell of the first heatmap of the final visualization. If only 'data1_ties` rather than 'labels1' is passed in, new labels for each cell in the first 8 x 8 heatmap will be made in the form “win (tie)"  where the probabilities are rounded to the nearest integer. If the user wants to save the heatmap as html, this is required. Error messages will be displayed accordingly.
- `data2_ties (np.ndarray)`: 8 x8 array detailing the tie probabilities from dataset 2 and is in the range [0,1]. It is optional parameter in the case the user already has information stored in `labels2` describing what they want displayed in each cell of the first heatmap of the final visualization. If only 'data2_ties' rather than 'labels2' is passed in, new labels for each cell in the second 8 x 8 heatmap will be made in the form “win (tie)" where the probabilities are rounded to the nearest integer. If the user wants to save the heatmap as html, this is required. Error messages will be displayed accordingly.
- `labels1 (np.ndarray)`: an 8 x8 array representing the labels for each cell in the first heatmap, and in the form “win (tie)” if the user uses data in `results/results.json`, where the win and tie probabilities are rounded to the nearest integer. This is an optional parameter in the case the user has information for `data1_ties`. If the user passes in both `data1_ties` and `labels1`, the item passed in as `labels1` will be overwritten, as the most accurate will be those using `data1` and `data1_ties`.
- `labels2 (np.ndarray)`: an 8 x8 array representing the labels for each cell in the second heatmap, and by default is in the form “win (tie)” where the win and tie probabilities are rounded to the nearest integer. This is an optional parameter in the case the user has information for `data2_ties`. If the user passes in both `data2_ties` and `labels2`, the item passed in as `labels2` will be overwritten, as the most accurate will be those using data1 and data1_ties.
- Note: For `data1`, `data1_ties`, `labels1`, `data2`, `data2_ties`, and `labels2`, each row, going top down, should represent the associated probabilities where “Opponent”’s guesses are in descending order (RRR - BBB or 111 - 000). Each column, going left to right across, should represent “My” guesses in ascending order (BBB - RRR or 000 - 111).
- `letters (bool)`: is a boolean and is set to `True` by default to indicate the card sequences are to be represented with letters (R for red, B for black). The user can specify `letters=False` if they want numbers to represent the card sequences (1 for red, 0 for black). The probabilities all relate to the user (represented by “My Guesses” and the x axis).
- `format (str)`: is a string and by default is set to ‘png’ to describe how the final visualization should be saved. The user can set `format =’html’` if they want a html file to be saved.
- Note: If the user is missing any required fields or has data of the wrong format or size, error messages will be displayed and indicate which set of data triggered them.

Extended descriptions of these functions, other functions used to aid them, error handling functions, and settings associated with the .png and .html figures are located in the [visualization documentation](vis_docs.md).



<!-- To run this simulation and visualization you must download `main.ipynb`, `penney_db1.py`, `visualization.py`, `simulation.py`, and `play.py` from the main branch. In the same directory, you must have a folder named `data` to hold the database files, and a folder named `figures` that stores visualizations depicting simulation results. In `main.ipynb`, we used 30,000 decks. We found that 100,000 decks leads to the most accurate results, but GitHub cannot handle that size data file. The figure with 100,000 decks has been uploaded, but if the FLB would like the data with 100,000 decks he should contact Annamarie directly.

In our game, a **red card is denoted as 1 and a black card is denoted as 0**. The final visualization depicts the probabilities of Player 1 winning based on each unique combination of their guess and Player 2’s guess. It also accounts for the methods of winning, those being by card amount and trick amount.

To start the game with no prior data, the user must use the function `play(path, n, seed=0)`. The variable `path` is a string representing the path to the database. If the file already exists, the function will append to the existing database. For our structure, the path must start with “data/”. The variable `n` is the number of iterations of the game to be played, and `seed` is an integer describing which random seed to use. Our implementation has seed = 0, so if the user does not specify a seed, they can replicate our results. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck.  -->
