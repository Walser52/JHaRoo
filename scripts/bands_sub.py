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










