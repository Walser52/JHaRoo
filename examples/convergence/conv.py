import subprocess
import numpy as np
import matplotlib.pyplot as plt
from imp import modify_input_file, extract_total_energy, plotter

# List of ecut values to loop over
ecut_values = [16, 20]  # Example values, replace with actual values

# Input and output file paths
input_file = 'pwscf.in'
output_file_template = 'pwscf_ecutwfc-{}.out'
energy_file = 'etot_vs_ecutwfc.dat'

# Ensure the energy file is empty or start fresh
open(energy_file, 'w').close()

for ecut in ecut_values:
    # Modify the input file with the current ecut value
    modified_input_file = f'pwscf_ecutwfc-{ecut}.in'
    modify_input_file(input_file, modified_input_file, ecut)

    # Run the pw.x calculation
    output_file = output_file_template.format(ecut)
    command = f'mpirun -n 8 --mca btl vader,self,tcp pw.x < {modified_input_file} > {output_file}'
    
    try:
        with open(output_file, 'w') as out:
            result = subprocess.run(command, shell=True, check=True, stdout=out, stderr=subprocess.PIPE)
        print(f"Calculation for ecut = {ecut} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the calculation for ecut = {ecut}: {e}")
        print(e.stderr.decode())
        continue

    # Extract the total energy from the output file
    total_energy = extract_total_energy(output_file)
    if total_energy is not None:
        # Write the ecut and total energy to the energy file immediately
        with open(energy_file, 'a') as energy_fid:
            energy_fid.write(f"{ecut} {total_energy}\n")
    else:
        print(f"Total energy not found in the output file for ecut = {ecut}.")

# After all calculations, load the data and plot
data = np.loadtxt(energy_file)
plotter(data)
