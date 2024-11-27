# Reads a cif
# Creates a supercell
# Removes atoms according to requirement
from ase import Atoms
from ase.io import read, write
from ase.build import make_supercell

#_____________Create supercell______________
# Load the CIF file into an ASE Atoms object
#structure = read("../../data/cif/CsPbI3.cif")  # Replace 'structure.cif' with your file name
#transformation_matrix = [
#    [1, 0, 0],  # Scale in the x-direction
#    [0, 1, 0],  # Scale in the y-direction
#    [0, 0, 1]   # Scale in the z-direction
#]
#supercell = make_supercell(structure, transformation_matrix)
#write("supercell.cif", supercell)
#

#-------------------------------



# 1. Create input file (template) using ase:

input = dict(calculation = 'scf',
            pseudo_dir   = '../pseudo/',
            outdir       = '../tmp/',
            prefix       = 'gr',
#            ibrav        = 4,
            a            = 2.4623,
            c            = 10.0,
            nat          = 2,
            ntyp         = 1,
            occupations  = 'smearing',
            smearing     = 'mv',
            degauss      = 0.02,
            ecutwfc      = None,
            mixing_beta  = 0.7,
            conv_thr     = 1.0e-6
)

pseudopotentials = {'C': 'C.pbe-n-rrkjus_psl.0.1.UPF'}
kpts = (12,12,1)
atoms = Atoms('CC', positions=[(0.333333333,  0.666666666,  0.500000000), (0.666666666,  0.333333333,  0.500000000)])
crystal_coordinates = True

ase_dict = dict(atoms = atoms, crystal_coodrinates = crystal_coordinates, pseudopotentials = pseudopotentials, kpts = kpts)

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
label = 'ECUT'

c = QEConverger()
all_files = c.conv_on(template=input, parameters=['ecutwfc'], valuesets=[5,6,8])
c.savefiles(prefix = f'aiida{label}', files_data = all_files, ext = 'in', code = 'pw', ase_dict = ase_dict) 



# 2. Perform convergence on a parameter (e.g. k-point grid).
#
#import subprocess
#from pathlib import Path
#files = ['aiidaNQ_0.in', 'aiidaNQ_0.in', 'aiidaNQ_0.in']
#
#convergence_param = []
#for f_in in files:
#
#  f_out = Path(f_in).stem
#  command = f"ph.x < {f_in} > {f_out}.out"
#  runcommand(command)
#
#  command = f"q2r.x < {q2r_in} > {q2r_out}"
#  runcommand(command)
#
#  command = f"matdyn.x < {matdyn_in} > {matdyn_out}"
#  runcommand(command)
# 
#  print("===Checking Convergence====")
#
#  # param = convergence value read from file
#  converged_param.append(param)
#  #check criteria 
#
#  print("=========")
#
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



