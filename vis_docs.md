# Visualization
### Authored by Kirin Mackey and Claire Kolman

## Figure Settings

### The following default settings apply for png images:

- Figure size: single heatmap - (height = 6, width = 6) , bundled heatmap - (height = 6, width = 12)
- Title font size: 15
- Axes:
    - X axis: title = “My Guesses”, title size = 12, tick size: 10
    - Y axis: title = “Opponent Guesses’, title size= 12,  tick size = 10
- Annot (text in each cell of heatmap) font size = 8
- Linewidth = 0.5
- colormap= ‘Blues’
- fmt =’’ (used to aid in displaying the annots)
- Colorbar
    - Position for single = [.95, 0.11, 0.035, .77], position for bundled = [.93, 0.11, 0.02, .77]
    - Outline width = 0.2
- Face color (background color) = #DBDBDB
- vmin = 0, vmax=100
- wspace (for bundled heatmaps) = 0.1

### The following default settings apply for html images:
- Figure size: single heatmap - (height = 750, width = 750), bundled heatmap - (height=675, width=1300)
- Title font size: 22
- Title spacing: single - (x = 0.5, y = 0.94) bundle - (y = 1.05)
- Axes:
    - X axis: title = 'My Guesses', title size=18, tick size=16
    - Y axis: title = 'Opponent Guesses', title size=18, tick size=16
    - showgrid = False for and x and y axes
- xgap and ygap both = 1
- Colors: ‘blues’
- Tool tip text:
    - Me: [x-value], Opponent: [y-value]
    - My Win Probability: [win_prob]
    - Tie Probability: [tie_prob], name = "",
- hoverongaps = False                       
- Colorbar:
    - Tick positions [0, 20, 40, 60, 80, 100]
    - Tick labels [0, 20, 40, 60, 80, 100]
    - outlinewidth = 1
    - outlinecolor = #E7E7E7
- zmin=0, zmax=100
- Plot background color = #DBDBDB

## Necessary Imports
- `import matplotlib.pyplot as plt`
- `import seaborn as sns`
- `import numpy as np`
- `from typing import Optional`
- `import random`
- `import json`
- `import os`
- `import plotly`
- `import plotly.graph_objects as go`
- `from plotly.subplots import make_subplots`
- `from typing import Union`
- `from typing import Tuple`

## Data Input (Array Structure)
For data to be displayed correctly in the image(s), the arrays in the json file follow a specific structure. If the user is passing their own data in to the visualization functions, they not only need to make sure their probabilities are in raw form (between 0,1), their data also needs to match this structure below.

Order of the array: 

Opponent’s Guess (y-axis) is ordered from RRR(111) to BBB(000) top to bottom [rows, each array 0-7], and My Guess (x-axis) is ordered from BBB(000) to RRR(111) from left to right [columns, each position inside of the arrays 0-7].

Ex:

[[(RRR,BBB), (RRR,BBR)...(RRR,RRB), (RRR,RRR)],

[(RRB,BBB), (RRB,BBR)...(RRB,RRB), (RRB,RRR)],

...

[(BBR,BBB), (BBR,BBR)...(BBR,RRB), (BBR,RRR)],

[(BBB,BBB), (BBB,BBR)...(BBB,RRB), (BBB,RRR)]]


## Main Functions

### `make_heatmap`
Note: Optional type hinting is used to handle the cases in which the user wants to use data stored in `results/results.json`, or calls `make_heatmap` with their own data where then our validation process needs to be satisfied and raises errors accordingly.

