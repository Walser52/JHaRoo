from module1 import process_band_structure, get_high_symmetry_positions_and_labels, plot_bandstructure
import numpy as np
import matplotlib.pyplot as plt
filename = 'aiida.bands.gnu'
data = np.loadtxt(filename)

# Get k points and bands from imported function
k, bands = process_band_structure(data)

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

# Plot the bandstructure using imported function
plot_bandstructure(k, bands, positions, labels, title='CsPbI3 Bands')
