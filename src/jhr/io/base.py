import subprocess
from ase.io.espresso import read_fortran_namelist

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
    result = subprocess.run(command, shell=shell, text=text)
    cls.checkerror(result)
    return   
  

class FileHandler():
  """Class for handling files"""

  @classmethod
  def read_fortran_namelists(cls, filename):
    """Reads fortran namelist"""
    with open(filename,"r") as f:
      input_data, additional_cards = read_fortran_namelist(f)
    return input_data, additional_cards

  @classmethod
  def fortran_card_splitter(cls, additional_cards, keywords):
    """
    When importing fortran namelists, 
    additional_cards is a list of strings that needs to be split according to where the keywords come. 

    This function breaks additional cards and returns a dictionary. Keywords indicate starting points. 
    """
    # Keywords to identify sections


    # Initialize variables
    cards_dict = {}
    current_key = None

    # Iterate through the additional_cards list
    for line in additional_cards:
        # Check if the line starts with any of the keywords
        if any(line.startswith(keyword) for keyword in keywords):
            # Set the current key to this line
            current_key = line
            # Initialize an empty list for this key in the dictionary
            cards_dict[current_key] = []
        elif current_key:
            # Append the line to the current section's list
            cards_dict[current_key].append(line)
    return cards_dict


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