**Parameters:**
- `data` (`Optional[np.ndarray]`): Win probability in its raw form (range[0,1]) stored in an 8 x 8 array or is `None`
- `data_ties` (`Optional[np.ndarray]`): Tie probability in its raw form (range[0,1]) stored in an 8 x 8 array or is `None`
- `annots` (`Optional[np.ndarray]`): Represents annotations, or what is displayed in each cell of the visualization most likely in the form “win (tie)”. Stored in an 8 x 8 array where each element is a string, or is `None`
- `n` (`Optional[int]`): an integer describing the number of decks, or is `None`
- `win_type` (`Optional[str]`):  a string indicating the win method for the probability data. It is either ‘cards’, ‘tricks’, or `None`
- `title` (`str`, optional): Title of the heatmap. Defaults to `"My Chance of Winning"`but can be modified by the user.
- `hide_y` (`bool`, optional): Determines whether to hide the y-axis title, tick labels, and tick marks. Defaults to `False` but is set to `True` in the case of a bundled heatmap visualization to hide the y axis of the 2nd subplot.
- `cbar_single` (`bool`, optional): Indicates whether a single heatmap is made and therefore specific colorbar settings shoudl apply. Defaults to `True`, but to create a bundled heatmap visualization in `make_heatmap_package_backend`, a separate cbar is made so `cbar_single` here is set to `False`.
- `ax` (`plt.Axes`, optional): Matplotlib Axes object. Defaults to `None` in the case that a single heatmap is made. If a bundled heatmap visualization is desired it takes in an axis to describe which subplot to be inserted into. 
- `bundle` (`bool`, optional): Boolean describing whether to bundle two heatmaps. Defaults to `False` when making a single heatmap, set to `True` to aid in `make_heatmap_package` described below this function.
- `letters` (`bool`, optional):a boolean by default set to `True`, meaning the card sequences are set to letters rather than numbers (`letters = False`).
- `format` (`str`, optional): Output format (`'png'` or `'html'`). Defaults to `'png'`.

**Returns:**
- `Union[Tuple[plt.Figure, plt.Axes], plotly.graph_objs._figure.Figure]`: Generated heatmap figure either as Matplotlib figure and axes objects if `format='png'`, or a Plotly figure object if `format='html'`

**Description:**
Main function to generate heatmaps based on provided or default data. If the user did not insert any data at all, make_heatmap() will make heatmaps of existing data in the `results/results.json` file. It accesses that data through the `get_data(path)` function. Heatmaps for cards, tricks, and both bundled together will be created and saved in a `figures` folder if win_type is not specified, but the bundled figure is the object that gets returned. The user can also specify "bundle=True" if they only want the bundled package. If the `results/results.json` file does not exist, an error message will appear.

- In the case the user inputs their own win probability data, setting it equal to `data`:
    - Checks the data passed in and formats it by calling `validate_and_process_input(n, win_type, data_ties, annots, data)`, raising a `ValueError` if the conditions in validate_and_process_input are not met.
    - Adjusts the title in the final visualization using `win_type` and `n` passed in by the user.
    - If the user set `format = ‘png’`, `make_heatmap_backend(data, annots, title, n, hide_y, cbar_single, ax, letters)` is called to make the visualization in png format. The figure is then saved as 'figures/heatmap_[win_type specified] _n[n specified].png"
    - If the user set format =’html’, `validate_existence(data_ties)` is run since the raw tie data is needed to make tooltips in plotly. If `validate_existence` is passed, `create_html(win_prob=data, tie_prob=data_ties, labels= annots, bundled=False, letters=letters, title=title, n=n)` is called to create a single heatmap. The file is then saved as  'figures/heatmap_[win_type specified] _n[n specified].html’
