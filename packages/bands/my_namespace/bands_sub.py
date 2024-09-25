import numpy as np
import matplotlib.pyplot as plt

def process_band_structure(data):
    """
    Functionailty

    Args: 
        data: type? list? dictionary?
    Returns: 

    """

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

def plot_bandstructure(k, bands, positions, labels, efermi, title=None, bandgap_info=None):
    
    for band in range (len(bands)):
        plt.plot(k,bands[band, :] - efermi)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel("High Symmetry Points")
    plt.ylabel("Energy (eV)")
    plt.xlim(positions[0], positions[-1])
    plt.xticks(positions, labels)
    if title:
        plt.title(title)
    #plt.grid(True)
    if bandgap_info:
        homo, lumo = bandgap_info
        plt.axhline(y=homo - efermi, color='g', linestyle='-')
        plt.axhline(y=lumo - efermi, color='g', linestyle='-')
        plt.annotate('', xy=(positions[-1], lumo - efermi), xytext=(positions[-1], homo - efermi),
                     arrowprops=dict(arrowstyle='<->', color='blue'))
        plt.text(positions[-1], (lumo + homo) / 2 - efermi, f'Bandgap: {lumo - homo:.4f} eV', 
                 ha='left', va='center', color='blue')
    
def plot_settings(**kwargs):
    for key, value in kwargs.items():
        if key in plt.rcParams:  # Only set rcParams for valid keys
            plt.rcParams[key] = value

def find_bandgap(bands, range_for_homo, range_for_lumo):
    # Flatten the bands array to easily find the HOMO and LUMO
    all_band_energies = bands.flatten()
       # Identify the HOMO and LUMO
    homo = np.max(all_band_energies[all_band_energies <= range_for_homo])
    lumo = np.min(all_band_energies[all_band_energies >= range_for_lumo])
 
    
    # Calculate the bandgap
    bandgap = lumo - homo
    return homo, lumo, bandgap
    

    













