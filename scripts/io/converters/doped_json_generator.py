#This code iterates over a 'doped' styled folder. 
import pandas as pd
from jhr.codes.doped import Doped
from ase.io import read
import os 
import json 

class Study():
  pass

class DopedStudy(Study):
  def __init__():
    return
  def from_dataframe(self, mats):
    self.mats = mats

  

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

atoms = read(df['POSCAR'][0])
df['atoms'] = df['POSCAR'].apply(lambda x: read(x) if x is not None else None)



df["json_modified"] = df.apply(
    lambda row: {**row["json_template"], 
                  "pbc": row["pbc"], 
                  "kpts": row["kpts"], 
                  'prefix': row['prefix'], 
                  'crystal_coordinates': row['crystal_coordinates']
                }, axis=1)
#print(df.json_modified.iloc[0])


# Save json_modified files
for (folder, subfolder), json_data in df["json_modified"].iteritems():
    # Construct the directory path
    dir_path = os.path.join(root_directory, folder, subfolder)
    
    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)
    
    # Define the file path
    file_path = os.path.join(dir_path, "template.json")
    print(file_path)
    # Save the JSON data to the file
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)


print("Files saved successfully.")

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
