import numpy as np
import matplotlib.pyplot as plt
import re

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

# def read_gnu_file_wann(gnu_content):
#     """
#     Reads the .gnu file content and extracts high symmetry points.

#     Args:
#         gnu_content (str): Content of the .gnu file as a string.

#     Returns:
#         high_symmetry_points (dict): Dictionary of symmetry points and their positions.
#         other_settings (dict): Other settings if needed.
#     """
#     high_symmetry_points = {}
#     lines = gnu_content.splitlines()

#     for line in lines:
#         if line.startswith("set xtics"):
#             # Extract the part after 'set xtics'
#             tics_part = line.split(" ", 2)[2]
#             # Remove the outer parentheses
#             tics_part = tics_part.strip()[1:-1]  # Removing the parentheses
#             # Split the string into individual ticks
#             ticks = tics_part.split(',')

#             for tick in ticks:
#                 # Split the label and position while accounting for potential whitespace
#                 parts = tick.split()
#                 if len(parts) >= 2:
#                     # Reconstruct the label from all but the last part
#                     label = ' '.join(parts[:-1]).strip().strip('"')  # Clean the label
#                     position = float(parts[-1].strip())  # Convert the last part to float

#                     # Store positions in a list to handle duplicates
#                     if label in high_symmetry_points:
#                         high_symmetry_points[label].append(position)
#                     else:
#                         high_symmetry_points[label] = [position]

#     return high_symmetry_points, {}


def read_gnu_file_wann(gnu_content):
    """
    Reads the .gnu file content and extracts high symmetry points.

    Args:
        gnu_content (str): Content of the .gnu file as a string.

    Returns:
        high_symmetry_points (dict): Dictionary of symmetry points and their positions.
        other_settings (dict): Placeholder for other settings if needed.
    """
    high_symmetry_points = {}
    lines = gnu_content.splitlines()
    
    for line in lines:
        if line.startswith("set xtics"):
            # Extract the part after 'set xtics'
            tics_part = line.split(" ", 2)[2]
            # Remove the outer parentheses
            tics_part = tics_part.strip()[1:-1]  # Removing the parentheses
            # Split the string into individual ticks
            ticks = tics_part.split(',')
            for tick in ticks:
                # Split the label and position while accounting for potential whitespace
                parts = tick.split()
                if len(parts) >= 2:
                    label = ' '.join(parts[:-1]).strip().strip('"')  # Clean the label
                    position_str = parts[-1].strip()  # Keep it as string for debugging

                    try:
                        position = float(position_str)  # Convert to float
                    except ValueError as e:
                        print(f"Could not convert position '{position_str}' for label '{label}': {e}")
                        continue

                    # Store positions in a list to handle duplicates
                    if label in high_symmetry_points:
                        high_symmetry_points[label].append(position)
                    else:
                        high_symmetry_points[label] = [position]

    return high_symmetry_points, {}




def plot_energy_bands(k_points, bands, high_symmetry_points, efermi, title=None, bandgap_info=None):
    """
    Plots the energy bands using k-points and energy values.
    
    Args:
        k_points (ndarray): Array of k-points.
        bands (ndarray): Array of energy values.
        high_symmetry_points (dict): Dictionary of symmetry points and positions.
        title (str, optional): Title of the plot.
    """
    import matplotlib.pyplot as plt

    


    # Plot each band
    for band in range(len(bands)):
        plt.plot(k_points, bands[band, :] - efermi)
        

    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel("High Symmetry Points")
    plt.ylabel("Energy (eV)")
    
    if title:
        plt.title(title)

    # Bandgap information
    if bandgap_info:
        homo, lumo = bandgap_info
        plt.axhline(y=homo - efermi, color='g', linestyle='-')
        plt.axhline(y=lumo - efermi, color='g', linestyle='-')

    # Formatting the plot
    plt.axhline(y=0, color='r', linestyle='--', label='Fermi Level')
    plt.xlabel('K-points')
    plt.ylabel('Energy (eV)')
    if title:
        plt.title(title)
    plt.legend()



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
    

    













