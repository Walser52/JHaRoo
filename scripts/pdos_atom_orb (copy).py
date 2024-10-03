import matplotlib.pyplot as plt
import numpy as np
import os
import glob

title = 'CsPbBr3'
# Define the fermi energy
efermi = 1.9671

# Define folder path to load data from
pdos_folder = r'E:\CsPbBr3\5_Nscf'

# Define the function to read multiple PDOS files
def r_dos(name):
    data = np.loadtxt(name, usecols=(0, 1))
    energy, dos = data.T
    return energy, dos

# Find all .pdos files to load
all_pdos = glob.glob(os.path.join(pdos_folder, '*.pdos*'))

if not all_pdos:
    print("No .pdos files found.")
else:
    print(f"Found {len(all_pdos)} .pdos files.")

# Initialize a dictionary to store energy and DOS for each atom and orbital type
pdos_data = {}

# Load PDOS files and store DOS for each atom and orbital
for file in all_pdos:
    energy, dos = r_dos(file)
    if energy is None or dos is None:
        continue
    
    # Check if the file name contains both 'atm#' and 'wfc#'
    try:
        # Extract atom and orbital information using regex-like string splitting
        atom_info = file.split('_atm#')[1].split('_wfc#')[0]
        atom_type = atom_info.split('(')[1].split(')')[0]  # Extract atom (e.g., Cs, Pb)
        
        orbital_info = file.split('_wfc#')[1]
        orbital_type = orbital_info.split('(')[1].split(')')[0]  # Extract orbital type (e.g., s, p, d)
    except IndexError:
        print(f"Skipping file {file} due to parsing issues.")
        continue

    # Create a key for each atom and orbital type (e.g., 'Cs-s', 'Pb-p')
    key = f"{atom_type}-{orbital_type}"
    
    if key not in pdos_data:
        pdos_data[key] = {'energy': energy, 'dos': np.zeros_like(dos)}

    # Accumulate DOS for the corresponding atom and orbital type
    pdos_data[key]['dos'] += dos

# Read the total PDOS
energy_tot, dos_tot = r_dos(os.path.join(pdos_folder, 'aiida.pdos_tot'))

# Create figure
plt.figure()

# Plot total DOS
plt.plot(dos_tot, energy_tot - efermi, c='blue', label='Total DOS')

# Plot PDOS for each atom and orbital type
for key, data in pdos_data.items():
    plt.plot(data['dos'], data['energy'] - efermi, label=f'{key} orbitals')

# Add labels and save the figure
plt.title(title)
plt.xlabel('DOS (states/eV)')
plt.ylabel('Energy (eV)')
plt.axhline(y=0, c='gray', linestyle='--', linewidth=1)

plt.xlim(0, 45)
plt.ylim(-4, 10)
plt.legend()

# Save the plots
base_dir = os.path.dirname(os.path.abspath(__file__))
svg_file = os.path.join(base_dir, '..', 'plots', 'DFT_PDOS_atom_orb', f"{title}")
plt.savefig(svg_file + '.svg', format='svg', transparent=True)
plt.savefig(svg_file + '.png', format='png', transparent=True, dpi=350)
plt.show()


if __name__ == '__main__':


  
