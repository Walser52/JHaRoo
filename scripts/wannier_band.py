import os
import sys
from wannier_bands_sub import read_datfile_wannier, read_gnu_file_wann, plot_settings, find_bandgap, plot_energy_bands # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current scriptp
# Load .dat file for Wannier bands
dat_file_wann = os.path.join(base_dir, '..', 'data', 'wann_band_files', 'relCsPBBr3_band_wann.dat')
data_dat = np.loadtxt(dat_file_wann)

# Load the .gnu file contents as a string
gnu_file_wann = os.path.join(base_dir, '..', 'data', 'wann_band_files', 'relCsPBBr3_band_wann.gnu')


#Title
title = 'CsPbBr3_SOC_wann'

# Define fermi energy and the range for valence and conduction band to find the bandgap
efermi = 1.9271
range_for_homo = efermi + 0.3
range_for_lumo = efermi + 0.1

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
svg_file = os.path.join(base_dir, '..', 'plots', f"{title}.svg")

# Save the figure as SVG
plt.savefig(svg_file, format='svg', transparent=True)
plt.savefig(svg_file, format='png', transparent=True)
plt.show()
