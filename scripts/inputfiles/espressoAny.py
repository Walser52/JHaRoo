from ase.io.espresso import Namelist
from ase.io.espresso import write_fortran_namelist

# input_data for pp.x, built automatically
input_data = {'outdir': '/path/to/output', 'prefix': 'prefix', 'verbosity': 'high'}

input_data = Namelist(input_data)
input_data.to_nested(binary='pp')

write_fortran_namelist('input_pp.in', input_data)

# Alternatively, the input_data can be written manually
# without the need to specify a binary

input_data = {
  'environ': {
    'environ_type': 'water',
  ...} # In this case, the ``input_data`` is a nested dictionary
  # since ASE cannot guess the input sections for exotic executables

additional_cards = [
      'EXTERNAL_CHARGES (bohr)',
      '-0.5 0. 0. 25.697 1.0 2 3',
      '-0.5 0. 0. 20.697 1.0 2 3'
] # This will be added at the end of the file

write_fortran_namelist('environ.in', input_data)