- In the case the user wants to use data stored in a results/results.json file:
    - The raw win by card probabilities (stored as `var_cards`), the raw win by trick probabilities (stored as `var_tricks)`, the tying probabilities associated with each (`card_ties` an `trick_ties`), and `n` are retrieved using `get_data(‘results/results.json)`. An error message will be displayed if `results/results.json` does not exist
    - Depending on the `win_type` specified by the user, the win by card, win by tricks, and associated tie probabilities are formatted and the required annotations are made as well with the `format_data` and `make_annots` functions.
    - `make_heatmap_backend` is called with the formatted win probability, annots, title, n from results/results.json, and letters (`True` or `False`) to make the visualization and returns a plt.Figure and plt.Axes
    - The visualization is then saved as  'figures/heatmap_[win_type specified] _n[n specified in results/results.json]’ followed by ‘.png’ or ‘html’ depending on what is passed in as format.
    - If the user did not specify any `win type`:
       - win by card, win by tricks, the associated tie probabilities are all formatted with `format_data`, accurate annotations are made with `make_annots`, and titles are made to indicate the win method and denote the number of decks used to make the probability data in `results/results.json`
       - decks used to make the probability data in `results/results.json`
If `format = ‘png’` a bundled version of the default win by card (1st subplot) and win by trick data (2nd subplot) is  made by calling `make_heatmap_package` with formatted win probabilities, annotations passed in as `labels1` and `labels2`, `win_type1=’cards’`, `win_type2=’tricks`, both `n1` and `n2` passed in as the `n` stored in `results/results.json`, and `letters` (`True` by default or `False`). If format = ‘html’, `create_html` is called where `bundled=True`, the formatted win probabilities for both win methods, the appropriate annotations for each win method, `n` stored in `results/results.json`, and letters (`True` by default or `False`) are passed in. If `bundle` (set to `False` by default)  in `make_heatmap` is `True`, then only the bundled set of heatmaps is returned. The file is saved as  'figures/heatmap_packaged_cards_tricks_n[n specified in results/results.json]” followed by “.png” or ".html" as specified in format in `make_heatmap_package'.

       - An individual win by cards visualization is created with `make_heatmap_backend` and saved as  'figures/heatmap_cards _n[n specified in results/results.json]’ followed by ‘.png’ or ‘html’ depending on what is passed in as format.
       - An individual win by tricks visualization is created with `make_heatmap_backend` and saved as  'figures/heatmap_tricks_n[n specified in results/results.json]’ followed by ‘.png’ or ‘html’ depending on what is passed in as format.
       - The bundled figure and axes object (only if `format=’png’`) are returned.



### `make_heatmap_package`
Note: Optional type hinting is used to handle the cases in which the user wants to use data stored in results.json, or calls make_heatmap_package with their own data where then our validation process needs to be satisfied and raises errors accordingly.

**Parameters:**
- `data1` (`Optional[np.ndarray]`): an 8 x8 array with the win probabitlies for the first set of data in raw format (range of [0,1])
- `data2` (`Optional[np.ndarray]`): an 8 x8 array with the win probabitlies for the second set of data in raw format (range of [0,1])
- `title1` (`Optional[str]`): Title for the first heatmap later modified to indicate win type and n. Defaults to “My Chance of Winning” but the user can modify it to represent team data such as “My Chance of Winning Team 1”
- `title2` (`Optional[str]`): Title for the second heatmap later modified to indicate win type and n. Defaults to “My Chance of Winning” but the user can modify it to represent team data such as “My Chance of Winning Team 2”
- `n1` (`Optional[int]`): number of decks represented in the first dataset and used in caluclating the probabilities in `data1`
- `n2` (`Optional[int]`): number of decks represented in the second dataset and used in caluclating the probabilities in `data2`
- `win_type1` (`Optional[str]`): either ‘cards’ or ‘tricks’ to denote which win method the winning probabilities represent in `data1`
- `win_type2` (`Optional[str]`):either ‘cards’ or ‘tricks’ to denote which win method the winning probabilities represent in `data2`
- `data1_ties` (`Optional[np.ndarray]`): an 8 x 8 array with the tie probabitlies for the first set of data in raw format (range of [0,1]). This is optional in the case the user wants a png but only has `labels1` which holds tie data. It is required if the user wants a html file to make the tooltips correctly.
- `data2_ties` (`Optional[np.ndarray]`): an 8 x 8 array with the tie probabitlies for the second set of data in raw format (range of [0,1]). This is optional in the case the user wants a png but only has `labels2` which holds tie data. It is required if the user wants a html file to make the tooltips correctly.
- `labels1` (`Optional[np.ndarray]`): an 8 x 8 array where each element is a string representation what should each cell display in the first subplot. This is optional in the case the user has raw tie data stored in `data1_ties`
- `labels2` (`Optional[np.ndarray]`): an 8 x 8 array where each element is a string representation what should each cell display in the second subplot. This is optional in the case the user has raw tie data stored in `data2_ties`
- `letters` (`bool`, optional): boolean denoting whether letters(`True` by default) or numbers (`letters=False`) should be used to represent the card sequences 
- `format` (`str`, optional): Output format (`'png'` or `'html'`). Defaults to `'png'`.

**Returns:**
- `Union[Tuple[plt.Figure, plt.Axes], plotly.graph_objs._figure.Figure]`: Generated bundled heatmap figure, which is either Matplotlib figure and axes objects if `format='png'`, or a Plotly figure object if `format='html'`

**Description:**
Generates bundled heatmaps based on the two different sets of data.
- In the case the user does not specify `data1` or `data2`, the data stored in `results/results.json` will be used to make the bundled heatmap. They can also adjust letters in this case, where `letters=True` (by default) has the card sequences represented by letters, while `letters=False` has them represented by numbers
    - If the user specified format = ‘html’, `make_heatmap(bundle=True, letters=letters, format='html')` is called, where the bundled heatmap is saved according to the name specified in the `make_heatmap` section.
    - If the user does not specify `format`, or passes in `format = ‘png’`, `make_heatmap(bundle=True, letters=letters)` is called,  where the bundled heatmap is saved according to the name specified in the `make_heatmap` section.
- In the case the user specifies at least one set of winning probabilities (`data1` or `data2`, or both)
    - The condition that both `data1` and `data2` are passed in is checked with `validate_existence`
    - `validate_and_process_input(n1, win_type1, data1_ties, labels1, data1)` is executed for the data pertaining to the first set of data, where any errors with regards to existence, size, and format are raised if triggered. Otherwise the data for the first set of data is formatted appropriately with `format_data` and `labels1` (in `make_heatmap` named `annots`) are either made or validated depending on the user input.
    - `validate_and_process_input(n2, win_type2, data2_ties, labels2, data2)` is executed for the data pertaining to the second set of data, where any errors with regards to existence, size, and format are raised if triggered. Otherwise the data for the second set of data is formatted appropriately with `format_data` and `labels2` (in `make_heatmap` named `annots`) are either made or validated depending on the user input.
    - If the format= ‘png’, `make_heatmap_package_backend(data1=data1, data1_ties=data1_ties, data2=data2, data2_ties=data2_ties,title1=title1, 
title2=title2, n1=n1, n2=n2, win_type1=win_type1, win_type2=win_type2, labels1=labels1, labels2=labels2, letters=letters)` is called. Its processes are described below.
    - If the format = ‘html’, `create_html(bundled=True, win_prob=data1, tie_prob=data1_ties, title1=title1, labels=labels1, win_prob2=data2, tie_prob2=data, labels2=labels2, n2=n2, title2=title2, letters=letters)` is called. Its processes are described below
    - In either case of format, the file is saved as 'figures/heatmap_packaged_[win_type1 specified]' followed by 'n[n1 specified]_[win_type2 specified]_n[n2 specified]' followed by “.png” or “.html"





## Helper Functions

### `get_data`

**Parameters:**
- `path` (`str`): Path to the JSON data file. `make_heatmap` calls `get_data` with `path = results/results.json`

**Returns:**
- `Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]`: Processed data arrays and simulation count.

**Description:**
This function is used to access the results/results.json file if the user doesn’t specify their own data in `make_heatmap` or `make_heatmap_package`.
- First checks to see if the file exists and if not it throws a file not found error
- If the file exists it will be opened and read and the following data will be extracted from the dictionary within the json file
    - var_cards (8x8 array of raw win probabilities for card version)
    - var_tricks (8x8 array of raw win probabilities for trick version)
    - card_ties (8x8 array of raw tie probabilities for card version)
    - trick_ties (8x8 array of raw tie probabilities for trick version)
    - n (the number of iterations or decks played)


### `fill_diag`

**Parameters:**
- `array` (`np.ndarray`): Input array.
- `filler`: Value to fill the diagonal with.

**Returns:**
- `np.ndarray`: Array with the bottom left to top right diagonal filled with what is specified in the filler argument

**Description:**

Fills the diagonal of a matrix with a specified filler. Uses np.fill_diagonal to achieve the desired output, but flipping the array before and after is required to fill the correct diagonal.
* Flips the data over the horizontal axis, uses np.fill_diagonal, flips it back over the horizontal axis

Used when making annotations in `make_annots` where `(filler = "")` and when formatting the data in `format_data` where `(filler=None)`.


### `format_data`

**Parameters:**
- `array` (`np.ndarray`): Array of raw probability values.

**Returns:**
- `np.ndarray`: Formatted array with percentages and cleaned diagonal.

**Description:**

Formats raw probability data into percentage values and cleans the diagonal by using `fill_diag` on the array with `filler = None`. Done in order to display the diagonal as blank in the final visualization.



### `make_annots`
Creates annotation strings from win and tie probabilities.

**Parameters:**
- `wins` (`np.ndarray`): Array of win probabilities.
- `ties` (`np.ndarray`): Array of tie probabilities.

**Returns:**
- `np.ndarray`: Array of annotation strings in the format "win(tie)".

**Description:**

The input arrays will need to already have gone through the `format_data` function or be in that format already. Loops through each array pulls each value at the respective places in each of the arrays. Appends them as strings in the form "win(tie)" to a new list that matches the order of probabilities depending on the Opponent guess or "My" guess. The `fill_diag` function is used on the new list with the `filler=“”`.


### `validate_existence`


**Parameters:**
- `input`: Input to validate.

**Raises:**
- `TypeError`: If input is missing.

**Description:**
Checks for the existence of a required input. This function is used on required arguments if the user is passing in their own data. For instance it is used on win type since the heatmaps cannot be created without the win type specified. The function checks if the input is `None` and if so it raises a type error.

### `validate_numbers`

**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `ValueError`: If any probability value exceeds 1.

**Description:**
Ensures that the data provided by the user is in raw format, meaning within the range [0, 1]. Loops through each array in the initial array and in each array and checks if a value is greater than 1. If any value is greater than 1, this means the probabilities are not in raw form and it raises a value error.

### `validate_size`

**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `IndexError`: If data is not 8x8.

**Description:**
Ensures data given by the user fits the project's guidelines of an 8 x 8 array by checking if the shape of the data is 8x8. If it is not then an index error is raised.

### `validate_data`


**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `IndexError`: If data size is not 8x8.
- `ValueError`: If probability values are out of range.

**Description:**
Validates the size and format of the input data.
* Uses a try and except block with the function `validate_size` and raises an index error if the array fails to satisfy the conditions of that function.
* Uses another try and except block with the `validate_numbers` function and raises a value error if the array fails to satisfy the conditions of that function.


### `validate_tie_existence`

**Parameters:**
- `input_raw`: Raw tie data.
- `input_annots`: Annotation data.

**Raises:**
- `TypeError`: If both tie data and annotations are missing.

**Description:**
This function is used to check if there is an instance of tie data. For the png format the actual tie data (in range [0,1]) is not required for the visualization, but is necessary for the annotations that label the squares in the final heatmaps. Therefore the function checks if either tie data or annotation data exists since both are not necessary for the png format to run. If neither exists, a type error is raised since some form of the tie documentation is needed.


### `validate_and_process_input`

**Parameters:**
- `n` (`Optional[int]`): Number of simulations or decks.
- `win_type` (`Optional[str]`): Type of win metric ('cards' or 'tricks').
- `data_ties` (`Optional[np.ndarray]`): Tie probability data.
- `annots` (`Optional[np.ndarray]`): Annotations, or labels, meant to be displayed in each cell of the heatmap.
- `data` (`Optional[np.ndarray]`): Win probability data.

**Returns:**
- `Tuple[int, str, Optional[np.ndarray], Optional[np.ndarray], np.ndarray]`: Processed inputs for `n`, `win_type`, `data_ties`, `annots`, and `data`.

**Description:**
Validates and processes user input for heatmap generation.
-  Note: all parameters are optional because this function is part of validating the user input. If any validation test fails error messages will appear to the user.
-  This function is run in both `make_heatmap` and `make_heatmap_package`.
-  It first runs `validate_existence(n)` and and `validate_existence(win_type)`. They are needed in any case the user wants to create a visualization from data.
-  Then `validate_tie_existence(data_ties, annots)` is run, testing if tie data is indicated in any form. If the format is .png, either `data_ties` or `annots` have to exist.
-  Next the function `validate_data(data)`, where data is the array of win probabilities, is executed, testing if the data passed in is of the correct raw format and size.
-  Then `format(data)` is called on `data` to format it properly for `make_heatmap_backend` and `make_annots`.
-  If the user passed in `data_ties`, the function checks if is  in the correct raw format and size with `validate_data(data_ties) `and formats it properly for `make_annots(data, data_ties)` and create_html (if the user specified format =’html’) executed outside this function. It formats it by calling `format_data(data_ties)`.
-  If the user passed in `annots` and `data_ties` in `make_heatmap`, the `annots` passed in will be overwritten as `data` and `data_ties` are more accurate in representing the winning and tying.
-  Regardless of whether the user passed in `annots` (without `data_ties`) or `data_ties`, `validate_size(annots)` is executed, making sure the `annots` are of the proper size. 



### `make_heatmap_backend`

**Parameters:**
- `data` (`np.ndarray`): an 8 x8 array with the win probabilities in the correct format (specified in `format_data`)
- `annots` (`np.ndarray`): Annotations.
- `title` (`str`): Title of the heatmap either set to a user input or “My Chance of Winning” followed by ‘By Cards” or “By Tricks” and “(n=[user specified or from results/result.json])”
- `hide_y` (`bool`, optional): Hide y-axis ticks labels, tick marks, and axis title. Defaults to `False`. Set to `True` in `make_heatmap_package_backend` to make a bundled version of two heatmaps.
- `cbar_single` (`bool`, optional): a boolean set to `True` by default.  In the case one heatmap is made, it makes a colorbar with settings meant for a single heatmap. This is set to `False` when this function is called in `make_heatmap_package_backend` where other colorbar settings used
- `ax` (`plt.Axes`, optional): Matplotlib Axes object set to None by default if a single heatmap is made. It is set to a specific axis in `make_heatmap_package_backend` to place a heatmap in a subplot for a bundled heatmaps visualization.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.

**Returns:**
- `Tuple[plt.Figure, plt.Axes]`: Matplotlib figure and axes objects.

**Description:**
Backend function to create a single heatmap using Seaborn.
* Checks if no axis is passed in, meaning a single heatmap is created. If one is, then the parent figure is retrieved with ax.get_figure()
* The proper tick labels are set according to `letters=True` or `letters=False` (where numbers are used instead to represent the card sequences)
* `sns.heatmap` is called with the proper data, annotations, axis, and additional png figure settings described above. Axis labels are also set according to the png figure settings described above.
* `ax.set_facecolor('#DBDBDB')` is called to ensure the diagonal, where the sequences  “My Guess” and “Opponent Guess” are the same, is gray.
* If `cbar_single = True`, an appropriate colorbar is made and placed according to the position noted in the png figure settings.
* The plot title is set accordingly
* If `hide_y= True`, meaning `make_heatmap_backend` is making the plot for the 2nd subplot in the, the y axis label and tick marks are hidden.

### `make_heatmap_package_backend`

**Parameters:**  
- `data1` (`np.ndarray`): Win probability data for the first set of data in an 8x8 array, formatted according to our `format_data` function specifications
- `data2` (`np.ndarray`): Win probability data for the second set of data in an 8x8 array, formatted according to our `format_data` function specifications
- `title1` (`str`): Title for the first heatmap.
- `title2` (`str`): Title for the second heatmap.
- `n1` (`int`): Number of simulations (or decks) for the first dataset.
- `n2` (`int`): Number of simulations (or decks) for the second dataset.
- `win_type1` (`str`): Win type for the first dataset. 
- `win_type2` (`str`): Win type for the second dataset.
- `labels1` (`np.ndarray`, optional): Annotations (in the "win (tie)" format) for the first dataset in an 8 x 8 array. Either made in `validate_and_process_input` with `data1_ties` or user specified.
- `labels2` (`np.ndarray`, optional): Annotations (in the "win (tie)" format) for the first dataset in an 8 x 8 array. Either made in `validate_and_process_input` with `data2_ties` or user specified.
- `letters` (`bool`, optional): Use letter sequences to denote the card sequences for tick labels. Defaults to `True`, if `False` numbers are used.

**Returns:**
- `Tuple[plt.Figure, plt.Axes]`: Matplotlib figure and axes objects with bundled heatmaps.

**Description:**
Create a 1x2 grid of heatmaps based on the given data. Helper function for the `make_heatmap_package` function.
* The width space between the heatmaps is assigned with gridspec_kw (noted in the png figure settings above)
* An empty figure with 2 subplots is made, according to the figure sizes noted in the png settings above with `fig, ax = plt.subplots(1, 2, figsize=(FIG_WIDE*2, FIG_HIGH),  gridspec_kw=gridspec_kw)`
* The final titles for each heatmap are made, using `title1`, `title2`, `n1`, `n2`, `win_type1`, and `win_type2`. For instance, if `title1` is set to “My Chance of Winning” (by default), `n1 = 1000000` and `win_type1=’cards’`, the new title for the first subplot will be “My Chance of Winning (By Cards)\n(n=1000000)”.
* `make_heatmap_backend(data1, ax=ax[0],  title=title1, annots=labels1, cbar_single=False, letters = letters`) is called, meaning the first subplot is made using the arguments corresponding to the first set of data and placed in the first position (`ax[0]`) in the initial empty figure created.
* `make_heatmap_backend(data2, ax=ax[1], annots=labels2, title=title2, cbar_single=False, hide_y=True,  letters = letters)` is called, meaning the second subplot is made using the arguments corresponding to the second set of data and placed in the second position (`ax[1]`) in the initial empty figure created.
* A colorbar is made for the bundled heat maps visualization, where specific details are found in the png figure settings described above


