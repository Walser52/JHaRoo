import numpy as np
import matplotlib.pyplot as plt
# k = np.unique(data[:,0])
# bands = np.reshape(data[:,1], [-1, len(k)])
def process_band_structure(data):
    nbnd = len(np.where(np.diff(data[:, 0]) < 0)[0]) + 1
    lenk = int(data.shape[0] / nbnd)
    k = data[:lenk, 0]
    bands = np.reshape(data[:, 1], (-1, lenk))
    return k, bands

# Get the positions
def get_high_symmetry_positions_and_labels(k, high_symmetry_points):
    positions = [k[index] for index in high_symmetry_points.values()]
    labels = list(high_symmetry_points.keys())
    return positions, labels

def plot_bandstructure(k, bands, positions, labels, title=None):
    
    for band in range (len(bands)):
        plt.plot(k,bands[band, :])

    plt.xlabel("High Symmetry Points")
    plt.ylabel("Energy (eV)")
    plt.xticks(positions, labels)
    if title:
        plt.title(title)
    plt.grid(True)
    
def plot_settings(**kwargs):
    for key, value in kwargs.items():
        plt.rcParams[key] = value
    

    













