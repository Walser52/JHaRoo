import matplotlib.pyplot as plt
import numpy as np
import os
import glob

from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

from jhr.plotters._base import createTag, annotate


from cycler import cycler

# from materials.CsPbBr3_info import *
# from materials.CsPbI3_info import *
# from materials.CsPbBr2I_info import *
from materials.CsPbBrI2_info import *



DOS_cycler = cycler(color=['#003049', '#f77f00', '#B028C6', '#f2542d', '#562c2c'])


savefile = f'../plots/Grids/{title}'

#Define High Symmetry Points
high_symmetry_points = {
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
    #'figure': {'figsize': (4,8)},
    'plot':{'x':[], 'y': [], 'label': [], 'alpha': 0.8}, 
    'xlabel': 'DOS (states/eV)', 
    'set_prop_cycle': DOS_cycler,
#    'ylabel': 'Energy (eV)',
    'xlim': xlimDOS,      
    'ylim': ylimDOS,
    'legend': {'frameon': False, 'ncol':2},
#      'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

#Bands Plot settings
plotsettingsBands = {
    'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': '#1C829C'}, 
    #'set_prop_cycle': custom_cycler,
     'yaxis.set_minor_locator': {'AutoMinorLocator': 2},
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': ylimBands,
    'legend': {'frameon': False},
    #'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}


plotsettingsW90Bands = {
    'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': 'green'}, 
}

#___Homo Lumo Settings______
showhomolumo = 5
homolumo_textsettings = {'fontsize': 10}

#====================================

#Create dictionary
mat = {'DOS': dict(pdos_folder = pdos_folder, totaldosfile = totaldosfile, 
                  toskip = toskipDOS, efermi = efermi, plotTDOS = plotTDOS, plotsettings = plotsettingsDOS),

      'bands': dict(data_file = bandsQEFile, plotsettings = plotsettingsBands, toskip = toskipbands, code = 'QE',
                    symmPoints = high_symmetry_points , efermi = efermi, 
                    showhomolumo = showhomolumo, homolumosettings = homolumo_textsettings
                    
                    ),

      'w90bands': dict(data_file = (dat_file_wann, gnu_file_wann), plotsettings= plotsettingsW90Bands, efermi = efermi, toskip = [], code = 'W90')

}


#============PLOTTER==============

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8), sharey = True)  # 2 rows, 1 column

plt.sca(ax2)
DOSExpress(**mat['DOS'])

plt.sca(ax1)
bandsExpress(**mat['bands'])
#bandsExpress(**mat['w90bands'])

createTag(name = title, pos = (0.02, .95), weight = 'bold', fontcolor = '#555555' ,  bboxsettings = dict(alpha = 0))
#annotate(append = '.')

#fig.tight_layout()
plt.subplots_adjust(wspace=0.04, hspace=0)

plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

plt.show()

  
