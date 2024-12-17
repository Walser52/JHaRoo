from typing import Union, Optional
from typing import List, Tuple, Dict, Any
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.io.modifiers import QEModifier
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


class QEConverger(BaseConverger):
    def _save_file(self, filename, template, ase_dict: dict = {}, code: str = 'ph.x', ase_hacks = True, atomic_positions:str = 'crystal_sg', verbose = False):
      """
      Save one file
      Args: 
        filename: File name
        template: template to pass to ase's espresso module methods.
        code: code which to pass to.
        ase_dict: other options. See ase's documentation.
      
      """
      with open(filename, "w") as f:
        if code == 'pw.x': write_espresso_in(f, input_data = template, **ase_dict)
        if code == 'ph.x': write_espresso_ph(f, template, **ase_dict)

      if ase_hacks: 
        QEModifier.modify_file(QEModifier.remove_ibrav, filename, verbose = verbose)
        QEModifier.modify_file(QEModifier.remove_cell_parameters, filename,verbose = verbose)
        QEModifier.modify_file(QEModifier.modify_atomic_positions, filename, atomic_positions = atomic_positions, verbose = verbose)

      logging.info(f"Saved {filename=}")
      return



    def _separate_args(self, templates:Union[Dict, List[Dict]]):
      """
      Sifts dictionary template into a format for ase. The file template is separated from other arguments.

      Args: 
        templates 

      Returns:
        mod_templates: modified by popping out unnecessary keys. Accepts a single dict or a list of dicts. 
        ase_dicts: other options to be passed to ase. 
      """
      
      if isinstance(templates, dict): templates = [templates]

      ase_dicts, mod_templates = [], []

      for template in templates:


        #Create atoms object from template
        atoms_dict = {}
        for key in ['positions', 'cell', 'pbc']:
          if key in template.keys(): atoms_dict[key] = template.pop(key)
        symbols = template.pop('atoms')

        atoms = Atoms(symbols, **atoms_dict)

        #Create ase dict for other options
        ase_dict = {'atoms': atoms}
        for key in ['pseudopotentials', 'kpts', 'crystal_coordinates', 'additional_cards', 'koffset', 'kspacing']:
            if key in template.keys(): ase_dict[key] = template.pop(key)


        mod_templates.append(template)
        ase_dicts.append(ase_dict)

      return mod_templates, ase_dicts

      

    def prepare_variants(self, template: dict, parameters: list, valuesets, code = 'pw', label = 'Conv', ase_hacks = True, atomic_positions:str = 'crystal_sg', verbose = False):
      """
      Prepare variants of the template for convergence. 

      Args:
        template: Dictionary
        ase_hacks: Removes ibrav and cell_paramters. Also modifies atomic positions by adding 'atomic_positions'

      Example:
        template = {"calculation": "scf", 
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
                    "pseudopotentials": {"Cs": "Cs.pbe-n-rrkjus_psl.0.1.UPF", 
                                      "Pb": "Pb.pbe-n-rrkjus_psl.0.1.UPF", 
                                      "I": "I.pbe-n-rrkjus_psl.0.1.UPF"}, 
                    "kpts": [2,2,2], 
                    "cell": [1, 1, 1], 
                    "pbc": [1, 1, 1], 
                    "positions": [[0.5, 0.5, 0.5], 
                              [0,   0,  0],
                              [0,   0,  0.5]], 
                    "crystal_coordinates": true
                }
      Returns: 
        List of saved files
      """
      all_data, all_names = self.conv_on(template, parameters, valuesets, label = label) #Flat template variants.
      mod_templates, ase_dicts = self._separate_args(all_data)

      for template, ase_dict, name in zip(mod_templates, ase_dicts, all_names):
        self._save_file(name, template, ase_dict, code = code, ase_hacks = ase_hacks, atomic_positions = atomic_positions, verbose = verbose)

      return all_names


    @staticmethod
    def read_total_energy(file):
      total_energy = extract_number(file, starts_with = '!')
      return total_energy
      
    def run_conv_one(self, files = [], folder = '.', prefix = '', ext = '.in', code = 'pw.x', tolerance = 0.1, relative = True):
      """
      Run convergence on one variable.

      Args:
        files = List of files on which to run convergence. Uses prefix and ext to find files if none are given.
        tolerance   = threshold to use for convergence
        relative = Relative or absolute tolerance.
      Returns: 
        converged: Whether converged or not
        vals: values on which convergence was achieved
      """
      
      # If no files given then use the prefix
      if len(files) == 0: 
        files = list(Path(folder).glob(f'{prefix}*{ext}')) # Find files starting with 'name' and ending with '.in'
        files = sorted(files, key=lambda f: int(f.stem.split(f'{prefix}_')[-1]))


      # Run convergence tests on files. 
      convergence_param = []
      converged = False
      for f_in, vals in zip(files, self.valuesets):

        stem, f_out = Path(f_in).stem, (Path(f_in).stem + '.out')

        command = f"{code} < {f_in} > {f_out}"
        Basher.runcommand(command)
        convergence_param.append(self.read_total_energy(f'{f_out}'))

        plt.plot(convergence_param, marker = 's')
        plt.savefig('energy_conv.pdf')
        
        print(convergence_param)
        #check convergence criteria
        converged = self.check_convergence(convergence_param, tolerance, relative)
        if converged: 
          self.converged_val = vals
          break;
      logging.info(f"Conv achieved/not {vals=}")
      return self.converged_val



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