### `single_map`


**Parameters:**
- `fig` (`plotly.graph_objs._figure.Figure`): The Plotly figure object with subplots created outside of this function.
- `win_prob` (`np.ndarray`): Win probability data in an 8x8 array, formatted according to our `format_data` function specifications
- `tie_prob` (`np.ndarray`): Tie probability data also formatted and in an 8x8 array
- `labels` (`np.ndarray`): 8 x8 array of annotations to denote the text in each square in the heatmaps.
- `letters` (`bool`): boolean for letters (`True`) or numbers (`False`) on the axes
- `col` (`int`, optional): Column index for subplot placement. Defaults to `1`.

**Returns:**
- `plotly.graph_objs._figure.Figure`: Updated Plotly figure with the heatmap added.

**Description:**
Creates a single heatmap within a Plotly figure.
* The function first checks if the argument `letters = True`, then specifies x and y variables with a list of strings for the axes ticks, letters being used if `letters = True` (the default), and numbers being used if `letters = False`
* Next adds heatmap trace to the subplot using the html figure settings above
    * win_prob is used as the data to make the heatmap, tie_prob is inserted as customdata for the purpose of the tool tip, the text argument is specified as np.flip(labels,0) for the purpose of the labels appearing correctly on the map and text is used for the texttemplate argument, x and y are set to the x and y lists from above
    * The trace is added to row = 1, col = col (default = 1), variable for the purpose of bundled maps needing 2 columns

