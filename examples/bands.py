import numpy as np
import re
import matplotlib.pyplot as plt
filename = 'aiida.bands.gnu'
data = np.loadtxt(filename)
# k = np.unique(data[:,0])
# bands = np.reshape(data[:,1], [-1, len(k)])
nbnd = len(np.where(np.diff(data[:, 0]) < 0)[0]) + 1
lenk = int(data.shape[0] / nbnd)
k = data[:lenk, 0]
bands = np.reshape(data[:, 1], (-1, lenk))
# High symmetry points dictionary
high_symmetry_points = {
    'gG1': 0,
    'X1': 30,
    'M1': 60,
    'gG2': 90,
    'R1': 120,
    'X2|M2': 150,
    'R2': 180
}

# Get the positions
def get_high_symmetry_positions_and_labels(k, points):
    positions = [k[index] for index in points.values()]
    labels = list(points.keys())
    return positions, labels
positions, labels = get_high_symmetry_positions_and_labels(k, high_symmetry_points)

for band in range (len(bands)):
    plt.plot(k,bands[band, :], c = 'blue')

plt.title("CsPbI3 Bands")
plt.xlabel("High Symmetry Points")
plt.ylabel("Energy (eV)")
plt.xticks(positions, labels)
plt.show()




