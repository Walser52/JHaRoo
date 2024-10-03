import os
from bands_sub import process_band_structure, get_high_symmetry_positions_and_labels, plot_bandstructure, plot_settings, find_bandgap
from bands_sub import plot_bands
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



if __name__ == '__main__':

  data = np.loadtxt(data_file)

  #______________DATA PREP_________________
  k, bands = process_band_structure(data) # Get k points and bands 
  positions, labels = get_high_symmetry_positions_and_labels(k, high_symmetry_points)
  homolumo, bandgap = find_bandgap(bands, range_for_homo, range_for_lumo)

  #_______________PLOT___________________
  
  settings = {
      'figure.figsize' : (4,6),
      'lines.linewidth'   : 1,
      'axes.labelsize'    : 14,
      'xtick.labelsize'   : 12,
      'ytick.labelsize'   : 12,
      'grid.linestyle'    : '-.',
      
   
  }

  #Define Colors
  colors = plt.cm.get_cmap('tab10').colors
  plt.gca().set_prop_cycle(cycler('color', colors))
   

#  plot_bandstructure(k, bands, positions, labels, efermi, title=title, bandgap_info=homolumo)
  toskip = list(range(0, 14))
  toskip = list(range(0, 12)) + []
  plot_bands(k, bands, positions, labels, efermi, skip = toskip)


  plot_settings(**settings)
  plt.ylim([-4,10])
  plt.xlim(min(positions), max(positions))


  # Save figure
  savefile = os.path.join(savefolder, f"{title}")
  plt.savefig(savefile+'.svg', format='svg', transparent=True)
  plt.savefig(savefile+'.png', format='png', transparent=True, dpi = 300)
  plt.show()



