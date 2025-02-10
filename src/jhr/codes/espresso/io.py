import json
from ase import Atoms

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

#=================Modifiers==================
from jhr.io.modifier import Modifier

class QEModifier(Modifier):
    """
    Class for modifiying espresso input files. 
    """
    @staticmethod
    def remove_ibrav(lines: list):
        """
        Removes ibrav from lines read from a file.
        """
        new_lines = []
        for line in lines:
            if 'ibrav' not in line.lower():
                new_lines.append(line)  # Keep the lines that don't contain 'ibrav'
        return new_lines


    @staticmethod
    def modify_atomic_positions(lines, atomic_positions: str = ''):
        """
        Modify the ATOMIC_POSITIONS line to 'ATOMIC POSITIONS crystal_sg' e.g.
        or to a user-specified atomic_positions string.
        """
        new_lines = []
        for line in lines:
            # Modify the ATOMIC_POSITIONS line if the atomic_positions string is provided
            if 'atomic_positions' in line.lower() and len(atomic_positions) > 0:
                new_lines.append(f'ATOMIC_POSITIONS {atomic_positions}\n')
            else:
                new_lines.append(line)

        return new_lines

    @staticmethod
    def remove_cell_parameters(lines):
        """
        Remove the line containing 'CELL_PARAMETERS' and the following 3 lines.
        """
        new_lines = []
        skip_next_lines = 0  # Flag to keep track of how many lines to skip
        for line in lines:
            # Check for 'CELL_PARAMETERS' line and set skip_next_lines
            if 'cell_parameters' in line.lower():
                skip_next_lines = 3  # Skip the next 3 lines after 'CELL_PARAMETERS'
                continue  # Skip the 'CELL_PARAMETERS' line itself
            # Skip the next lines if flagged
            if skip_next_lines > 0:
                skip_next_lines -= 1
            else:
                new_lines.append(line)  # Keep this line if we are not skipping it

        return new_lines
  
