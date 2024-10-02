import matplotlib.pyplot as plt
import numpy as np
import os
import glob

title = 'CsPbI3'
# Define the fermi energy
efermi = 3.6711

# Define folder path to load data from
pdos_folder = r'D:\Research\DFT_main\DFt\Data\CsPbI3\7_PDOS'

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
# Initialize dictionaries to store energy and DOS for each orbital
energy_dict = {'s': None, 'p': None, 'd': None}
dos_dict = {'s': None, 'p': None, 'd': None}

# Load PDOS files and accumulate DOS for each orbital
for file in all_pdos:
    energy, dos = r_dos(file)
    if energy is None or dos is None:
        continue

    if '_wfc#1(s)' in file:
        orbital = 's'
    elif '_wfc#2(p)' in file:
        orbital = 'p'
    elif '_wfc#3(d)' in file:
        orbital = 'd'
    else:
        continue

    # Initialize or accumulate DOS for each orbital
    if energy_dict[orbital] is None:
        energy_dict[orbital] = energy
        dos_dict[orbital] = np.zeros_like(dos)

    # Check if the energy array matches the existing one
    if len(energy) == len(energy_dict[orbital]):
        dos_dict[orbital] += dos
    else:
        # Handle the case where energy arrays don't match (interpolation might be needed)
        print(f"Energy arrays for {orbital}-orbital don't match. Skipping accumulation.")
        continue

# Read the total PDOS
energy_tot, dos_tot = r_dos(os.path.join(pdos_folder, 'aiida.pdos_tot'))

# Create figure
plt.figure()

# Plot total DOS
plt.plot(dos_tot, energy_tot - efermi,  c='blue', label='Total DOS')

# Plot PDOS for each orbital
for orbital in ['s', 'p', 'd']:
    if energy_dict[orbital] is not None and dos_dict[orbital] is not None:
        plt.plot(dos_dict[orbital], energy_dict[orbital] - efermi,  label=f'{orbital}-orbital')

# Add labels and save the figure
plt.title(title)
plt.xlabel('DOS (states/eV)')
plt.ylabel('Energy (eV)')
plt.axhline(y=efermi-efermi, c='gray', linestyle='--', linewidth=1)

plt.xlim(0, 25) 
plt.ylim(-6, 10)  
plt.legend()

base_dir = os.path.dirname(os.path.abspath(__file__))
svg_file = os.path.join(base_dir, '..', 'plots', 'DFT_PDOS', f"{title}")
plt.savefig(svg_file+'.svg', format='svg', transparent=True)
plt.savefig(svg_file+'.png', format='png', transparent=True)
plt.show()
plt.show()
