from typing import Union, Optional
from typing import List, Tuple
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.io.modifiers import QEModifier
import re


class BaseConverger:
    def __init__(self, parameters = None, valuesets = None, template = {}):
        # Initialize any attributes or settings if needed
        """
        Base converger that others use by inheritance. 

        Args:
          parameter (list): parameters which to converge.
          valuesets (list(tuple)): values. Length of each valuesets should be the same as the length of parameter.

        """

        self.parameters = parameters
        self.valuesets = valuesets
        self.template = template

        for eachset in valuesets:
          if not isinstance(eachset, (list, tuple)): 
            eachset = [eachset]
          if len(eachset) != len(parameters):
            raise ValueError(f"Length of at least one value set does not match the number of parameters.")

        return


    def conv_on(self, template=None, parameters=None, valuesets=None):
        """
        Create convergence files changing parameters according to values sets.

        "template" (dict): Contains parameters. See ASE documentation
        "parameters" (list of strings): Parameters to change.
        "valuesets" (list of lists)   : sets of values.
        """

        all_files = []

        if parameters is None:  parameters = self.parameters
        if valuesets is None:   valuesets = self.valuesets
        if template is None:    template = self.template
        # Loop over the valuesets and adjust the template

        for values in valuesets:
            new_template = template.copy()  # Make a copy to avoid modifying the original
            for i, p in enumerate(parameters):
#                print(valuesets)
                if isinstance(values, (list, tuple)) and len(values) > 1:
                  new_template[p] = values[i]
                else: 
                  values = [values]
                  new_template[p] = values[i]
            
            all_files.append(new_template)

        return all_files

    @staticmethod
    def check_convergence(values, tolerance=0.01):
        """
        Check if the successive values in the list have converged based on relative error.

        Args:
            values (list): A list of numerical values.
            tolerance (float): The convergence tolerance in percentage (default is 0.01%).

        Returns:
            bool: True if converged, False otherwise.
        """
        converged = False

        if len(values) > 1: 

#          for i in range(1, len(values)):
              # Calculate the relative error between successive values
          relative_error = abs(values[-1] - values[-2]) / abs(values[-2]) * 100
          
          # Check if the relative error is within the tolerance
          if relative_error < tolerance:
              print("Convergence achieved")
              converged = True

        return converged  


    @property
    def converged_val(self):
        """Getter for the converged_val attribute"""
        return self._radius

    @converged_val.setter
    def converged_val(self, value: float):
        """Setter for the converged_val attribute to enforce a condition"""
        self._converged_val = value


class QEConverger(BaseConverger):
    def savefiles(self, prefix: str = '', files_data: List[dict] = [], ext: str = 'in', code: str = 'ph', ase_dict: dict = {}) -> None:
      """
      Use ase's espresso module to save files.
      Args:
        files_data (List[dict]): List of dictionaries containing the input variables. 
        ase_dict: other parameters such as additional cards which are passed to ase. 
      """
#      print(ase_dict)
      #phonon files write
      for i, data in enumerate(files_data):
        file = f'{prefix}_{i}.{ext}'
        with open(file, "w") as f:
          if code == 'pw': write_espresso_in(f, input_data = data, **ase_dict)
          if code == 'ph': write_espresso_ph(f, data, **ase_dict)
      return

    @staticmethod
    def read_total_energy(file):
      total_energy = extract_number(file, starts_with = '!')
      return total_energy
      

    def conv_express(self, prefix: str = 'convfile', ext:str = 'in', code:str = 'pw', ase_dict:dict = {}, ase_hacks:bool = True, atomic_positions:str = 'crystal_sg', template = None, parameters = None, valuesets = None):
      """
      Express method for performing convergence. Use with care. The method:

      - Creates dicts for convergence which is to be carried out. 
      - Saves files 
      - Performs some ase hacks. using QEModifier class methods. 

      Args:
        prefix (str): File name prefix which to save. 

      """

      if valuesets is None: valuesets = self.valuesets

      all_files = self.conv_on(template = template, parameters = parameters, valuesets = valuesets) #No arguments passed, uses object parameters for inputs.
      self.savefiles(prefix = prefix, files_data = all_files, ext = ext, code = code, ase_dict = ase_dict) 

      #_____ASE Espresso hacks: Work arounds for modifying ASE output_______
      if ase_hacks: 
        for i in range(len(valuesets)):
          file = f'{prefix}_{i}.in'

          QEModifier.modify_file(QEModifier.remove_ibrav, file)
          QEModifier.modify_file(QEModifier.remove_cell_parameters, file)
          QEModifier.modify_file(QEModifier.modify_atomic_positions, file, atomic_positions = atomic_positions)

      return







def extract_number(file_path, starts_with = '!') -> float:
    """
    Finds the line starting with '!' and extracts the number from it.
    
    Args:
        file_path (str): Path to the file to be read.

    Returns:
        float: The number found in the comment line, or None if not found.
    """
    with open(file_path, 'r') as file:
        for line in file:
            if line.lstrip().startswith(starts_with):
                # Using regular expression to find numbers (integers or floating-point)
                match = re.search(r'!.*\s*(-?\d+(\.\d+)?)', line)
                if match:
                    return float(match.group(1))  # Return the number as a float
    return None  # If no line starting with '!' is found

