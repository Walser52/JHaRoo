import subprocess

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
