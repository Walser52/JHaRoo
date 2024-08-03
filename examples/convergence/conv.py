import numpy as np
import matplotlib.pyplot as plt
from imp import modify_input_file, extract_total_energy, initialize_energy_file, runbash, writexy, convOver, plotter, calculate_relative_errors # type: ignore

# List of ecutwfc values to loop over
ecutwfc = [16, 20, 24, 28, 32]

# Input and output file paths
input_file = 'pwscf.in'
output_file_template_wfc = 'pwscf_ecutwfc-{}.out'
energy_file_wfc = 'etot_vs_ecutwfc.dat'
command = 'mpirun -n 8 --mca btl vader,self,tcp pw.x < {} > {}'

# Run convergence for ecutwfc values
convOver(values=ecutwfc, calc='ecutwfc', input_file=input_file, output_file_template=output_file_template_wfc, energy_file=energy_file_wfc, command=command)

# Load data and calculate relative errors
data_wfc = np.loadtxt(energy_file_wfc)
relative_errors_wfc = calculate_relative_errors(data_wfc[:, 1])

# Determine the converged value for ecutwfc
converged_ecutwfc = None
for i, rel_error in enumerate(relative_errors_wfc):
    if rel_error < 0.001:
        converged_ecutwfc = ecutwfc[i + 1]
        break

if converged_ecutwfc is None:
    converged_ecutwfc = ecutwfc[-1]

print(f"Converged ecutwfc: {converged_ecutwfc}")

# Append converged ecutwfc to the energy file
with open(energy_file_wfc, 'a') as f:
    f.write(f"Converged ecutwfc: {converged_ecutwfc}\n")

# Run convergence for ecutrho values
ecutrho_factors = [4, 6, 8, 10, 12]
ecutrho_values = [factor * converged_ecutwfc for factor in ecutrho_factors]
output_file_template_rho = 'pwscf_ecutrho-{}.out'
energy_file_rho = 'etot_vs_ecutrho.dat'
convOver(values=ecutrho_values, calc='ecutrho', input_file=input_file, output_file_template=output_file_template_rho, energy_file=energy_file_rho, command=command)

# Load data and calculate relative errors for ecutrho
data_rho = np.loadtxt(energy_file_rho)
relative_errors_rho = calculate_relative_errors(data_rho[:, 1])

# Determine the converged value for ecutrho
converged_ecutrho = None
for i, rel_error in enumerate(relative_errors_rho):
    if rel_error < 0.001:
        converged_ecutrho = ecutrho_values[i + 1]
        break

if converged_ecutrho is None:
    converged_ecutrho = ecutrho_values[-1]

print(f"Converged ecutrho: {converged_ecutrho}")

# Append converged ecutrho to the energy file
with open(energy_file_rho, 'a') as f:
    f.write(f"Converged ecutrho: {converged_ecutrho}\n")

#----Plot----
plotter(data_wfc, 'Ecutwfc (Ry)', 'Total Energy (Ry)', 'ecutwfc.pdf')
plotter(data_rho, 'Ecutrho (Ry)', 'Total Energy (Ry)', 'ecutrho.pdf')
