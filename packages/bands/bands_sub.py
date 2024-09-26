import numpy as np
import matplotlib.pyplot as plt

def read_datfile_wannier(data_dat):
    """
    Reads the .dat file and returns k-points and energy values.
    
    Args:
        data_dat (ndarray): Numpy array containing the .dat file data.
    
    Returns:
        k_points (ndarray): Array of k-points.
        bands (ndarray): Array of energy values.
    """
    nbnd = len(np.where(np.diff(data_dat[:, 0]) < 0)[0]) + 1
    lenk = int(data_dat.shape[0] / nbnd)
    k_points = data_dat[:lenk, 0]
    bands = np.reshape(data_dat[:, 1], (-1, lenk))
    return k_points, bands

def read_gnu_file_wann(file_content):
    """
    Parses the content of the .gnu file to extract high symmetry points and plot configuration.
    
    Args:
        file_content (str): Content of the .gnu file.
    
    Returns:
        high_symmetry_points (dict): Dictionary of symmetry points and positions.
        other_settings (dict): Additional plotting settings from the .gnu file.
    """
    high_symmetry_points = {}
    other_settings = {}
    
    for line in file_content.splitlines():  # Process the file content line by line
        # Parse high symmetry points and positions (assuming a specific format)
        if "set xtics" in line:
            points = line.split("('")[1:]  # Splitting to extract points
            for point in points:
                label, pos = point.split("'")[0], float(point.split(",")[1])
                high_symmetry_points[label] = pos
        
        # Extract other settings if needed (e.g., title, x/y limits)
        # Add conditions here if necessary
    
    return high_symmetry_points, other_settings


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
    

    













