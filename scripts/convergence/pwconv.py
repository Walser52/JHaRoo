# Reads a cif
# Creates a supercell
# Removes atoms according to requirement
from ase import Atoms
from ase.io import read, write
from ase.build import make_supercell
from ase.io.espresso import ffloat
from jhr.convergers.base import QEConverger
import json 
from jhr.io.modifiers import QEModifier
from jhr.io.base import from_JSON
import matplotlib.pyplot as plt



mat_file = 'sample2.json'
prefix = 'CsPbI3'



#Convergence parameters 1
label = 'ECUT'
parameters = ['ecutwfc']
valuesets=[5,6,8]
code = 'pw'
ext = 'in'
name = f'{prefix}{label}'



#Perform convergence. 

atoms, ase_dict, template = from_JSON(mat_file)


all_conv_parameters = [['ecutwfc'], ['ecutrho'], ['k-points']]
all_conv_valuesets = [[1,2,3], [4,5,6], [7,8,9]]


#======Create convergence files
conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)
conv.conv_express(prefix = name, ext = ext, code = code, ase_dict = ase_dict, ase_hacks = True, atomic_positions = 'crystal_sg')



#======Perform convergence on a parameter (e.g. k-point grid).
from pathlib import Path
files = list(Path('.').glob(f'{name}*{ext}')) # Find files starting with 'name' and ending with '.in'
files = sorted(files, key=lambda f: int(f.stem.split(f'{name}_')[-1]))


from jhr.io.base import Basher
convergence_param = []
for f_in, vals in zip(files, conv.valuesets):

  stem, f_out = Path(f_in).stem, (Path(f_in).stem + '.out')

  command = f"pw.x < {f_in} > {f_out}"
  Basher.runcommand(command)
  convergence_param.append(conv.read_total_energy(f'{f_out}'))





  plt.plot(convergence_param, marker = 's')
  plt.savefig('energy_conv.pdf')
  
  #check convergence criteria
  converged   = conv.check_convergence(convergence_param)
  if converged: conv.converged_val = vals


