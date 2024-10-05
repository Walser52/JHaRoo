import os
from jhr.plotters.express import bandsExpress
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler



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
    'figure': {'figsize': (4,4)},
    'plot':{'x':[], 'y': [], 'alpha': 0.8}, 
    'xlabel': 'k points', 
    'ylabel': 'Energy (eV)',
    'ylim': [-4,10],
    'legend': {'frameon': False},
    'savefig': {'fname':savefile+'.png', 'format':'png', 'transparent':True, 'dpi': 300}
  
}

toskip = list(range(0, 12)) + []
#-------------------------------------------

if __name__ == '__main__':
  bandsExpress(data_file, high_symmetry_points, efermi, toskip, settings)
  plt.show()



