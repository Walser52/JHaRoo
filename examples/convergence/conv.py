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

#============Function Definitions===============

def runbash(output_file, command):
  try:
      with open(output_file, 'w') as out:
          result = subprocess.run(command, shell=True, check=True, stdout=out, stderr=subprocess.PIPE)
      # print(f"Calculation for ecut = {ecut} completed successfully.")
  except subprocess.CalledProcessError as e:
      # print(f"An error occurred while running the calculation for ecut = {ecut}: {e}")
      print(e.stderr.decode())
      continue
  return


def writexy(readfrom, writeto, x):
  """Read value in readfrom corresponding to x and write both x and y to writeto file"""
  y = extract_total_energy(readfrom)
  if y is not None:
      # Write the ecut and total energy to the energy file immediately
      with open(writeto, 'a') as energy_fid:
          energy_fid.write(f"{x} {y}\n")
  else:
      print(f"Value not found in the output file for {x}.")
  return


def convOver(values, calc = 'ecutwfc'):
  
#  open(energy_file, 'w').close()


  for val in values:

      
      # Modify the input file with the current ecut value
      modified_input_file = f'pwscf_{calc}-{val}.in'
      modify_input_file(input_file, modified_input_file, val)

      # Run the pw.x calculation
      output_file = output_file_template.format(ecut)
      command = f'mpirun -n 8 --mca btl vader,self,tcp pw.x < {modified_input_file} > {output_file}'
      
#      generateinput(val = ecut, input_file = input_file)
      runbash(output_file, command)
      writexy(readfrom = output_file, writeto = energy_file, x = val)

  return


#======================================================

#-----------Code------------
convOver(values = ecut_values, calc = 'ecutwfc')
# Put the optimized value in the rho input

ecutrho_values = [2,3]
convOver(values = ecutrho_values, calc = 'ecutrho')
#----Plot----
data = np.loadtxt(energy_file)
plotter(data)





#if __name__ == '__main__':
  


