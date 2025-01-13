from typing import Union, Optional
from typing import List, Tuple, Dict, Any
#from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
#from jhr.io.modifiers import QEModifier
import re
from pathlib import Path
from jhr.io.base import Basher
import matplotlib.pyplot as plt
from ase import Atoms

import logging 


logging.basicConfig(
  filename = "app.log",
  format="{message} - {asctime} - {levelname}",
   style="{",
   datefmt="%Y-%m-%d %H:%M",
   level=logging.INFO)


#name = "Samara"
#logging.debug(f"{name=}")
#logging.warning(f"{name=}")


class Converter():
  
  def VASP2QE(self):
#  VASP2JSON template
    return




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
        self.converged_val = None

#        for eachset in valuesets:
#          if not isinstance(eachset, (list, tuple)): 
#            eachset = [eachset]
#          if len(eachset) != len(parameters):
#            raise ValueError(f"Length of at least one value set does not match the number of parameters.")

        return


    def conv_on(self, template=None, parameters=None, valuesets=None, prefix = 'File', label = 'Conv'):
        """
        Create convergence files changing parameters according to values sets.

        "template" (dict): Contains parameters. See ASE documentation
        "parameters" (list of strings): Parameters to change.
        "valuesets" (list of lists)   : sets of values.
        """

        all_files = []
        all_filenames = []

        if parameters is None:  parameters = self.parameters
        if valuesets is None:   valuesets = self.valuesets
        if template is None:    template = self.template


        #Loop over value sets (i.e. make len(valuesets) variants with each variant changing len(parameters) number of entries. 
        for j, values in enumerate(valuesets):
          new_template = template.copy()
          if 'prefix' in template.keys(): prefix = template['prefix']

          all_filenames.append(f'{prefix}{label}_{j}.in')            
          for i, p in enumerate(parameters):
#                print(valuesets)
              if isinstance(values, (list, tuple)) and len(values) > 1:
                new_template[p] = values[i]
              else: 
                values = [values]
                new_template[p] = values[i]
          
          all_files.append(new_template)

        return all_files, all_filenames

    @staticmethod
    def check_convergence(values, tolerance=0.01, relative = True):
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
        return self._converged_val

    @converged_val.setter
    def converged_val(self, value: float):
        """Setter for the converged_val attribute to enforce a condition"""
        self._converged_val = value





#====================

class MaterialTemplate():
  def __init__(self, template):
     
#    qe_template
#    ase_dict
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

