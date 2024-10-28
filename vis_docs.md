# Visualization
### Authored by Kirin Mackey and Claire Kolman

## Figure Settings

### The following default settings apply for png images:

- Figure size: single heatmap - (height = 6, width = 6) , bundled heatmap - (height = 6, width = 12)
- Title font size: 15
- Axes:
         * X axis: title = “My Guesses”, title size = 12, tick size: 10
         * Y axis: title = “Opponent Guesses’, title size= 12,  tick size = 10
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

## Main Functions

### `make_heatmap`
Main function to generate heatmaps based on provided or default data. If the user did not insert any data at all, make_heatmap() will make heatmaps of existing data in the `results/results.json` file. It accesses that data through the `get_data(path)` function. Heatmaps for cards, tricks, and both will be created if win_type is not specified. The user can also specify "bundle=True" if they only want the bundled package. If the `results/results.json` does not exist, an error message will appear.

**Parameters:**
- `data` (`Optional[np.ndarray]`): Win probability data.
- `data_ties` (`Optional[np.ndarray]`): Tie probability data.
- `annots` (`Optional[np.ndarray]`): Annotations.
- `n` (`Optional[int]`): Number of simulations.
- `win_type` (`Optional[str]`): Type of win metric.
- `title` (`str`, optional): Title of the heatmap. Defaults to `"My Chance of Winning"`.
- `hide_y` (`bool`, optional): Hide y-axis labels. Defaults to `False`.
- `cbar_single` (`bool`, optional): Show colorbar for single heatmap. Defaults to `True`.
- `ax` (`plt.Axes`, optional): Matplotlib Axes object.
- `bundle` (`bool`, optional): Bundle multiple heatmaps. Defaults to `False`.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.
- `format` (`str`, optional): Output format (`'png'` or `'html'`). Defaults to `'png'`.

**Returns:**
- `Union[Tuple[plt.Figure, plt.Axes], plotly.graph_objs._figure.Figure]`: Generated heatmap figure.

### `make_heatmap_package`
Generates bundled heatmaps based on the two different types of game types, win by cards and win by "tricks". 

**Parameters:**
- `data1` (`Optional[np.ndarray]`): 8x8 array of win probabilities for the first set of data.
- `data2` (`Optional[np.ndarray]`): 8x8 array of win probabilities for the second set of data.
- `title1` (`Optional[str]`): Title for the first heatmap. Defaults to `"My Chance of Winning"`.
- `title2` (`Optional[str]`): Title for the second heatmap. Defaults to `"My Chance of Winning"`.
- `n1` (`Optional[int]`): Number of simulations for the first dataset.
- `n2` (`Optional[int]`): Number of simulations for the second dataset.
- `win_type1` (`Optional[str]`): Win type for the first dataset.
- `win_type2` (`Optional[str]`): Win type for the second dataset.
- `data1_ties` (`Optional[np.ndarray]`): Tie data for the first dataset.
- `data2_ties` (`Optional[np.ndarray]`): Tie data for the second dataset.
- `labels1` (`Optional[np.ndarray]`): Annotations for the first dataset.
- `labels2` (`Optional[np.ndarray]`): Annotations for the second dataset.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.
- `format` (`str`, optional): Output format (`'png'` or `'html'`). Defaults to `'png'`.

**Returns:**
- `Union[Tuple[plt.Figure, plt.Axes], plotly.graph_objs._figure.Figure]`: Generated bundled heatmap figure.


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
Validates and processes user input for heatmap generation.

**Parameters:**
- `n` (`Optional[int]`): Number of simulations.
- `win_type` (`Optional[str]`): Type of win metric.
- `data_ties` (`Optional[np.ndarray]`): Tie probability data.
- `annots` (`Optional[np.ndarray]`): Annotations.
- `data` (`Optional[np.ndarray]`): Win probability data.

**Returns:**
- `Tuple[int, str, Optional[np.ndarray], Optional[np.ndarray], np.ndarray]`: Processed inputs.

**Description:**

### `make_heatmap_backend`
Backend function to create a single heatmap using Seaborn.

**Parameters:**
- `data` (`np.ndarray`): Formatted win probability data.
- `annots` (`np.ndarray`): Annotations.
- `title` (`str`): Title of the heatmap.
- `hide_y` (`bool`, optional): Hide y-axis labels. Defaults to `False`.
- `cbar_single` (`bool`, optional): Show colorbar. Defaults to `True`.
- `ax` (`plt.Axes`, optional): Matplotlib Axes object.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.

**Returns:**
- `Tuple[plt.Figure, plt.Axes]`: Matplotlib figure and axes objects.

**Description:**

### `make_heatmap_package_backend`
Create a 1x2 grid of heatmaps based on the given data. Helper function for the `make_heatmap_package` function.

**Parameters:**
- `data1` (`np.ndarray`): First dataset.
- `data2` (`np.ndarray`): Second dataset.
- `title1` (`str`): Title for the first heatmap.
- `title2` (`str`): Title for the second heatmap.
- `n1` (`int`): Number of simulations for the first dataset.
- `n2` (`int`): Number of simulations for the second dataset.
- `win_type1` (`str`): Win type for the first dataset. 
- `win_type2` (`str`): Win type for the second dataset.
- `data1_ties` (`Optional[np.ndarray]`): Tie data for the first dataset.
- `data2_ties` (`Optional[np.ndarray]`): Tie data for the second dataset.
- `labels1` (`Optional[np.ndarray]`): Annotations for the first dataset.
- `labels2` (`Optional[np.ndarray]`): Annotations for the second dataset.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.

**Returns:**
- `Tuple[plt.Figure, plt.Axes]`: Matplotlib figure and axes objects with bundled heatmaps.

**Description:**


### `single_map`


**Parameters:**
- `fig` (`plotly.graph_objs._figure.Figure`): The Plotly figure object with subplots created outside of this function.
- `win_prob` (`np.ndarray`): Win probability data in an 8x8 array, formatted according to our `format_data` function specifications
- `tie_prob` (`np.ndarray`): Tie probability data also formatted and in an 8x8 array
- `labels` (`np.ndarray`): 8 x8 array of annotations to denote the text in each square in the heatmaps.
- `letters` (`bool`): boolean for letters (`True`) or numbers (`False`) on the axes
- `col` (`int`): Column index for subplot placement. Defaults to `1`.

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

