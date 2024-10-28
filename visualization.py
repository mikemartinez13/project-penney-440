import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional 
import random
import json
import os
import plotly 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Union
from typing import Tuple

##global settings for .png figure
FIG_HIGH = 6
FIG_WIDE = 6
TITLE_SIZE = 15
LABEL_SIZE = 12
TICK_SIZE = 10
ANNOT_SIZE = 8

def create_html(win_prob:np.ndarray, tie_prob:np.ndarray, labels:np.ndarray, n:int, 
                title: 'str', bundled = False, letters = True, 
                **kwargs,) -> plotly.graph_objs._figure.Figure:
    win_prob2 = kwargs.get('win_prob2', None) #np.ndarray
    tie_prob2 = kwargs.get('tie_prob2', None) #np.ndarray
    labels2 = kwargs.get('labels2', None) #np.ndarray
    n2 = kwargs.get('n2', None) #int
    title2 = kwargs.get('title2', None) #str
    
    data1=np.flip(win_prob,0)
    tie1=np.flip(tie_prob,0)
    
    if bundled == False: #if bundled == False which is the default
        title = title
        fig = make_subplots(rows = 1, cols = 1)
        single_map(fig, data1, tie1, labels, letters)
        fig.update_layout(height = 750, width = 750)
        fig.update_layout(title = title, 
                          title_x = 0.5,
                          title_y = 0.94,
                          title_font_size = 22)
    else: #if bundled == True this has to be specified
        data2 = np.flip(win_prob2,0) #if bundled = true, a second set of data is required 
        tie2 = np.flip(tie_prob2,0)
        titles = (title, title2)
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles= titles)
        bundled_maps(fig, data1, tie1, labels, data2, tie2, labels2, letters, col = 2)
        fig.update_layout(height=675, width=1300)
    fig.update_layout(
        xaxis = dict(
            title = 'My Guesses',
            title_font = dict(size=18),
            tickfont=dict(size=16)
        ),
        yaxis = dict(
            title = 'Opponent Guesses',
            title_font = dict(size=18),
            tickfont=dict(size=16)))
    for annotation in fig['layout']['annotations']:
        annotation['y'] = 1.05
        annotation['font'] = dict(size=22)
    fig.update_traces(xgap = 1, ygap = 1)
    if bundled == True:
        fig.update_layout(
        xaxis2 = dict(
            title = 'My Guesses',
            title_font = dict(size=18),
            tickfont=dict(size=16)
        ),
        yaxis2 = dict(
            tickfont=dict(size=16)))

    return fig


def single_map(fig:plotly.graph_objs._figure.Figure, win_prob:np.ndarray, tie_prob:np.ndarray, labels:np.ndarray, letters: bool, col = 1) -> plotly.graph_objs._figure.Figure:#data need to be formatted
    '''
    Creates the basics of a single heatmap. This function is used once to make a solo heatmap
    and twice to make a bundled heatmap. Returns the 
    '''
    if letters == True:
        x = ['BBB','BBR','BRB','BRR','RBB','RBR','RRB','RRR']
        y = ['BBB','BBR','BRB','BRR','RBB','RBR','RRB','RRR']
    else:
        x = ['000','001','010','011','100','101','110','111']
        y = ['000','001','010','011','100','101','110','111']
    fig.add_trace(
        go.Heatmap(z = win_prob, colorscale = 'blues',customdata = tie_prob,
                       hovertemplate = "Me: %{x}, Opponent: %{y}<br>My Win Probability: %{z}%<br>Tie Probability: %{customdata}%", name = "",
                       text = np.flip(labels,0), texttemplate='%{text}',
                       x = x, y = y,
                       hoverongaps = False,
                       colorbar=dict(
                           tickvals=[0, 20, 40, 60, 80, 100],  # Positions of the ticks
                           ticktext=[0, 20, 40, 60, 80, 100],   # Labels for the ticks
                           outlinewidth=1,  # Thin outline width
                           outlinecolor="#E7E7E7"),
                       zmin=0,
                       zmax=100),
        row = 1, col = col)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        margin=dict(t=100),
        plot_bgcolor="#DBDBDB")
    return fig

