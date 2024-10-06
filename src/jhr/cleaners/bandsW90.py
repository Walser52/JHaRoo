import numpy as np


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

def bandHandlerW90(dat_file_wann, gnu_file_wann, efermi):
    #==========TO REMOVE==========
    range_for_homo = efermi - 0.1
    range_for_lumo = efermi - 0.1
    #==============================
    data_dat = np.loadtxt(dat_file_wann)
    # Use the content directly (no need for a path)
    k_points, bands = read_datfile_wannier(data_dat)

    with open(gnu_file_wann, 'r') as file:
        gnu_content = file.read()  # Read the content of the .gnu file
        high_symmetry_points, other_settings = read_gnu_file_wann(gnu_content)  # Pass the content, not the file path

        positions = []
        labels = []

    # Iterate through high symmetry points
    for label, pos_list in high_symmetry_points.items():
    # Append all positions for the current label
        for position in pos_list:
            positions.append(position)
            labels.append(label)  # Keep the label, even if it repeats
    # positions = [pos for pos_list in high_symmetry_points.values() for pos in pos_list]
    # labels = [label for label, pos_list in high_symmetry_points.items() for _ in pos_list]

    (homo, lumo), bandgap = find_bandgap(bands, range_for_homo, range_for_lumo)
    if bandgap is not None:
        print(f"Bandgap: {bandgap:.4f} eV")
        bandgap_info = (homo, lumo)
    else:
        print("No bands found near eFermi to calculate bandgap.")
        bandgap_info = None

    return k_points, bands, high_symmetry_points, other_settings, positions, labels, (homo, lumo), bandgap


def find_bandgap(bands, range_for_homo, range_for_lumo):
    # Flatten the bands array to easily find the HOMO and LUMO
    all_band_energies = bands.flatten()
       # Identify the HOMO and LUMO
    homo = np.max(all_band_energies[all_band_energies <= range_for_homo])
    lumo = np.min(all_band_energies[all_band_energies >= range_for_lumo])
 
    
    # Calculate the bandgap
    bandgap = lumo - homo
    return (homo, lumo), bandgap

