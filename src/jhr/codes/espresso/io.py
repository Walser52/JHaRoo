import json
from ase import Atoms
import tempfile
import os
import re
from ase.io.espresso import read_espresso_in
from jhr.io.base import FileHandler
from pathlib import Path

class QEFileHandler(FileHandler):
  #Card list in different QE input files. 
  cards = {
              'pw.x': ['k_points', 'atomic_positions', 'atomic_species'],
              'ph.x': ['qPointsSpecs']
  }
  
  #convert to list
  card_list = []
  for k,v in cards.items():
    card_list.extend(v)


  def __init__(self, template):
    """
    Args:
        template (str|path): File path with template. Could be json or qe input.
    """

    filepath = Path(template)
    name, ext = filepath.stem, filepath.suffix

    if ext == '.in':
        new_file = filepath.with_suffix('.json')
        self.qeinput2json(file_in = template, file_out = new_file, update = {})

    
    self.template = self.from_flat_JSON(new_file)

    return 

  @classmethod
  def from_scfin(cls):

    return 

  def additional_cards_splitter(self, additional_cards):
    keywords = ["ATOMIC_SPECIES", "ATOMIC_POSITIONS", "K_POINTS"]
    cards_dict = self.fortran_card_splitter(additional_cards, keywords)

    for k in cards_dict.keys():
      #parse each key.
      if 'K_POINTS' in k.upper():
  #     print(cards_dict[k][0].split())
        pass
    return cards_dict

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

    return matdict

  def flatten_dict(self, d):
      """
      Flattens a nested dict by removing parents. Helps in reading scf input file.
      """
      items = []
      for k, v in d.items():
          new_key = f"{k}" 

          try:
            v = v.data
          except:
            pass

          if isinstance(v, dict):
              items.extend(self.flatten_dict(v).items())
          else:
              items.append((new_key, v))

      return dict(items)




  def card_parser(self, cards_dict, card_id = 'k_points'):
      """
      For parsing additional_cards. 
      Args:
          card_id
      Returns:
          Dictionary with two keys 'setting' and 'values'

      Example:
          For:
          k_points automatic
          4 4 4 0 0 0

          Returns:
          {'setting': automatic, 'values': [4,4,4,0,0,0]


      """
      def splitter(row, card_id = 'k_points'):
          """
          Split a row of additional_cards. 
          """
          def convert_value(value):
              """
              Convert value to float, int or return as string
              """
              try:
                  if "." in value:  # Check if it's a float
                      return float(value)
                  return int(value)  # Otherwise, try converting to int
              except ValueError:
                  return value  # If conversion fails, return as string

          return [convert_value(v) for v in row.split()]
      #------------------------------------------------

      #Find the key with k_points in it.
      for key in cards_dict.keys():
          if key.lower().startswith(card_id):
              parts = key.split()  # Split at the first underscore
              setting = parts[1] if len(parts) > 1 else ""  
              break

      #Extract values and return dict
      values = cards_dict[key]
      splitted_values = []

      for val in values:
          split_val = splitter(val, card_id)
          splitted_values.append(split_val)

      return {card_id: {'setting': setting, 'values': splitted_values}}


  def card2dict(self, card_dict):
      """
      Args:
        card_dict (dict): Dict with two keys 'settings' and 'values' 
      """


      to_ase = {}
      
      for key in card_dict.keys():
        values = card_dict[key]['values']
        setting = card_dict[key]['setting'] 

        if key == 'k_points':
            to_ase['kpts'] = values[0]

        elif key == 'atomic_positions':
            to_ase['positions'], to_ase['atoms'] = [], ''
            for val in values:
              to_ase['positions'].append(val[1:])
              to_ase['atoms']+=(val[0])

        elif key == 'atomic_species':
            to_ase['pseudopotentials'] = {val[0]:val[2] for val in values}
              

    
      
      return to_ase


  def qeinput2json(self, file_in = 'scf.in', file_out = 'scf.json', update = {}):
    """
    Convert qe input file to json.

    file_in: qe input file
    file_out: json output file
    update (dict): any other updates that you want to write to json. e.g. {'pbc':[1,1,1]}
    """
    #Read input file
    input_data, additional_cards = self.read_fortran_namelists(file_in)

    #Split cards according to QE namelists and cards. 
    cards_dict = self.additional_cards_splitter(additional_cards)
    flattened_dict = self.flatten_dict(input_data)

    #Parse cards into dictionaries.
    parsed = {}
    for k in self.card_list:
        try: 
            parsed.update(self.card_parser(cards_dict, card_id = k))
        except:
            pass

    #Convert dict to dict suitable for json input file in JHR.
    ase_dict = self.card2dict(parsed)

    flattened_dict.update(ase_dict)
    flattened_dict.update(update)

    #Write to json.
    with open(file_out, 'w') as fp:
        json.dump(flattened_dict, fp)

    return 

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


    @staticmethod
    def remove_ibrav_and_read(input_filename):
        """
        Sets ibrav to 0 in a temp file and reads because ase does not read qe input file if ibrav != 0.

        Returns;    
          atoms
          parameters
        """
        # Read the original input file
        with open(input_filename, 'r') as f:
            lines = f.readlines()
        
        # Modify lines: set any ibrav parameter to 0
        new_lines = []
        for line in lines:
            if 'ibrav' in line.lower():
                # Use a regular expression to replace the value after 'ibrav ='
                line = re.sub(r'(ibrav\s*=\s*)\S+', r'\1 0', line, flags=re.IGNORECASE)
            new_lines.append(line)
        
        # Write modified content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.in') as tmp:
            temp_filename = tmp.name
            tmp.writelines(new_lines)
        
        # Read the temporary file using ASE's read_espresso_in function
        atoms, parameters = read_espresso_in(temp_filename)
        
        # Delete the temporary file
        os.remove(temp_filename)
        
        return atoms, parameters
  
