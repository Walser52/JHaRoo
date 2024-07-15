from module1 import process_band_structure, get_high_symmetry_positions_and_labels, plot_bandstructure, plot_settings
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
filename = 'aiida.bands.gnu'
data = np.loadtxt(filename)

# Get k points and bands from imported function
k, bands = process_band_structure(data)
#Title
title = 'CsPbI3'
#Define High Symmetry Points
high_symmetry_points = {
    'gG1': 0,
    'X1': 30,
    'M1': 60,
    'gG2': 90,
    'R1': 120,
    'X2|M2': 150,
    'R2': 180
}

#Get positions and labels using imported function
positions, labels = get_high_symmetry_positions_and_labels(k, high_symmetry_points)

#Define Plot Settings

define_plot_settings = {
    'figure.figsize' : (4,6),
    'lines.linewidth'   : 1,
    'axes.labelsize'    : 14,
    'xtick.labelsize'   : 12,
    'ytick.labelsize'   : 12,
    'grid.linestyle'    : '-.'
}

plot_settings(**define_plot_settings)
#Define Colors
colors = plt.cm.get_cmap('tab10').colors
plt.gca().set_prop_cycle(cycler('color', colors))


# Plot the bandstructure using imported function
plot_bandstructure(k, bands, positions, labels, title=title)
plt.show()

