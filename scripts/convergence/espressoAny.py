from ase.io.espresso import write_fortran_namelist

# input_data for pp.x, built automatically
#input_data = {'outdir': '/path/to/output', 'prefix': 'prefix', 'verbosity': 'high'}

input_data = {
  'input': {'fildyn': 'prefix.dyn', 'zasr': 'crystal', 'flfrc':'prefix.fc'}
} 
 

additional_cards = [
      'EXTERNAL_CHARGES (bohr)',
      '-0.5 0. 0. 25.697 1.0 2 3',
      '-0.5 0. 0. 20.697 1.0 2 3'
] # This will be added at the end of the file

with open('environ.in', 'w') as fd:
  write_fortran_namelist(fd, input_data, additional_cards = additional_cards)
