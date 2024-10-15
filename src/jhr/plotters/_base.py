import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator, LogLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker 

def makeplot(fun, plotsettings):
    """
    Pass a dictionary plotsettings to create a generic plot. 
    

    
    Usage:
    
        - Do not pass figsize if you want to use the old figure. 
        - For plt.plot use 'x' and 'y' in 'plot' word for providing data i.e.:
                {'plot': {'x': [1,2,3], 'y': [3,4,5]}
    
    Example 1 (plt.plot):
        settings2 = {
            'figure': {'figsize': (4,4)},
            'plot':{'x':[4,4,4,5,3], 'y': [2,3,1,4,5], 'color':'green', 'alpha': 0.4}, 

            'xlabel': 'sigma1_traceAvlog10', 
            'xlim': [0.5,7.8],
            'ylabel': 'Frequency',
            'ylim': [1,2],
            'legend': {'frameon': False}
        }

        makeplot(plt.plot, settings2)
    
    
    """
    
    if 'figure' in plotsettings.keys(): plt.figure(**plotsettings['figure'])

    ax = plt.gca()

    if 'inset_axes' in plotsettings.keys(): inset_axes(ax, **plotsettings['inset_axes'])
    if 'set_prop_cycle' in plotsettings.keys(): ax.set_prop_cycle(plotsettings['set_prop_cycle'])   
    
    #_________Make plot and set defaults___________
    if 'plot' in plotsettings.keys(): 
        #-------Matplotlib's plt.plot needs a special hack----------
        if fun.__name__ == 'plot':
            x = plotsettings['plot'].pop('x')
            y = plotsettings['plot'].pop('y')
            
            fun(x, y, **plotsettings['plot'])
            
            plotsettings['plot']['x'] = x
            plotsettings['plot']['y'] = y
        #-------Else runs for plt.hist, plt.scatter etc.-------------
        else:
            fun(**plotsettings['plot'])
        if 'xscale' in plotsettings['plot'].keys():
            if plotsettings['plot']['xscale'] == 'log': ax.xaxis.set_major_locator(LogLocator(numticks=4)) 
        if 'yscale' in plotsettings['plot'].keys():
            if plotsettings['plot']['yscale'] == 'log': ax.yaxis.set_major_locator(LogLocator(numticks=3))

    ax.tick_params(axis='both', which = 'both', direction='in')
    ax.xaxis.set_major_locator(MaxNLocator(integer=False, prune='both', nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(integer=False, prune='both', nbins=4))


   
    #_____Changes to defaults____

    if 'title' in plotsettings.keys(): plt.title(plotsettings['title']) 
    if 'xlim' in plotsettings.keys(): plt.xlim(plotsettings['xlim'])
    if 'ylim' in plotsettings.keys(): plt.ylim(plotsettings['ylim'])
    if 'xlabel' in plotsettings.keys(): plt.xlabel(plotsettings['xlabel'])
    if 'ylabel' in plotsettings.keys(): plt.ylabel(plotsettings['ylabel'])
    if 'xscale' in plotsettings.keys(): plt.xscale(plotsettings['xscale'])
    if 'yscale' in plotsettings.keys(): plt.yscale(plotsettings['yscale'])
    
    if 'legend' in plotsettings.keys(): plt.legend(**plotsettings['legend'])
    if 'tick_params' in plotsettings.keys(): ax.tick_params(**plotsettings['tick_params'])
    if 'xticks' in plotsettings.keys(): plt.xticks(**plotsettings['xticks'])
    if 'yticks' in plotsettings.keys(): plt.yticks(**plotsettings['yticks'])
    if 'xaxis.set_major_locator' in plotsettings.keys():ax.xaxis.set_major_locator(**plotsettings['xaxis.set_major_locator'])
    if 'yaxis.set_major_locator' in plotsettings.keys():ax.yaxis.set_major_locator(**plotsettings['yaxis.set_major_locator'])

    if 'axvline' in plotsettings.keys(): ax.axvline(**plotsettings['axvline'])
    if 'axhline' in plotsettings.keys(): ax.axhline(**plotsettings['axhline'])
    if 'annotate' in plotsettings.keys(): ax.annotate(**plotsettings['annotate'])
    if 'colorbar' in plotsettings.keys(): plt.colorbar(**plotsettings['colorbar'])
    if 'savefig' in plotsettings.keys(): plt.savefig(**plotsettings['savefig'])
   
    

    return 


def createTag(pos = (0.017, 1.005), name = None, box_clr = 'red', edgecolor = 'black', alpha = 0.6, boxstyle = 'round', fontcolor = 'black', alignment = ('left', 'bottom')):
    """
    Purpose: 
        Create a tag at the top left corner of an axis. Use position to change x and y.
    """
    ax = plt.gca()
    ax.text(pos[0], pos[1], s = name, 
                bbox=dict(facecolor=box_clr, edgecolor = edgecolor, alpha=alpha, boxstyle=boxstyle), 
                color = fontcolor, horizontalalignment=alignment[0], verticalalignment=alignment[1],transform=ax.transAxes, )
    
    return


def annotate(fig = None, labels = 'abc', style = 'lower', parenthesis = False, size = 12, weight = 'bold', loc = (-0.13, 1.04), append = "", label_by = 'all '):
    """
    Annotate with a, b, c
    
    Args:
        label_by: 'row', 'col', 'all'
    """
    import string
    
    if fig == None: 
        fig = plt.gcf()
        
    if labels == 'abc':
        abc = list(string.ascii_lowercase)
        #abc = list(string.ascii_uppercase)
        labels = abc[:len(fig.axes)]
   
    for index, (label, ax) in enumerate(zip(labels, fig.axes)):
        ax.text(loc[0], loc[1], label+append,
        transform=ax.transAxes,
        size=size, weight=weight)
    return




