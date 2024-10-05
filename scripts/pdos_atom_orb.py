import matplotlib.pyplot as plt
import numpy as np
import os
import glob
#from QEplots import reader, prepareDOS#, plotDOS
from jhr.plotters.express import DOSExpress



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


settings = {
    'figure': {'figsize': (4,8)},
    'plot':{'x':[], 'y': [], 'label': [], 'alpha': 0.8}, 
    'xlabel': 'DOS (states/eV)', 
    'ylabel': 'Energy (eV)',
    'xlim': [0,5],      
    'ylim': [-4,10],
    'legend': {'frameon': False},
#      'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}




if __name__ == '__main__':

  DOSExpress(pdos_folder, totaldosfile, toskip, plotTDOS, efermi, settings)
  plt.show()
  
