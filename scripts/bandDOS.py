import matplotlib.pyplot as plt
import numpy as np
import os
import glob
#from QEplots import reader, prepareDOS#, plotDOS
from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

CsPbBr3 = {'efermi':1.9671,  }

CsPbBr2I = {}

CsPbBrI2 = {}

CsPbI3 = {}

mats = {'CsPbBr3': CsPbBr3,
        'CsPbBr2I':CsPbBr2I,
        'CsPbBrI2':CsPbBrI2,
        'CsPbI3': CsPbI3
}


#=====================PLOT 1=======================


#================= DOS=======================
title = 'CsPbI3'
pdos_folder = r'../data/pdos_files/CsPBI3_PDOS'

totaldosfile = 'aiida.pdos_tot'
saveto = '../plots/DFT_PDOS_atom_orb'
toskip = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':['s'], 'I':['s']}

#efermi = 1.9671 # CsPbBr3
#efermi = 3.1106 # CsPbBr2I
#efermi = 5.7132 # CsPbBrI2
efermi = 3.6711 # CsPbI3

#___________plotsettings

plotTDOS = True
#===============================================

#key = 'CsPbBr3'
#
#
#efermi = mats[key]['efermi']
#saveto = mats[key]['saveto']

settings = {
    #'figure': {'figsize': (4,8)},
    'plot':{'x':[], 'y': [], 'label': [], 'alpha': 0.8}, 
    'xlabel': 'DOS (states/eV)', 
    'ylabel': 'Energy (eV)',
    'xlim': [0,5],      
    'ylim': [-4,10],
    'legend': {'frameon': False},
#      'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 10))  # 2 rows, 1 column
plt.sca(ax2)

DOSExpress(pdos_folder, totaldosfile, toskip, plotTDOS, efermi, settings)
#plt.show()

#========================PLOT 2================




title = 'CsPbBr3'
filename = 'CsPbBr3.bands.gnu'
savefolder = '../plots/DFT_bands/'
data_file = os.path.join('..', 'data', 'band_files', filename)

# Fermi energy and the range for valence and conduction band to find the bandgap
efermi =1.9671
range_for_homo = efermi - 0.1
range_for_lumo = efermi - 0.1

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


#_____________Plot settings____________

savefile = os.path.join(savefolder, f"{title}")

settings = {
    #'figure': {'figsize': (4,4)},
    'plot':{'x':[], 'y': [], 'alpha': 0.8}, 
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': [-4,10],
    'legend': {'frameon': False},
    'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

toskip = list(range(0, 12)) + []
#-------------------------------------------

plt.sca(ax1)
bandsExpress(data_file, high_symmetry_points, efermi, toskip, settings)
plt.show()

  
