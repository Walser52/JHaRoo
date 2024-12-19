
import pandas as pd
from jhr.codes.doped import Doped

# Specify doped directory
root_directory = '/home/fes33/Software/QE/Data/doped'
df = Doped().collect_file_paths(root_directory)

json_template = {"calculation": "scf", 
                  "pseudo_dir": "../pseudo/", 
                  "outdir": "../tmp/", 
#                  "prefix": "gr", 
#                  "nat": 2, "ntyp": 1, 
                  "occupations": "smearing", 
                  "smearing": "mv", 
                  "degauss": 0.02, 
                  "ecutwfc": 40, 
                  "mixing_beta": 0.7, 
                  "conv_thr": 1e-06, 
#                  "atoms": "CC", 
#                  "kpts": [4, 4, 1], 
#                  "pbc": [1, 1, 1], 
#                  "crystal_coordinates": False
                }
 
df['prefix']  = [(ind[0]+ind[1]) for ind in df.index]
df['kpts']    = [[2,2,2]]*len(df)
df['pbc']     = [[1,1,1]]*len(df)
df['crystal_coordinates']     = [True]*len(df)
df['json_template'] = [json_template] * len(df)

print(df)
# Display the DataFrame
#ind = 'Te_i_Td_Te2.83_+2'
#ind2 = 'Bond_Distortion_0.0%'
# df.loc[(ind, ind2)]
#
#matdict = {'cell':      atoms.get_cell(), 
#           'positions': atoms.get_positions(), 
#           'atoms':     ''.join(atoms.get_chemical_symbols()),
#           'pbc'  :     pbc,
#          'crystal_coordinates': crystal_coordinates
#}

#
#for i, row in df.iterrows():
#  print(i)
