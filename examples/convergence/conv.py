import numpy as np
import matplotlib.pyplot as plt
from imp import modify_input_file, extract_total_energy, initialize_energy_file, runbash, writexy, convOver, plotter, calculate_relative_errors # type: ignore


def checkconv(datafile = None, thresh = 0.001):
  """Returns value over which convergence is achieved"""

  relative_errors_wfc = calculate_relative_errors(data = energy_file_wfc)

  converged_ecutwfc = None
  for i, rel_error in enumerate(relative_errors_wfc):
      if rel_error < thresh:
          converged_ecutwfc = ecutwfc[i + 1]
          break

  if converged_ecutwfc is None:
      converged_ecutwfc = ecutwfc[-1]


  return converged_ecutwfc

#__________________________Converge ecutwfc_________________
# List of ecutwfc values to loop over
calc = {'ecutfwfc': [16,20,24,28,32]}


# Input and output file paths
input_file = 'pwscf.in'
output_file_template_wfc = 'pwscf_ecutwfc-{}.out'
energy_file_wfc = 'etot_vs_ecutwfc.dat'
command = 'mpirun -n 8 --mca btl vader,self,tcp pw.x < {} > {}'


# Run convergence for ecutwfc values
convOver(calc= calc, input_file=input_file, output_file_template=output_file_template_wfc, energy_file=energy_file_wfc, command=command)
converged_ecutwfc = checkconv(datafile = energy_file_wfc)
print(f"Converged ecutwfc: {converged_ecutwfc}")



#calc = {'ecutfwfc': [16,20,24,28,32]}
#params = {
#'input_file': 'pwscf.in', 
#  'output_file_template' : 'pwscf_ecutwfc-{}.out', 
#  'energy_file' : 'etot_vs_ecutwfc.dat',
#  'command' : 'mpirun -n 8 --mca btl vader,self,tcp pw.x < {} > {}'}
#convOver(calc= calc, params = params)
#

# Append converged ecutwfc to the energy file
with open(energy_file_wfc, 'a') as f:
    f.write(f"Converged ecutwfc: {converged_ecutwfc}\n")





#________________________Converge ecutrho_____________________

# Run convergence for ecutrho values
ecutrho_values = [factor * converged_ecutwfc for factor in [4, 6, 8, 10, 12]]
calc = {'ecutrho': ecutrho_values}
output_file_template_rho = 'pwscf_ecutrho-{}.out'
energy_file_rho = 'etot_vs_ecutrho.dat'
convOver(calc= calc, input_file=input_file, output_file_template=output_file_template_rho, energy_file=energy_file_rho, command=command)

# Load data and calculate relative errors for ecutrho
converged_ecutrho = checkconv(datafile = energy_file_rho)
print(f"Converged ecutwfc: {converged_ecutrho}")

# Append converged ecutrho to the energy file
with open(energy_file_rho, 'a') as f:
    f.write(f"Converged ecutrho: {converged_ecutrho}\n")




#__________________________Plot__________________________
plotter(data_wfc, 'Ecutwfc (Ry)', 'Total Energy (Ry)', 'ecutwfc.pdf')
plotter(data_rho, 'Ecutrho (Ry)', 'Total Energy (Ry)', 'ecutrho.pdf')
