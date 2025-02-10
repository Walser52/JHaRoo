# Run convergence over several parameters. 

import jhr


from jhr.codes.espresso.converger import QEConverger
from jhr.codes.espresso.io import QEio, QEModifier
from jhr.io.base import Basher


def gen_prefix(template):
  if 'prefix' not in template.keys():
#   generate prefix from ase_atoms
    pass

  return prefix

#=======================INPUTS=====================

mat_file = 'sample-scf.json'
#prefix = 'CsPbI3'

def converge(template, parameters, valuesets, code, tolerance, file_out, check_convergence, label = None):
  """
  Perform convergences over a parameter. The method:
    - Saves files
    - Runs convergence on the saved files. 

  Args:
    template: Input file template. 
    parameters: QE parameters over which to converge
    valuesets:  Values which the parameter takes
    code: Computation code which to use. 
    tolerance: tolerance which to take
    label: Label which to use for file. Joins parameters if none given.
    check_convergence: Boolean for whether to check convergence. 
    file_out
  Returns:
    conv_val: Convergad value
  """

  if label is None: 
    label = '_'.join(parameters)
  
  conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)                 #Create converger object
  saved_files = conv.prepare_variants(template, parameters, valuesets, code, label = label)               #Prepare input files for convergences
  conv_val = conv.run_conv_one(files = saved_files, parameters = parameters, code = code, 
             tolerance = tolerance, file_out = file_out, check_convergence = check_convergence)     #Run convergence and find converged value
  return conv_val                                                                           


conv_dict1 = dict(label = 'ecutwfc',         #label to use for convergence input files
                parameters = ['ecutwfc'],   #parameters on which to converge
                file_out = 'ecutwfc_conv',
                valuesets=[5,6,8],          #convergence values
                tolerance = 0.001)

conv_dict2 = dict(label = 'degauss',          #label to use for convergence input files
                  parameters = ['degauss'],   #parameters on which to converge
                  file_out = 'degauss_conv',
                  valuesets=[0.1,0.2,0.3],          #convergence values
                  tolerance = 0.001)

conv_dict3 = dict(label = 'kpts',          #label to use for convergence input files
                  parameters = ['kpts'],   #parameters on which to converge
                  file_out = 'kpts_conv',
                  valuesets=[[1,1,1], [2,2,2]],          #convergence values
                  tolerance = 0.001)
#

#=================================================

template = QEio.from_flat_JSON(mat_file)


conv_val = converge(template, code = 'pw.x', check_convergence= True, **conv_dict1)  #Convergence 1: ecutwfc
template[conv_dict1['parameters'][0]] = conv_val                                      #update template with converged value
conv_val = converge(template, code = 'pw.x', check_convergence= True, **conv_dict2)  #Convergence 2: degauss
template[conv_dict2['parameters'][0]] = conv_val                                      #update template with converged value
# conv_val = converge(template, code = 'pw.x', check_convergence= False, **conv_dict3)                            #Convergence 3: kpoints

exit()

#====================NSCF-BANDS==============
#Run nscf

def nscf_io(template, file_in, ase_hacks = True, verbose = True, atomic_positions = 'crystal_sg'):
  """
  Prepare QE io file for nscf
  """
  #Extract ase_dict from template and modify template. 
  ase_dict, template = QEConverger().extract_ase_dict(template)
  write_espresso_in(file_in, input_data = template, **ase_dict)

  if ase_hacks:
    QEModifier.modify_file(QEModifier.remove_ibrav, file_in, verbose = verbose)
    QEModifier.modify_file(QEModifier.remove_cell_parameters, file_in,verbose = verbose)
    QEModifier.modify_file(QEModifier.modify_atomic_positions, file_in, atomic_positions = atomic_positions, verbose = verbose)

  return

from ase.io.espresso import read_espresso_in, write_espresso_in
mat_file = 'sample-nscfbands.json'
template = QEio.from_flat_JSON(mat_file)
prefix = 'CsPbI3'
code, file_in, file_out = 'pw.x', 'nscfinp.in', 'nscfout.out'

ase_hacks = True
verbose = True
atomic_positions = 'crystal_sg'

nscf_io(template, file_in, ase_hacks = ase_hacks, verbose = verbose, atomic_positions = atomic_positions)
Basher.runcommand(f'{code} < {file_in} > {file_out}')




#==============Bands.x=======================
from ase.io.espresso import write_fortran_namelist

prefix = 'CsPbI3'
bands_template = {'bands': dict(outdir  = '../tmp/', prefix  = f'{prefix}', filband = f'{prefix}.bands')}
file_in = 'bands.in'
file_out = 'bands.out'
code = 'bands.x'
additional_cards = []

with open(f'{file_in}', 'w') as fd:
  write_fortran_namelist(fd, bands_template, additional_cards = additional_cards)
Basher.runcommand(f'{code} < {file_in} > {file_out}')


#====================NSCF (DOS)==============
#Run nscf
from ase.io.espresso import read_espresso_in, write_espresso_in
mat_file = 'sample-nscfdos.json'
prefix = 'CsPbI3'
template = QEio.from_flat_JSON(mat_file)
file_in = 'nscfinp.in'

ase_dict, template = QEConverger().extract_ase_dict(template)
write_espresso_in(file_in, input_data = template, **ase_dict)

verbose = True
atomic_positions = 'crystal_sg'

QEModifier.modify_file(QEModifier.remove_ibrav, file_in, verbose = verbose)
QEModifier.modify_file(QEModifier.remove_cell_parameters, file_in,verbose = verbose)
QEModifier.modify_file(QEModifier.modify_atomic_positions, file_in, atomic_positions = atomic_positions, verbose = verbose)
Basher.runcommand('pw.x < nscfinp.in > nscfout.out')

#==============DOS/PDOS=======================
from ase.io.espresso import write_fortran_namelist

prefix = 'CsPbI3'
bands_template = {'bands': dict(outdir  = '../tmp/', prefix  = f'{prefix}', filband = f'{prefix}.bands')}
file_in = 'bands.in'
file_out = 'bands.out'
code = 'bands.x'
additional_cards = []

with open(f'{file_in}', 'w') as fd:
  write_fortran_namelist(fd, bands_template, additional_cards = additional_cards)
Basher.runcommand(f'{code} < {file_in} > {file_out}')




# Restart option?
# Converge on kpts

# ====
# Verify for ph.x
