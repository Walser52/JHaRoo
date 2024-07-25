import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os 

def runone(value):
  #change the $value in the pwtk script and execute the script.
  
  return


def runconvergence(scriptfolder = '.'):

  if scriptfolder != '.':
    os.chdir(scriptfolder)
    print(os.getcwd())

  # Define the PWTK script and command
  pwtk_script = 'conv_ecut.pwtk'
  command = ['pwtk',pwtk_script]

  # Step 1: Run the PWTK script
  try:
      result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      print("PWTK script completed successfully.")
  except subprocess.CalledProcessError as e:
      print(f"An error occurred while running the PWTK script: {e}")
      print(e.stderr.decode())
      exit(1)
  return

def plotter(dat_file):

  # Read the data from the .dat file
  data = np.loadtxt(dat_file)

  # Separate the data into two columns
  ecut_values = data[:, 0]
  second_column = data[:, 1]

  # Step 3: Create the plot
  plt.figure(figsize=(10, 6))
  plt.plot(ecut_values, second_column, marker='o', linestyle='-', color='b', label='Data')

  # Add title and labels
  plt.title('Plot of output.dat')
  plt.xlabel('Ecut Values')
  plt.ylabel('Second Column Values')
  plt.legend()

  # Show grid
  plt.grid(True)

  # Save the plot as a PDF
  plt.savefig('output_plot.pdf')

  print("Plot saved as output_plot.pdf")

  return


def hasconverged():
#  Test if convergence has been achieved.
  return
#
if __name__=='__main__':
  runconvergence('data')

  dat_file2 = 'etot_vs_ecutwfc.dat'
  plotter(dat_file = dat_file2)

  hasconverge()