### `bundled_maps`

**Parameters:**
- `fig` (`plotly.graph_objs._figure.Figure`): The Plotly figure object with subplots created outside of this function.
- `win_prob` (`np.ndarray`): Win probability data in an 8x8 array, formatted according to our `format_data` function specifications
- `tie_prob` (`np.ndarray`): Tie probability data also formatted and in an 8x8 array
- `labels` (`np.ndarray`): 8 x8 array of annotations to denote the text each square in the heatmaps.
- `win_prob2` (`np.ndarray`): second set of win probability data in an 8x8 array, formatted according to our `format_data` function specifications
- `tie_prob2` (`np.ndarray`): second set of tie probability data also formatted and in an 8x8 array
- `labels2` (`np.ndarray`): second set of labels (or annotations) in an 8x8 array as well
- `letters` (`bool`): boolean for letters (`True`) or numbers (`False`) on the axes
- `col` (`int`): Column index for subplot placement. 

**Returns:**
- `plotly.graph_objs._figure.Figure`: Returns the Plotly figure object from the second instance of `single_map`

**Description:**
* This function adds trace to the first subplot using the single_map function with the inputs: fig, win_prob, tie_prob, labels, and letters) This uses the default value,1, of the col argument.
* The `single_map` function is used again with the first instance of the function being used as the fig argument to add trace to fig that has already been updated, win_prob2, tie_prob2, labels2, letters, and col = 2 so the trace is added the the subplot in the second column and not overwriting the first one


