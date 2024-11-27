# Reads a cif
# Creates a supercell
# Removes atoms according to requirement

from ase.io import read, write
from ase.build import make_supercell

#_____________Create supercell______________
# Load the CIF file into an ASE Atoms object
structure = read("../../data/cif/CsPbI3.cif")  # Replace 'structure.cif' with your file name
transformation_matrix = [
    [1, 0, 0],  # Scale in the x-direction
    [0, 1, 0],  # Scale in the y-direction
    [0, 0, 1]   # Scale in the z-direction
]
supercell = make_supercell(structure, transformation_matrix)
write("supercell.cif", supercell)


#-------------------------------

&INPUTPH
dict(
outdir = '../tmp/'
prefix = 'gr'
tr2_ph = 1d-14
ldisp  = .true.
nq1    = None
nq2    = None
nq3    = 1
fildyn = 'gr.dyn'
)

# 1. Create phonon input file (template) using ase:
input_ph = {
  'tr2_ph': 1.0e-12,
  'prefix': 'pwscf',
  'verbosity': 'high',
  'ldisp': True,
  'qplot': False,
  'alpha_mix(1)': 0.1,
  'nq1': None,
  'nq2': None,
  'nq3': None,
}

input_ph = dict(
            outdir = '../tmp/'
            prefix = 'gr'
            tr2_ph = 1d-14
            ldisp  = .true.
            nq1    = None
            nq2    = None
            nq3    = 1
            fildyn = 'gr.dyn'
            )

qpts = [(0.0, 0.0, 0.0), (0.5, 0.5, 0.5), (0.5, 0.5, 0.0), (0.0, 0.0, 0.5)]

#___________Q2R file________
from ase.io.espresso import write_fortran_namelist
q2r_data = {
  'input': {'fildyn': 'prefix.dyn', 'zasr': 'crystal', 'flfrc':'prefix.fc'}
} 

q2r_in = 'q2r.in'
q2r_out = 'q2r.out'
with open(q2r_in, 'w') as fd:
  write_fortran_namelist(fd, q2r_data)

#__________MATDYN file___________

from ase.io.espresso import write_fortran_namelist

input_data = {
  'input': {'asr':'crystal', 'flfrc':'prefix.fc', 'flfrq': 'prefix.freq'}
} 

matdyn_in = 'matdyn.in'
matdyn_out = 'matdyn.out'
with open(matdyn_in, 'w') as fd:
  write_fortran_namelist(fd, input_data)

#---------------------------------


from jhr.convergers.base import QEConverger


def checkerror(result):
  if result.returncode == 0: print("Command executed successfully.")
  else: print(f"Command failed with return code {result.returncode}")
  return 

def runcommand(command, shell = True, text = True):
  print(f"Running: {command}")
  result = subprocess.run(command, shell=True, text=True)
  checkerror(result)
  return  

#======Create convergence files
label = 'NQ'

c = QEConverger()
all_files = c.conv_on(template=input_ph, parameters=['nq1', 'nq2'], valuesets=[(2, 2), (3, 3), (4, 4)])
c.savefiles(prefix = f'aiida{label}', files_data = all_files, ext = 'in', code = 'ph') 



# 2. Perform convergence on a parameter (e.g. k-point grid).

import subprocess
from pathlib import Path
files = ['aiidaNQ_0.in', 'aiidaNQ_0.in', 'aiidaNQ_0.in']

convergence_param = []
for f_in in files:

  f_out = Path(f_in).stem
  command = f"ph.x < {f_in} > {f_out}.out"
  runcommand(command)

  command = f"q2r.x < {q2r_in} > {q2r_out}"
  runcommand(command)

  command = f"matdyn.x < {matdyn_in} > {matdyn_out}"
  runcommand(command)
 
  print("===Checking Convergence====")

  # param = convergence value read from file
#  converged_param.append(param)
  #check criteria 

  print("=========")

  # Find the converged parameter
  # Check if criteria met.

  # Take all files with label in name



# 3. Check if converged?





#____________Symmetry reduction_________ (Delete unnecessary atoms)



#___________Create espresso input/Relaxation/Convergence_______
    #_________Create input______
    #_________Verify threshold met or not_____







## Create QE file
## Relaxation
## Convergence tests