def bundled_maps(fig:plotly.graph_objs._figure.Figure, win_prob:np.ndarray, tie_prob:np.ndarray, labels:np.ndarray, win_prob2:np.ndarray, tie_prob2:np.ndarray, labels2:np.ndarray, letters:bool, col:int) -> plotly.graph_objs._figure.Figure:
    return single_map((single_map(fig, win_prob, tie_prob, labels, letters)), win_prob2, tie_prob2, labels2, letters, col = 2)


def get_data(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
    '''
    Access the results/results.json file and returns the necessary arrays and n in order to make heatmaps where the user specifies no data
    '''
    ##Check if the file exists, if not an error will appear
    if not os.path.exists(path):
        raise FileNotFoundError('File does not exist. See more details below.')
    with open(path, 'r') as openfile:
    	json_object = json.load(openfile) 	# Reading from json file
    var_cards = np.array(json_object['cards'])
    var_tricks = np.array(json_object['tricks'])
    card_ties= np.array(json_object['card_ties'])
    trick_ties = np.array((json_object['trick_ties']))
    n = json_object['n']
    return var_cards,var_tricks, card_ties, trick_ties, n

def format_data(array: np.ndarray) -> np.ndarray:
    '''
    Cleans the array of probabilities in decimal form to return whole numbers 
    representing the percent out of 100 and fill the 'nonsense' diagonal with None 
    in order to display the diagonal as blank in the final visualization. 
    The rounding is done here before getting passed into make_heatmap so that if two squares represent the same integer (such as 0 and 0) on the annotations, they will have the exact same color.
    '''
    temp=np.round((array)*100,0)
    final = fill_diag(temp, None)
    return final
    
def fill_diag(array: np.ndarray, filler) -> np.ndarray:
    '''
    Sets the diagonal going up (left to right across) to whatever the user specifies as filler. 
    Done when making annotations (filler = "") and when formatting the data (filler=None)
    '''
    
    flipped = np.flip(array, 0)
    np.fill_diagonal(flipped, filler)
    return np.flip(flipped,0)

def make_annots(wins : np.ndarray,ties: np.ndarray) -> np.ndarray:
    '''
    Uses two 8x8 arrays for wins and ties respectively to return one array of strings in the form win(tie)
    The input arrays will need to already have gone through the format_data function or be in that format already
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(f'{str(wins[i,j])[:-2]} ({str(ties[i,j])[:-2]})')
        annots.append(row)
    annots=fill_diag(annots, "")
    return np.array(annots)

def validate_data(data: np.ndarray) -> None:
    '''
    Checks both the size and whether the data is in the correct initial format. When triggered additional message will display saying more details.
    '''
    try:
        validate_size(data)
    except Exception as e:
        raise IndexError('Data was not of 8 x 8 size. See more details below.') from None ##have from None so it doesn't have repeating messages, 
        ##IndexError because it relates to size (data could be bigger than 8 x 8 potentially)

    try:
        validate_numbers(data)
    except Exception as e:
        raise ValueError('Data does not represent the raw values of probability. See more details below.') from None ##have from None so it doesn't have repeating messages
    return 

def validate_numbers(data: np.ndarray) -> None :
    '''
    Ensures that the data provided by the user is in raw format
    '''
    for i in data:
        for j in i:
            if j >1.0:
                raise ValueError("At least one probability value is above 1.")
    return

def validate_size(data: np.ndarray) -> None :
    '''
    Ensures data given by the user fits the project's guidelines of an 8 x 8 array

    '''
    if data.shape != (8,8):
        raise IndexError("Data is not in an 8 x 8 array.") ##IndexError because it relates to size (data could be bigger than 8 x 8 potentially)
    return

def validate_tie_existence(input_raw, input_annots) -> None:
    '''
    If the user inputs their own data, they must either have raw tie data or already made annotations to prove their existence.
    '''
    if (input_raw is None) & (input_annots is None):
        raise TypeError("You are missing tie data. See details below.") ##raising type error because user would be missing a 'required' argument
    return

def validate_existence(input) -> None:
    if input is None:
        raise TypeError("You are missing an essential argument. See details below.") ##raising type error because user would be missing a 'required' argument
    return

def validate_and_process_input(n: Optional[int]=None, 
                               win_type: Optional[str]=None, 
                               data_ties: Optional[np.ndarray]=None, 
                               annots: Optional[np.ndarray]=None, 
                               data: Optional[np.ndarray]=None) -> Tuple[int, str, Optional[np.ndarray],Optional[np.ndarray], np.ndarray] : 
    ##checking if n was given if data was given
    try:
        validate_existence(n)
    except Exception as e: ##if you provided data, you have to provide n
        raise TypeError ("You did not provide an n.") from e ##raising type error because user would be missing a 'required' argument

    ##maybe add a check if win_type was specified
    try:
        validate_existence(win_type)
    except Exception as e: ##if you provided data, you have to provide n
        raise TypeError ("You did not provide a win type.") from e ##raising type error because user would be missing a 'required' argument

    ##have to validate tie existence because heatmap doesn't make sense without ties
    
    try: 
        validate_tie_existence(data_ties, annots)
    except Exception as e:
        raise TypeError('Your winning probabilites do not have tie probabilities attached.') from e ##raising type error because user would be missing a 'required' argument
  
    ##check if data in correct form and size
    try: 
        validate_data(data)
    except Exception as e:
        raise ValueError('Your data about winning the game is either of the wrong size or format.') from e ##ValueError because function recieved data of proper type but inappropriate value
    data=format_data(data) ##data is now being put into correct format
    
    ## if data_ties was given, we need to make sure its in raw form and in the correct size
    if isinstance(data_ties, np.ndarray): 
        try:
            validate_data(data_ties)
        except Exception as e:
            raise ValueError('Your data about tieing the game is either of the wrong size or format.') from e ##ValueError because function recieved data of proper type but inappropriate value
        data_ties=format_data(data_ties)
        ##data is now sufficiently validated to make annots
        annots=make_annots(data, data_ties) ##if the user had other annots they are overwritten, as the tie and true data are more accurate 
    
    ##check if annotations created/given by the user are in the correct format
    try:
        validate_size(annots) 
    except Exception as e:
        raise ValueError('The annotations you provided are of the wrong size. Please change them or call the function with your win and tie probabilities instead.') from e ##ValueError because function recieved data of proper type but inappropriate value

    
    
    return n, win_type, data_ties, annots, data

def make_heatmap(data: Optional[np.ndarray]=None,
                 data_ties:Optional[np.ndarray]=None,
                 annots: Optional[np.ndarray]=None,    
                 n: Optional[int]=None,
                 win_type: Optional[str]=None,
                 title: str= "My Chance of Winning",
                 hide_y: bool = False,
                 cbar_single: bool = True,
                 ax: plt.Axes = None,
                 bundle: bool = False,
                 letters: bool =True,
                 format: str ='png') -> Union[Tuple[plt.Figure, plt.Axes],plotly.graph_objs._figure.Figure]: 

    ##If user specified their own probability data: 
    #(in the case they did not but specified other arguments, our default data (in results/results.json) will be used and use our default settings to be accurate to the default data)
    if isinstance(data, np.ndarray): 
        
        ##Testing if other data that should have been passed in with user data is correct, formatting it as needed
        try:
            n, win_type, data_ties, annots, data = validate_and_process_input(n, win_type, data_ties, annots, data)
        except Exception as e:
            raise ValueError("There is something wrong with the data you passed in.") from e ##generic value error since the overall input could be wrong

        
        if win_type == 'cards':
            title = title+' (by Cards)\n(n='+str(n)+')'
        elif win_type == 'tricks':
            title= title+' (by Cards)\n(n='+str(n)+')'
        
        if format=='png':
            fig, ax =make_heatmap_backend(data, annots, title, hide_y, cbar_single, ax, letters) 
            fig.savefig('figures/heatmap_'+win_type+"_n"+str(n)+".png", bbox_inches = 'tight', facecolor = 'white')


        elif format=='html':
            ## ensures data_ties exists since they are needed for the tool tips
            try:
                validate_existence(data_ties)
            except Exception as e: 
                raise TypeError ("You did not provide raw tie data which is required to make an html.") from e
            single_html=create_html(win_prob=data, tie_prob=data_ties, labels= annots, bundled=False, letters=letters, title=title, n=n)
            path = 'figures/heatmap_'+win_type+"_n"+str(n)+".html"
            single_html.write_html(path)
            return single_html
        

    else: ##if data and any other arguments that would imply the user has their own data == None:
        '''
        If the user did not insert any data at all, make_heatmap() will make heatmaps of existing data in the results/results.json file.
        It accesses that data through the get_data(path) function.
        Heatmaps for cards, tricks, and both will be created if win_type is not specified. The user can also specify bundle=True if they only want the bundled package
        If this file does not exist, an error message will appear.
        
        '''
        try:
            var_cards,var_tricks, card_ties, trick_ties, n_default = get_data('results/results.json') 
        except Exception as e:
            raise FileNotFoundError('results/results.json does not exist. You should run the simulate data function') from e

        if win_type=='cards':##makes visualization just for cards (win type specified in saved file)
            title_cards=title+' (by Cards)\n(n='+str(n_default)+')'
            var_cards = format_data(var_cards)
            card_ties= format_data(card_ties)
            ct_annots=make_annots(var_cards, card_ties) 
            if format == 'png':
                fig,ax=make_heatmap_backend(data=var_cards, annots=ct_annots, title=title_cards, letters = letters)
                fig.savefig('figures/heatmap_'+win_type+'_n'+str(n_default)+".png", bbox_inches = 'tight', facecolor = 'white')

                
            elif format == 'html':
                single_html=create_html(win_prob=var_cards, tie_prob=card_ties, labels= ct_annots, bundled=False, letters=letters, title=title_cards, n=n_default)
                path = 'figures/heatmap_'+win_type+"_n"+str(n_default)+".html"
                single_html.write_html(path)
                return single_html
            

        elif win_type == 'tricks': ##makes visualization just for cards (win type specified in saved file)
            title_tricks=title+' (by Tricks)\n(n='+str(n_default)+')'
            var_tricks = format_data(var_tricks)
            trick_ties = format_data(trick_ties)
            tt_annots=make_annots(var_tricks, trick_ties)
            if format == 'png':
                fig,ax= make_heatmap_backend(data=var_tricks, annots=tt_annots, title=title_tricks, letters = letters)
                fig.savefig('figures/heatmap_'+win_type+"_n"+str(n_default)+".png", bbox_inches = 'tight', facecolor = 'white')

            elif format == 'html':
                single_html=create_html(win_prob=var_tricks, tie_prob=trick_ties, labels= tt_annots, bundled=False, letters=letters, title=title_tricks, n=n_default)
                path = 'figures/heatmap_'+win_type+"_n"+str(n_default)+".html"
                single_html.write_html(path)
                return single_html

        else:
            #makes visualization for cards, tricks, and bundled, with bundled appearing first to save time in make_heatmap_package()
            title_cards=title+' (by Cards)\n(n='+str(n_default)+')'
            title_tricks=title+' (by Tricks)\n(n='+str(n_default)+')'
            ct_annots=make_annots(format_data(var_cards), format_data(card_ties))
            tt_annots=make_annots(format_data(var_tricks), format_data(trick_ties))
            if format =='png':
                fig_b, ax_b= make_heatmap_package(data1=var_cards, data2=var_tricks, labels1=ct_annots, labels2=tt_annots, title1=title,
                                                  title2=title, n1=n_default, n2=n_default, win_type1='cards', win_type2='tricks', letters=letters) ##make_heatmap_package adjusts the titles within it
                fig_b.savefig('figures/heatmap_packaged_cards_tricks_n'+str(n_default)+".png", bbox_inches = 'tight', facecolor = 'white')
                
                if bundle:
                    return fig_b, ax_b
                
                fig_c,ax_c =make_heatmap_backend(data=format_data(var_cards), annots=ct_annots, title=title_cards,  letters = letters) ##make_heatmap backend requires the title to have been already finalized
                fig_t,ax_t =make_heatmap_backend(data=format_data(var_tricks), annots=tt_annots, title=title_tricks,letters = letters)
                fig_c.savefig('figures/heatmap_cards_n'+str(n_default)+".png", bbox_inches = 'tight', facecolor = 'white')
                fig_t.savefig('figures/heatmap_tricks_n'+str(n_default)+".png", bbox_inches = 'tight', facecolor = 'white')

                return fig_b, ax_b 

            elif format == 'html':
                
                bundle_html=create_html(bundled=True, win_prob=format_data(var_cards), title=title_cards,tie_prob=format_data(card_ties), labels=ct_annots, n=n_default,
                                        win_prob2=format_data(var_tricks), 
                                        tie_prob2=format_data(trick_ties), labels2=tt_annots, n2=n_default, title2=title_tricks)
                bundle_html.write_html('figures/heatmap_packaged_cards_tricks_n'+str(n_default)+".html")
                
                if bundle: 
                    return bundle_html
                    
                card_html=create_html(win_prob=format_data(var_cards), tie_prob=format_data(card_ties), labels= ct_annots, bundled=False, letters=letters, title=title, n=n_default) #-- bundle = false (cards)
                card_html.write_html('figures/heatmap_cards_n'+str(n_default)+".html")
                trick_html=create_html(win_prob=format_data(var_tricks), tie_prob=format_data(trick_ties), labels= tt_annots, bundled=False, letters=letters, title=title, n=n_default) #-- bundle == false (tricks)
                trick_html.write_html('figures/heatmap_tricks_n'+str(n_default)+".html")
                bundle_html.show() 
                card_html.show()
                trick_html.show()
                return bundle_html
 
    return fig, ax
        

def make_heatmap_backend(data: np.ndarray,
                 annots: np.ndarray,
                 title:str,
                 hide_y: bool = False,
                 cbar_single: bool = True,
                 ax: plt.Axes = None,
                 letters: bool = True) -> [plt.Figure, plt.Axes]: 
   
    '''
    If ax is None, create a new figure.
    Otherwise, add the heatmap to the provided ax.
    '''
    
    if ax is None:
        # Create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDE, FIG_HIGH))
    else:
        # Get the parent figure
        fig = ax.get_figure()

    
    seqs= ['BBB','BBR','BRB','BRR','RBB','RBR','RRB','RRR'] #if letters are desired tick labels
    if letters == False:
        seqs = [f'{i:b}'.zfill(3) for i in range(8)] ##if numbers are desired tick labels

    settings = {
        'vmin': 0,
        'vmax': 100,
        'linewidth': .5,
        'cmap': 'Blues',
        'cbar': False,
        'annot_kws': {"size": ANNOT_SIZE},
        'fmt': ''
    }

    
    sns.heatmap(data=data, ax=ax,  annot=annots,**settings)
    ax.set_xlabel('My Guesses', fontsize=LABEL_SIZE)
    ax.set_ylabel('Opponent Guesses', fontsize=LABEL_SIZE)
    ax.set_xticklabels(seqs, fontsize=TICK_SIZE)
    ax.set_yticklabels(seqs[::-1], fontsize=TICK_SIZE)
    ax.set_facecolor('#DBDBDB')

    '''
    If a standalone plot is being created, the colorbar should be adjusted in this make_heatmap function 
    If bundled heatmaps are being made, the colorbar will be adjusted in the make_heatmap_package function to avoid double colorbars
    '''

    if cbar_single: 

        cbar_ax = fig.add_axes([.95, 0.11, 0.035, .77])
        cb = fig.colorbar(ax.collections[0], cax=cbar_ax)
        #adjusting the tickmark sizes on colorbar 
        cb.ax.tick_params(labelsize=TICK_SIZE)
        cb.outline.set_linewidth(.2)


    ax.set_title(title, fontsize=TITLE_SIZE) 

    
    if hide_y: ### for bundled heatmaps, both the yticks and axis title should be hidden on 2nd subplot
        ax.set_yticks([])
        ax.set_ylabel(None)
     
    return fig, ax


    
def make_heatmap_package_backend(data1: np.ndarray, 
                         data2: np.ndarray,
                         title1: str,
                         title2: str,
                         n1:int,
                         n2: int,
                         win_type1: str,
                         win_type2:str,
                         data1_ties:Optional[np.ndarray]=None,
                         data2_ties:Optional[np.ndarray]=None,
                         labels1: Optional[np.ndarray]=None,
                         labels2: Optional[np.ndarray]=None,
                         letters: bool = True
                        ) -> [plt.Figure, plt.Axes]:
    
    '''
    Create a 1x2 grid of heatmaps based on the given data
    '''


    gridspec_kw = {'wspace': 0.1,
                  }

    fig, ax = plt.subplots(1, 2, 
                           figsize=(FIG_WIDE*2, FIG_HIGH), 
                           gridspec_kw=gridspec_kw)
    
    #setting the titles appropriately
    titles=[title1, title2]
    win_types=[win_type1, win_type2]
    n_list=[n1,n2]
    for i, title in enumerate(titles):
        if win_types[i]=='cards':
            titles[i]=title+' (by Cards)\n(n='+str(n_list[i])+')'
        else:
            titles[i]=title+' (by Tricks)\n(n='+str(n_list[i])+')'
    title1=titles[0]
    title2=titles[1]
  
    


    make_heatmap_backend(data1, ax=ax[0], 
                 title=title1, annots=labels1, cbar_single=False, letters = letters
                )

    make_heatmap_backend(data2, ax=ax[1], annots=labels2,
                 title=title2, cbar_single=False,
                 hide_y=True,  letters = letters)

    cbar_ax = fig.add_axes([.93, 0.11, 0.02, .77])
    cb = fig.colorbar(ax[0].collections[0], cax=cbar_ax)
    cb.ax.tick_params(labelsize=TICK_SIZE)
    cb.outline.set_linewidth(.2)
    


    
    return fig, ax



def make_heatmap_package(data1: Optional[np.ndarray]=None, 
                         data2: Optional[np.ndarray]=None,
                         title1: Optional[str]="My Chance of Winning", 
                         title2: Optional[str]="My Chance of Winning",
                         n1:Optional[int]=None,
                         n2: Optional[int]=None,
                         win_type1: Optional[str]=None,
                         win_type2:Optional[str]=None,
                         data1_ties:Optional[np.ndarray]=None,
                         data2_ties:Optional[np.ndarray]=None,
                         labels1: Optional[np.ndarray]=None,
                         labels2: Optional[np.ndarray]=None,
                         letters: bool = True,
                         format: str = 'png'
                        ) -> Union[Tuple[plt.Figure, plt.Axes],plotly.graph_objs._figure.Figure] :

    if isinstance(data1, np.ndarray) or isinstance(data2, np.ndarray): 
        ##if the user specified at least one piece of 8 x8 probability data then the other should exist as well
        try:
            validate_existence(data1)
            validate_existence(data2)
            
        except Exception as e:
            raise TypeError("You inserted only 1 piece of probability data. Please provide another.") from e ##TypeError because user is missing 'required' argument
        
        ##validating/processing first set of data
        try:
            n1, win_type1, data1_ties, labels1, data1=validate_and_process_input(n1, win_type1, data1_ties, labels1, data1)
        except Exception as e:
            raise ValueError("There is something wrong with the data you gave corresponding to the first set.") from e ##generic value error since the overall input could be wrong

        ##validating/processing second set of data
        try:
            n2, win_type2, data2_ties, labels2, data2=validate_and_process_input( n2, win_type2, data2_ties, labels2, data2)
        except Exception as e:
            raise ValueError("There is something wrong with the data you gave corresponding to the second set.") from e ##generic value error since the overall input could be wrong

        ##making heatmaps corresponding to format
        if format == 'png':
            fig, ax=make_heatmap_package_backend(data1=data1, data1_ties=data1_ties, data2=data2, 
                                   data2_ties=data2_ties,title1=title1, 
                                   title2=title2, n1=n1, n2=n2, win_type1=win_type1, win_type2=win_type2, labels1=labels1, labels2=labels2, letters=letters)
            fig.savefig('figures/heatmap_packaged_'+win_type1+"_n"+str(n1)+win_type2+"_n"+str(n2)+".png", bbox_inches = 'tight', facecolor = 'white')

        if format == 'html':
            html_b=create_html(bundled=True, win_prob=data1, tie_prob=data1_ties, title1=title1, labels=labels1, win_prob2=data2, tie_prob2=data, labels2=labels2, n2=n2, title2=title2, letters=letters)
            html_b.write_html('figures/heatmap_packaged_'+win_type1+"_n"+str(n1)+win_type2+"_n"+str(n2)+".html")

            return html_b
    else:
        if format == 'png':
            fig, ax=make_heatmap(bundle=True, letters=letters) ##saved in make_heatmap function 
        if format == 'html':
            html_b=make_heatmap(bundle=True, letters=letters, format='html') ##saved in make_heatmap function
            return html_b
    return fig, ax