### `create_html`


**Parameters:**
- `win_prob` (`np.ndarray`): win probability data in an 8x8 array, formatted according to our `format_data` function specifications
- `tie_prob` (`np.ndarray`): tie probability data also formatted and in an 8x8 array
- `labels` (`np.ndarray`): 8 x8 array of annotations to denote the text each square in the heatmaps.
- `n` (`int`): Number of decks.
- `title` (`str`): Title of the heatmap.
- `bundled` (`bool`, optional): Whether to bundle multiple heatmaps. Defaults to `False`.
- `letters` (`bool`, optional): Boolean for letters or numbers on the axes. Defaults to 'True' to have letters on the axes.
- `**kwargs`: Additional keyword arguments win_prob2, tie_prob2, labels2, n2, title2. The format of these optional arguments is the same as the equivalent arguments for the first set of data above.

**Returns:**
- `plotly.graph_objs._figure.Figure`: The generated Plotly figure.

**Description:**
Generates an interactive HTML heatmap. Helper function for the `make_heatmap` function if user requests HTML image. 
- First flips the win and tie probabilities arrays (win_prob, tie_prob) for the purpose of the html figure creation
- If the bundled = False argument exists (which is the default) that if block is entered,
    - A fig is created and uses the single_map function with the arguments: fig (subplots created outside of this function), win_prob, tie_prob, labels, and letters
    - The sizes and fonts are updated according to the settings above
- If bundled = True, the else block is entered
    - The second set of win and tie data is flipped for the purpose of creating the figure
    - A fig with 2 subplots is created and the bundled_maps function is used to add data to the subplots with the arguments: fig, win_prob, tie_prob, labels, win_prob2, tie_prob2, labels2, letters, and col = 2 for the purpose of creating 2 plots
    - The sizes and fonts are updated according to the html figure settings above

