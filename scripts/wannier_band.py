import os
import sys
from jhr.plotters.express import wannbandsExpress
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler


title = 'CsPbBr3_wann'
dat_filename = 'CsPbBr3_band_wann.dat'
gnu_filename = 'CsPbBr3_band_wann.gnu'
savefolder = '../plots/wannier_bands'
# Load .dat file for Wannier bands
dat_file_wann = os.path.join('..', 'data', 'wann_band_files', dat_filename)
# Load the .gnu file contents as a string
gnu_file_wann = os.path.join('..', 'data', 'wann_band_files', gnu_filename)
# Define fermi energy and the range for valence and conduction band to find the bandgap
efermi = 1.9272
range_for_homo = efermi - 0.5
range_for_lumo = efermi + 0.3
#________________________________________PLOT SETTINGS______________________

savefile = os.path.join(savefolder, f"{title}")
settings = {
  
    'figure': {'figsize': (4,4)},
    'plot':{'x':[], 'y': [], 'alpha': 0.8}, 
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': [-4,6],
    #'axhline': {'y': [0], 'color': 'r', 'linestyle': '--'},
    # 'legend': {'frameon': False},
    'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

#________________________________________________

if __name__ == '__main__':
  wannbandsExpress(dat_file_wann, gnu_file_wann, efermi, settings)
  plt.show()

