import matplotlib.pyplot as plt
import numpy as np
import os
import glob

from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

from jhr.plotters._base import createTag, annotate


from cycler import cycler

from CsPbBr3 import *


custom_cycler = cycler(color=['lightblue']*36)

savefile = '../plots/Grids/CsPbBr3-All'

#Define High Symmetry Points
high_symmetry_points = {
    'gG1'   : 0,
    'X1'    : 30,
    'M1'    : 60,
    'gG2'   : 90,
    'R1'    : 120,
    'X2|M2' : 150,
    'R2'    : 180
}


#_________Plot settings__________
#DOS Plot settings
plotsettingsDOS = {
    #'figure': {'figsize': (4,8)},
    'plot':{'x':[], 'y': [], 'label': [], 'alpha': 0.8}, 
    'xlabel': 'DOS (states/eV)', 
#    'ylabel': 'Energy (eV)',
    'xlim': xlimDOS,      
    'ylim': ylimDOS,
    'legend': {'frameon': False},
#      'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

#Bands Plot settings
plotsettingsBands = {
    #'figure': {'figsize': (4,4)},
#    'title': title,
    'plot':{'x':[], 'y': [], 'alpha': 0.8}, 
    'set_prop_cycle': custom_cycler,
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': ylimBands,
    'legend': {'frameon': False},
    #'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}


plotsettingsW90Bands = {
    #'figure': {'figsize': (4,4)},
    'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': 'green'}, 
#    'set_prop_cycle': custom_cycler,
#    'xlabel': 'k points', 
#    'ylabel': 'Energy (eV)',
#    'ylim': [-4,10],
#    'legend': {'frameon': False},
    #'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}


range_for_homo = efermi - 0.1
range_for_lumo = efermi - 0.1

#====================================

#Create dictionary
mat = {'DOS': dict(pdos_folder = pdos_folder, totaldosfile = totaldosfile, 
                  toskip = toskipDOS, efermi = efermi, plotTDOS = plotTDOS, plotsettings = plotsettingsDOS),

      'bands': dict(data_file = bandsQEFile, plotsettings = plotsettingsBands, toskip = toskipbands, code = 'QE',
                    symmPoints = high_symmetry_points , efermi = efermi),

      'w90bands': dict(data_file = (dat_file_wann, gnu_file_wann), plotsettings= plotsettingsW90Bands, efermi = efermi, toskip = [], code = 'W90')

}


#============PLOTTER==============

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 10), sharey = True)  # 2 rows, 1 column

plt.sca(ax2)
DOSExpress(**mat['DOS'])

plt.sca(ax1)
bandsExpress(**mat['bands'])
bandsExpress(**mat['w90bands'])

createTag(name = title)
annotate(append = '.')


plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

plt.show()

  
