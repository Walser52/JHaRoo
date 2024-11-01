"""
Module for aesthetics. Colors, markers etc. 
"""

import matplotlib.pyplot as plt
from numpy import arange

def select_colors_lines_markers(number = 5, solid_lines = 'first', palette = 'Nature'):
    """
    Usage:
        Create colors, lines and markers of required lenghts. 

        If solid_lines = 'first', 'all', 'none'. If 'all' then only solid lines are returned: ['-']*number.


        palette may be one of 'Nature', 'Mathematica', 'Custom_1', 'Mine'
    """
    markerstyles = ["o", "s", "^","*","P","p","x","1","2","3","4","8",",","<",".","v", ">"] # https://matplotlib.org/3.1.1/api/markers_api.html
    #https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    linestyles_tuples = [
        ('solid', 'solid'),
        ('dashed',                (0, (5, 5))),
        ('dotted',                (0, (1, 1))),
        ('densely dashed',        (0, (5, 1))),

        ('dashdotted',            (0, (3, 5, 1, 5))),
        ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),


        ('long dash with offset', (5, (10, 3))),

        ('loosely dashed',        (0, (5, 10))),
        ('loosely dotted',        (0, (1, 10))),
        ('loosely dashdotted',    (0, (3, 10, 1, 10))),
        ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),

        ('densely dotted',        (0, (1, 1))),

        ('densely dashdotted',    (0, (3, 1, 1, 1))),
        ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))
    ]

    palettes = {'Nature': ['#E64B35FF', '#3C5488FF', '#009F75', #red, blue, green
                           '#D54799',
                           '#2F7BBF', '#F39B7FFF','#00A087FF', '#8491B4FF', '#91D1C2FF', '#DC0000FF', '#7E6148FF', '#B09C85FF'],
                'Mathematica': ['#5E81B5', '#E19C24', '#8FB131', '#EC6235', '#8778B3'],
                'Custom_1': ['#1f77b4',  # muted blue
                               '#ff7f0e',  # safety orange
                               '#2ca02c',  # cooked asparagus green
                               '#d62728',  # brick red
                               '#9467bd',  # muted purple
                               '#8c564b',  # chestnut brown
                               '#e377c2',  # raspberry yogurt pink
                              '#7f7f7f',  # middle gray
                               '#bcbd22',  # curry yellow-green
                               '#17becf'  # blue-teal
                               ],
                'Mine':['#9A2617', '#093145', '#829356', '#9F6E2D', '#C2571A', '#107896', '#7030A0'],
                'Intense': ['#E64B35FF',  '#3C5488FF', '#2E8B57', '#F7B32BFF' ],
                'Muted': [],
                'Bright': [],
                
                


                #_____Qualitative_____
                'Category_1': ['#ff595e','#1982c4', '#82bc24','#ffca3a',  '#6a4c93'], #Tested -> Good
                'Category_2': ['#E64B35FF','#00CD6C','#AF58BA','#F28522'],
                'Category_3': ['#F13F3F','#4861B7', '#36AB6B','#B177DE', '#515151'], #Red, Blue, Green, Violet, Brown
                'up_to_four': ['#E9002D','#E19C24', '#009ADE','#00B000','#FFAA00',  ], #red, amber, green, blue
                
                'Branded':["#00798c", "#d1495b","#edae49","#66a182","#2e4057","#8d96a3"], #blue, red, yellow, green, navy, grey. See https://www.garrickadenbuie.com/blog/custom-discrete-color-scales-for-ggplot2/


                
                #____Seqeuential____
                'Sequential_Blues': ['#a0cbe2', '#8bc0dd', '#76b4d8', '#62a8d3', '#519ccc', '#4090c5', '#3282be', '#2474b7', '#1967ad', '#0f59a3', '#084c94', '#083e80', '#08306b'],
                'Sequential_Teal':['#B7E6A5','#7CCBA2','#46AEA9','#089099','#00718B','#045275','#003147'],
                'Sequential_Gray':['#000000', '#121212', '#242424', '#373737', '#494949', '#5b5b5b', '#6d6d6d', '#808080', '#929292', '#a4a4a4', '#b6b6b6', '#c8c8c8', '#dbdbdb', '#ededed'],
                'Sequential_Greens': ['#b3e1ad', '#a3da9d', '#90d18d', '#7dc87e', '#69bf71', '#54b466', '#3fa95c', '#339c52', '#268e48', '#18823d', '#097533', '#006729', '#005522', '#00441b']
                #____Diverging____
                #____Cyclic____

               }
    
    #__________Select__________
    try:
        lines = [line for (name, line) in linestyles_tuples[0:number]]
        
        markers = markerstyles[0:number]
        
        colors = palettes[palette][0:number]
        #print(palette, "\n", colors)
    except: 
        if number > len(palette) or number > len(markers) or number > len(lines):
            print("number greater than available options. Select different set.")

    #____________Overrides________________
    if solid_lines =='all': lines = ['-'] * number
    if solid_lines =='none': lines = [line for (name, line) in linestyles_tuples[1:number+1]]

    return colors, lines, markers



def show_palette(colors):
    """
    Converts a list of colors into a color palette.

    Usage:
      colors = ['c', 'm', 'y', 'k', 'r', 'g', 'b', '#FF5733']
      show_palette(colors)
    """
  
    # Number of colors
    num_colors = len(colors)
    
    # Create a figure with a single subplot
    fig, ax = plt.subplots(figsize=(num_colors, 1))  # Adjust figure size for better visibility

    # Create an array for the color squares
    for i, color in enumerate(colors):
        # Draw a rectangle for each color
        rect = plt.Rectangle((i, 0), 1, 1, color=color)
        ax.add_patch(rect)
    
    # Set the limits and aspect
    ax.set_xlim(0, num_colors)
    ax.set_ylim(0, 1)
    ax.set_xticks(arange(num_colors) + 0.5)  # Center ticks
    ax.set_xticklabels(colors, rotation=45, ha='center')
    ax.set_yticks([])  # Hide y ticks
    ax.set_title('Color Palette')

    plt.show()



