import subprocess
import json
from ase import Atoms
#def modify_input_file(input_file, output_file, **kwargs):
#    """Update the input file with various parameter values."""
#    with open(input_file, 'r') as file:
#        lines = file.readlines()
#
#    with open(output_file, 'w') as file:
#        for line in lines:
#            updated_line = line
#            for param, value in kwargs.items():
#                if param in line:
#                    if isinstance(value, str):
#                        # Add quotes around string values
#                        updated_line = f"  {param} = '{value}',\n"
#                    else:
#                        # For non-string values
#                        updated_line = f"  {param} = {value},\n"
#                    break  # Break after updating the line for the specific parameter
#            file.write(updated_line)
#  return
#

class Basher():
  """Class for running commands on shell"""
  def __init__():
    return

  @classmethod
  def checkerror(cls, result):
    if result.returncode == 0: print("Command executed successfully.")
    else: print(f"Command failed with return code {result.returncode}")
    return 

  @classmethod
  def runcommand(cls, command, shell = True, text = True):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, text=True)
    cls.checkerror(result)
    return   
  

class QEio():
  def __init__():
    return 

  @classmethod
  def from_JSON(cls, file):
    """
    Create ase.Atoms object from a json file and a dictionary of settings. The dict is used to create a template which may be used to perform convergence.

    Args: json file with structure.

          {"template": 
            {"calculation": "scf", 
              "pseudo_dir": "../pseudo/", 
              "outdir": "../tmp/", 
              "prefix": "gr", 
              "a": 2.4623, "c": 10.0, 
              "nat": 2, "ntyp": 1, 
              "occupations": "smearing", 
              "smearing": "mv", 
              "degauss": 0.02, 
              "ecutwfc": null, 
              "mixing_beta": 0.7, 
              "conv_thr": 1e-06}, 
          "atoms": "CC", 
          "pseudopotentials": {"C": "C.pbe-n-rrkjus_psl.0.1.UPF"}, 
          "kpts": [12, 12, 1], 
          "cell": [1, 1, 1], 
          "pbc": [1, 1, 1], 
          "positions": [[0.333333333, 0.666666666, 0.5], [0.666666666, 0.333333333, 0.5]], 
          "crystal_coordinates": true
        }


    """
    #Create input files
    with open(file) as json_file:
        matdict = json.load(json_file)


    atoms = Atoms(matdict['atoms'], 
            positions = matdict['positions'], 
            cell  = matdict['cell'], 
            pbc   = matdict['pbc']
            )

    ase_dict = dict(atoms = atoms, 
                    crystal_coordinates = matdict['crystal_coordinates'], 
                    pseudopotentials   = matdict['pseudopotentials'], 
                    kpts               = matdict['kpts'])


    return atoms, ase_dict, matdict['template']

  @classmethod
  def from_flat_JSON(cls, file):
    """
    Create ase.Atoms object from a json file and a dictionary of settings. The dict is used to create a template which may be used to perform convergence.

    Args: json file with structure.

          {"template": 
            {"calculation": "scf", 
              "pseudo_dir": "../pseudo/", 
              "outdir": "../tmp/", 
              "prefix": "CsPbI3", 
              "a": 6.27514229,
              "nat": 3, "ntyp": 3, 
              "space_group": 221, 
              "occupations": "smearing", 
              "smearing": "cold", 
              "degauss": 0.0146997236, 
              "ecutwfc": 5, 
              "conv_thr": 1e-06, 

              "atoms": "CsPbI", 
              "pseudopotentials": {"Cs": "C.pbe-n-rrkjus_psl.0.1.UPF", 
                                "Pb": "C.pbe-n-rrkjus_psl.0.1.UPF", 
                                "I": "C.pbe-n-rrkjus_psl.0.1.UPF"}, 
              "kpts": [2,2,2], 
              "cell": [1, 1, 1], 
              "pbc": [1, 1, 1], 
              "positions": [[0.5, 0.5, 0.5], 
                        [0,   0,  0],
                        [0,   0,  0.5]], 
              "crystal_coordinates": true
          }

    """
    #Create input files
    with open(file) as json_file:
        matdict = json.load(json_file)

#
#    atoms = Atoms(matdict['atoms'], 
#            positions = matdict['positions'], 
#            cell  = matdict['cell'], 
#            pbc   = matdict['pbc']
#            )
#
#    ase_dict = dict(atoms = atoms, 
#                    crystal_coordinates = matdict['crystal_coordinates'], 
#                    pseudopotentials   = matdict['pseudopotentials'], 
#                    kpts               = matdict['kpts'])
#
#
    return matdict
def load_variables_from_file(file_path):
  """
  DEPRECATE
  """
  variables = {}
  with open(file_path) as f:
      exec(f.read(), variables)
  return variables

def get_vars(file_path, var_names):
  """
  DEPRECATE?

  Usage: 
    mats[0] = filepath
    requested_vars = ['efermi', 'title', 'xlimDOS']
    efermi, title, xlimDOS = get_variables_in_order(mats[0], requested_vars)
  """

  variables = load_variables_from_file(file_path)
  return [variables[name] for name in var_names if name in variables]
