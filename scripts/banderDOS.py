import matplotlib.pyplot as plt
import numpy as np
import os
import glob

from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

from jhr.plotters._base import createTag, annotate, ax_divider
from matplotlib.gridspec import GridSpec

from cycler import cycler

# from materials.CsPbBr3_info import *
# from materials.CsPbI3_info import *
# from materials.CsPbBr2I_info import *
# from materials.CsPbBrI2_info import *

# mat = __import__('./materials/CsPbBrI2_info')


showplot = True

with open('materials/CsPbBrI2_info.py') as f:
    exec(f.read())

print(title)

title = 'grid'
#________Data settings___________

savefile = f'../plots/Grids/{title}'
DOS_cycler = cycler(color=['#003049', '#f77f00', '#B028C6', '#f2542d', '#562c2c'])

high_symmetry_points = {#Define High Symmetry Points
    '$\Gamma$'   : 0,
    'X'          : 30,
    'M'          : 60,
    '$\Gamma$ '  : 90,
    'R'          : 120,
    'X|M'        : 150,
    'R '         : 180
}


#_________Plot settings__________
#DOS Plot settings
plotsettingsDOS = {
    'plot':{'x':[], 'y': [], 'label': [], 'alpha': 0.8}, 
    'xlabel': 'DOS (states/eV)', 
    'set_prop_cycle': DOS_cycler,
    'xlim': xlimDOS,      
    'ylim': ylimDOS,
    'legend': {'frameon': False, 'ncol':2}}

#Bands Plot settings
plotsettingsBands = {
    'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': '#1C829C'}, 
    'yaxis.set_minor_locator': {'AutoMinorLocator': 2},
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': ylimBands,
    'legend': {'frameon': False},
}


plotsettingsW90Bands = {
    'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': 'green'}, 
}


#Create dictionary
mat = {'DOS': dict(pdos_folder = pdos_folder, totaldosfile = totaldosfile, 
                  toskip = toskipDOS, efermi = efermi, plotTDOS = plotTDOS, plotsettings = plotsettingsDOS),

      'bands': dict(data_file = bandsQEFile, plotsettings = plotsettingsBands, toskip = toskipbands, code = 'QE',
                    symmPoints = high_symmetry_points , efermi = efermi, 
                    showhomolumo = showhomolumo, homolumosettings = {'fontsize': 10}
                    
                    ),

      'w90bands': dict(data_file = (dat_file_wann, gnu_file_wann), plotsettings= plotsettingsW90Bands, efermi = efermi, toskip = [], code = 'W90')
}


fig, Axs =  plt.subplots(2, 2, figsize=(12, 12))  # 2 rows, 1 column

Axs = Axs.flatten()


for ax in Axs:
    plt.sca(ax)
    ax1, ax2 = ax_divider(ax, divisions = 2, direction = "right", pad = 0.2, share = True)

    plt.sca(ax1)
    bandsExpress(**mat['bands'])
    plt.sca(ax2)
    DOSExpress(**mat['DOS'])

plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

if showplot: plt.show()


#============PLOTTER==============

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8), sharey = True)  # 2 rows, 1 column

# plt.sca(ax2)
# DOSExpress(**mat['DOS'])

# plt.sca(ax1)
# bandsExpress(**mat['bands'])
# #bandsExpress(**mat['w90bands'])

# createTag(name = title, pos = (0.02, .95), weight = 'bold', fontcolor = '#555555' ,  bboxsettings = dict(alpha = 0))
# #annotate(append = '.')

# fig.tight_layout()
# plt.subplots_adjust(wspace=0.04, hspace=0)

# plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
# plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

# if showplot: plt.show()

  
#========================================


# plt.show()