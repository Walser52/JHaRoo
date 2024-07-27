from module1 import process_band_structure, get_high_symmetry_positions_and_labels, plot_bandstructure, plot_settings, find_bandgap
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
filename = 'aiida.bands.gnu'

filename = ['CsPbBr3.bands.gnu','relCsPbBr3.bands.gnu']

def readfile(filename):
  """
  Read data for file name.
  """
  data = np.loadtxt(filename)
  k, bands = process_band_structure(data)

  return k, bands

k0, bands0 = readfile(filename[0])
k1, bands1 = readfile(filename[1])
bands1 += 56


#k, bands = [readfile(file) for file in filename]

print(bands1.max(), bands1.min())
print(bands0.max(), bands0.min())


#__________________________Parameters_________________
k = k0

efermi = 3.6711
range_for_homo = efermi + 0.3
range_for_lumo = efermi + 0.1

title = 'CsPbI3'
high_symmetry_points = {
    'gG1'   : 0,
    'X1'    : 30,
    'M1'    : 60,
    'gG2'   : 90,
    'R1'    : 120,
    'X2|M2' : 150,
    'R2'    : 180
}
positions, labels = get_high_symmetry_positions_and_labels(k, high_symmetry_points)

define_plot_settings = {
    'figure.figsize' : (4,6),
    'lines.linewidth'   : 1,
    'axes.labelsize'    : 14,
    'xtick.labelsize'   : 12,
    'ytick.labelsize'   : 12,
    'grid.linestyle'    : '-.'
}

plot_settings(**define_plot_settings)

  #__________Define Colors
colors_reds = plt.cm.get_cmap('Blues')(np.linspace(0, 1, 10))
plt.gca().set_prop_cycle(cycler('color', colors_reds))

#=====================================================================

# Plot the bandstructure using imported function
plot_bandstructure(k0, bands0, positions, labels, efermi, title=title)

colors_greens = plt.cm.get_cmap('Greens')(np.linspace(1, 2, 10))
plt.gca().set_prop_cycle(cycler('color', colors_greens))

plot_bandstructure(k1, bands1, positions, labels, efermi, title=title)

plt.ylim([-10,10])
 
plt.show()
# Find the bandgap

for bands in [bands0, bands1]:
  bandgap = find_bandgap(bands, range_for_homo, range_for_lumo)
  if bandgap is not None:
      print(f"Bandgap: {bandgap:.4f} eV")
  else:
      print("No bands found near eFermi to calculate bandgap.")
# plt.show()

