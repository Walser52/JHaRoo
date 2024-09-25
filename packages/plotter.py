#________________________
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator, LogLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker 
def makeplot(fun, plotsettings):
    """
    Pass a dictionary plotsettings to create a generic plot. 
    
    Usage:
    
    Do not pass figsize if you want to use the old figure. 
    
    """
    
    if 'figure' in plotsettings.keys(): plt.figure(**plotsettings['figure'])

    ax = plt.gca()

    if 'inset_axes' in plotsettings.keys(): inset_axes(ax, **plotsettings['inset_axes'])
    
    
    #_________Make plot and set defaults___________
    if 'plot' in plotsettings.keys(): 
        fun(**plotsettings['plot'])
        if 'xscale' in plotsettings['plot'].keys():
            if plotsettings['plot']['xscale'] == 'log': ax.xaxis.set_major_locator(LogLocator(numticks=4)) 
        if 'yscale' in plotsettings['plot'].keys():
            if plotsettings['plot']['yscale'] == 'log': ax.yaxis.set_major_locator(LogLocator(numticks=3))

    ax.tick_params(axis='both', which = 'both', direction='in')
    ax.xaxis.set_major_locator(MaxNLocator(integer=False, prune='both', nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(integer=False, prune='both', nbins=4))
    
   
    #_____Changes to defaults____

    
    if 'xlim' in plotsettings.keys(): plt.xlim(plotsettings['xlim'])
    if 'ylim' in plotsettings.keys(): plt.ylim(plotsettings['ylim'])
    if 'xlabel' in plotsettings.keys(): plt.xlabel(plotsettings['xlabel'])
    if 'ylabel' in plotsettings.keys(): plt.ylabel(plotsettings['ylabel'])
    if 'xscale' in plotsettings.keys(): plt.xscale(plotsettings['xscale'])
    if 'yscale' in plotsettings.keys(): plt.yscale(plotsettings['yscale'])
    
    if 'legend' in plotsettings.keys(): plt.legend(**plotsettings['legend'])
    if 'tick_params' in plotsettings.keys(): ax.tick_params(**plotsettings['tick_params'])
    if 'xaxis.set_major_locator' in plotsettings.keys():ax.xaxis.set_major_locator(**plotsettings['xaxis.set_major_locator'])
    if 'yaxis.set_major_locator' in plotsettings.keys():ax.yaxis.set_major_locator(**plotsettings['yaxis.set_major_locator'])

    if 'axvline' in plotsettings.keys(): ax.axvline(**plotsettings['axvline'])
    if 'annotate' in plotsettings.keys(): ax.annotate(**plotsettings['annotate'])
    if 'colorbar' in plotsettings.keys(): plt.colorbar(**plotsettings['colorbar'])
    if 'set_prop_cycle' in plotsettings.keys(): plt.set_prop_cycle(**plotsettings['set_prop_cycle'])
    if 'savefig' in plotsettings.keys(): plt.savefig(**plotsettings['savefig'])
   
    return 

