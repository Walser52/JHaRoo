import numpy as np


#calculate sum of (mui)*(ni)
def chem_pot(mu_energies: dict, n: dict) -> float:
    tot_chem_pot = 0
    for k, mu in mu_energies.items():
        elem = k.replace('_mu', '')  # Extract 'Pb' from 'Pb_mu'
        tot_chem_pot += mu * n.get(elem, 0)
    return tot_chem_pot


def find_plateau(z, V_short, start_z, end_z):
    first_derivative = np.gradient(V_short, z)
    second_derivative = np.gradient(first_derivative, z)
    
    threshold_first = 0.01
    threshold_second = 0.01
    plateau_region = (z >= start_z) & (z <= end_z)
    
    flat_points = (np.abs(first_derivative) < threshold_first) & (np.abs(second_derivative) < threshold_second) & plateau_region
    
    plateau_z = z[flat_points]
    plateau_y = V_short[flat_points]
    
    if plateau_y.size > 0:
        plateau_value = plateau_y.mean()
        print(f"Plateau region detected between z = {plateau_z.min():.2f} and z = {plateau_z.max():.2f} Bohr")
        print(f"Average plateau potential: {plateau_value:.4f} eV")
    else:
        print("No significant plateau found in the selected region.")
        
    return plateau_value