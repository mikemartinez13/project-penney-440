
## Functions

### `create_html`
Generates an interactive HTML heatmap. Helper function for the `make_heatmap` function if user requests HTML image. 

**Parameters:**
- `win_prob` (`np.ndarray`): Array of win probabilities.
- `tie_prob` (`np.ndarray`): Array of tie probabilities.
- `labels` (`np.ndarray`): Array of annotations.
- `n` (`int`): Number of simulations.
- `title` (`str`): Title of the heatmap.
- `bundled` (`bool`, optional): Whether to bundle multiple heatmaps. Defaults to `False`.
- `letters` (`bool`, optional): Use letter sequences for labels. Defaults to `True`.
- `**kwargs`: Additional keyword arguments for customization.

**Returns:**
- `plotly.graph_objs._figure.Figure`: The generated Plotly figure.

### `single_map`
Creates a single heatmap within a Plotly figure.

**Parameters:**
- `fig` (`plotly.graph_objs._figure.Figure`): The Plotly figure object.
- `win_prob` (`np.ndarray`): Array of win probabilities.
- `tie_prob` (`np.ndarray`): Array of tie probabilities.
- `labels` (`np.ndarray`): Array of annotations.
- `letters` (`bool`): Use letter sequences for labels.
- `col` (`int`, optional): Column index for subplot placement. Defaults to `1`.

**Returns:**
- `plotly.graph_objs._figure.Figure`: Updated Plotly figure with the heatmap added.

### `bundled_maps`
Adds bundled heatmaps to a Plotly figure.

**Parameters:**
- `fig` (`plotly.graph_objs._figure.Figure`): The Plotly figure object.
- `win_prob` (`np.ndarray`): Array of win probabilities for the first dataset.
- `tie_prob` (`np.ndarray`): Array of tie probabilities for the first dataset.
- `labels` (`np.ndarray`): Array of annotations for the first dataset.
- `win_prob2` (`np.ndarray`): Array of win probabilities for the second dataset.
- `tie_prob2` (`np.ndarray`): Array of tie probabilities for the second dataset.
- `labels2` (`np.ndarray`): Array of annotations for the second dataset.
- `letters` (`bool`): Use letter sequences for labels.
- `col` (`int`): Column index for subplot placement. Defaults to `2`.

**Returns:**
- `plotly.graph_objs._figure.Figure`: Updated Plotly figure with both heatmaps added.

### `get_data`
Retrieves and processes data from a JSON file.

**Parameters:**
- `path` (`str`): Path to the JSON data file.

**Returns:**
- `Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]`: Processed data arrays and simulation count.

### `format_data`
Formats raw probability data into percentage values and cleans the diagonal.

**Parameters:**
- `array` (`np.ndarray`): Array of raw probability values.

**Returns:**
- `np.ndarray`: Formatted array with percentages and cleaned diagonal.

### `fill_diag`
Fills the diagonal of a matrix with a specified filler.

**Parameters:**
- `array` (`np.ndarray`): Input array.
- `filler`: Value to fill the diagonal with.

**Returns:**
- `np.ndarray`: Array with filled diagonal.

### `make_annots`
Creates annotation strings from win and tie probabilities.

**Parameters:**
- `wins` (`np.ndarray`): Array of win probabilities.
- `ties` (`np.ndarray`): Array of tie probabilities.

**Returns:**
- `np.ndarray`: Array of annotation strings in the format "win(tie)".

### `validate_data`
Validates the size and format of the input data.

**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `IndexError`: If data size is not 8x8.
- `ValueError`: If probability values are out of range.

### `validate_numbers`
Ensures all probability values are within the range [0, 1].

**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `ValueError`: If any probability value exceeds 1.

### `validate_size`
Ensures the input data is an 8x8 array.

**Parameters:**
- `data` (`np.ndarray`): Input data array of 8x8 shape.

**Raises:**
- `IndexError`: If data is not 8x8.

### `validate_tie_existence`
Checks for the existence of tie data or annotations.

**Parameters:**
- `input_raw`: Raw tie data.
- `input_annots`: Annotation data.

**Raises:**
- `TypeError`: If both tie data and annotations are missing.

### `validate_existence`
Checks for the existence of a required input.

**Parameters:**
- `input`: Input to validate.

**Raises:**
- `TypeError`: If input is missing.

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

### `play(path, n, seed=0)`
**Parameters:**
- `path` (`str`): Path where you would like to store your data.
- `n` (`int`): The number of games you would like to run.
- `seed` (`int`, optional): The random seed to use. If none set, defaults to `0`.

**Description:**
The function stores data in a database format. If the database file already exists, the function will append to the existing database. For our structure, the data is stored in a `data/` folder. If data is being appended to an existing database, a different seed should be used so that duplicate decks are not generated. In every iteration, each possible combination of guesses from Player 1 and Player 2 will be tested, making 64 total games using one deck.

For more information on what exactly goes into the `play` function, check out the [data management documentation](data_mgmt.md).

### `heatmap(path)`
**Parameters:**
- `path` (`str`): Path where the database of decks is located.

**Description:**
Generates heatmaps based on the simulation data stored at the specified path. The function processes the data to visualize the probabilities and outcomes of Penney's Game variations. 

### The following defualt settings apply for png images:

Figure size: single heatmap - height=6, width=6, bundled heatmap - height=6, width=12
Title font size: 15
Axes:
X axis: title = “My Guesses”, title size = 12, tick size: 10
Y axis:title = “Opponent Guesses’, title size= 12,  tick size = 10
Annot (in each cell of heatmap) font size = 8
Linewidth =0.5
colormap= ‘Blues’
fmt =’’ (used to aid in displaying the annots)
Colorbar
Position for single = [.95, 0.11, 0.035, .77], position for bundled = [.93, 0.11, 0.02, .77]
Outline width = 0.2
Face color (background color) = #DBDBDB
vmin = 0, vmax=100
Wspace (for bundled) = 0.1

### The following default settings apply for html images:
Figure size: single heatmap - (height = 750, width = 750), bundled heatmap - (height=675, width=1300)
Title font size: 22
Title spacing: single - (x = 0.5, y = 0.94) bundle - (y = 1.05)
Axes:
X axis: title = 'My Guesses', title size=18, tick size=16
Y axis: title = 'Opponent Guesses', title size=18, tick size=16
showgrid=False for and x and y axes
xgap and ygap both = 1
Colors: ‘blues’
Tool tip text: Me: [x-value], Opponent: [y-value]
         My Win Probability: [win_prob]
         Tie Probability: [tie_prob], name = "",
hoverongaps = False                       
Colorbar
Tick positions [0, 20, 40, 60, 80, 100]
Tick labels [0, 20, 40, 60, 80, 100]
outlinewidth=1
outlinecolor="#E7E7E7"
zmin=0, zmax=100
Plot background color = #DBDBDB

