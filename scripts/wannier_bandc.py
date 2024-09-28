import os
import sys
from wannier_bands_sub import read_datfile_wannier, read_gnu_file_wann, plot_settings, find_bandgap, plot_energy_bands # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler



base_dir = '../data/wann_band_files'
files = ['CsPbBr2I_band_wann', 'CsPBBr3_band_wann', 'CsPBBrI2_band_wann']

#title = files #Change if you want to plot titles.
title = [1,2,3]
efermi = [1,2,4]
homolumogaps = [(0.3, 0.1), (0.3, 0.1),(0.3, 0.1)] #homo-lumo gaps for each material.



#-------------------------------------
homolumo = [(ef + hl[0], ef + hl[1]) for ef, hl in zip(efermi, homolumogaps)] 

dat_file_wann = [os.path.join(base_dir, f+'.dat') for f in files]
data_dat =  [np.loadtxt(f) for f in dat_file_wann]

gnu_file_wann = [os.path.join(base_dir, f+'.gnu') for f in files]



def plotwannier(data_dat,gnu_file_wann,title, show = False, **kwargs):
  """
  

  **kwargs: 
      'efermi': Float value for efermi, 
      'homolumo': Tuple containing homo lumo values.
  """

  if 'efermi' in kwargs.keys(): efermi = kwargs['efermi']
  if 'homolumo' in kwargs.keys(): 
    homolumo = kwargs['homolumo']
    range_for_homo = homolumo[0]
    range_for_lumo = homolumo[1]

  #++++++++++++++++++++++++++++++++++++
  with open(gnu_file_wann, 'r') as file:
      gnu_content = file.read()  # Read the content of the .gnu file

  # Use the content directly (no need for a path)
  k_points, bands = read_datfile_wannier(data_dat)

  high_symmetry_points, other_settings = read_gnu_file_wann(gnu_content)  # Pass the content, not the file path

  positions = []
  labels = []

  # Iterate through high symmetry points
  for label, pos_list in high_symmetry_points.items():
      # Append all positions for the current label
      for position in pos_list:
          positions.append(position)
          labels.append(label)  # Keep the label, even if it repeats

  # Debugging: Print unique positions and labels
  print("Positions:", positions)
  print("Labels:", labels)

  # Ensure the lengths match
  if len(positions) != len(labels):
      print("Mismatch found: Positions and Labels do not match!")
  else:
      # Set custom ticks and labels for x-axis
      plt.xticks(positions, labels)

 
  define_plot_settings = {
      'figure.figsize' : (4,6),
      'lines.linewidth'   : 1,
      'axes.labelsize'    : 14,
      'xtick.labelsize'   : 12,
      'ytick.labelsize'   : 12,
      'grid.linestyle'    : '-.',
     
  }

  # x_limits = (k_points[0], k_points[-1])
  y_limits = (-4, 8) 

  plot_settings(**define_plot_settings)
  #Define Colors
  colors = plt.cm.get_cmap('tab10').colors
  plt.gca().set_prop_cycle(cycler('color', colors))

  # plt.xlim(x_limits)  
  plt.ylim(y_limits)
  plt.xlim(min(positions), max(positions))

  # Find the bandgap

  homo, lumo, bandgap = find_bandgap(bands, range_for_homo, range_for_lumo)
  if bandgap is not None:
      print(f"Bandgap: {bandgap:.4f} eV")
      bandgap_info = (homo, lumo)
  else:
      print("No bands found near eFermi to calculate bandgap.")
      bandgap_info = None
      # Plot the bandstructure using imported function

  plot_energy_bands(k_points, bands, high_symmetry_points, efermi, title=title, bandgap_info = bandgap_info)
  svg_file = os.path.join(f'{base_dir}/../../', 'plots', f"{title}")

  # Save the figure as SVG
  plt.savefig(svg_file+'.svg', format='svg', transparent=True)
  plt.savefig(svg_file+'.png', format='png', transparent=True)

  if show: plt.show()
  return 

for i in range(len(files)):
  settings = {'efermi': efermi[i], 'homolumo': homolumo[i]}
  plotwannier(data_dat[i], gnu_file_wann[i], title[i], **settings)

