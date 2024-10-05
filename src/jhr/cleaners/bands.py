
import numpy as np



def bandhandler(data_file, high_symmetry_points, efermi):
  #==========TO REMOVE==========
  range_for_homo = efermi - 0.1
  range_for_lumo = efermi - 0.1
  #==============================

  data = np.loadtxt(data_file)
  k, bands = _process_band_structure(data) # Get k points and bands 
  positions, labels = _get_high_symmetry_positions_and_labels(k, high_symmetry_points)
 
  homolumo, bandgap = _find_bandgap(bands, range_for_homo, range_for_lumo)


  return k, bands, positions, labels, homolumo, bandgap


def _process_band_structure(data):
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
def _get_high_symmetry_positions_and_labels(k, high_symmetry_points):
    positions = [k[index] for index in high_symmetry_points.values()]
    labels = list(high_symmetry_points.keys())
    return positions, labels




def _find_bandgap(bands, range_for_homo, range_for_lumo):
    # Flatten the bands array to easily find the HOMO and LUMO
    all_band_energies = bands.flatten()
       # Identify the HOMO and LUMO
    homo = np.max(all_band_energies[all_band_energies <= range_for_homo])
    lumo = np.min(all_band_energies[all_band_energies >= range_for_lumo])
 
    
    # Calculate the bandgap
    bandgap = lumo - homo
    print(f"Bandgap: {bandgap:.4f} eV")
    return (homo, lumo), bandgap
    

    





