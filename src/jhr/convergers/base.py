from typing import Union, Optional
from typing import List, Tuple, Dict, Any
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.io.modifiers import QEModifier
import re
from pathlib import Path
from jhr.io.base import Basher
import matplotlib.pyplot as plt
from ase import Atoms

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
    def _save_file(self, filename, template, ase_dict: dict = {}, code: str = 'ph'):
      """
      Save one file
      Args: 
        filename: File name
        template: template to pass to ase's espresso module methods.
        code: code which to pass to.
        ase_dict: other options. See ase's documentation.
      
      """
      with open(filename, "w") as f:
        print(code)
        if code == 'pw': write_espresso_in(f, input_data = template, **ase_dict)
        if code == 'ph': write_espresso_ph(f, template, **ase_dict)
      return



    def _separate_args(self, templates:Union[Dict, List[Dict]]):
      """
      Sifts flattened dictionary template into a format for ase. The file template is separated from other arguments.

      Args: 
        templates 

      Returns:
        template: modified by popping out unnecessary keys. Accepts a single dict or a list of dicts. 
        ase_dict: other options to be passed to ase. 
      """
      
      if isinstance(templates, dict): templates = [templates]

      ase_dicts, mod_templates = [], []

      for template in templates:


        #Create atoms object from template
        atoms = Atoms(template['atoms'], 
                positions = template['positions'], 
                cell  = template['cell'], 
                pbc   = template['pbc']
                )
        
        #Create ase_dict and modified template
        ase_dict = {'atoms': atoms}
        keys = list(template.keys())
        for key in keys:
          if key in ['pseudopotentials', 'kpts', 'crystal_coordinates']:
            ase_dict[key] = template.pop(key)


        mod_templates.append(template)
        ase_dicts.append(ase_dict)

      return mod_templates, ase_dicts

      

    def prepare_variants(self, template, parameters, valuesets, code = 'pw', label = 'Conv'):
      all_data, all_names = self.conv_on(template, parameters, valuesets, label = label) #Flat template variants.
      mod_templates, ase_dicts = self._separate_args(all_data)

      with open('abc.in', "w") as f:
        
        write_espresso_in(f, input_data = mod_templates[0], **ase_dicts[0])
#        if code == 'ph': write_espresso_ph(f, template, **ase_dict)

#      [print(d) for d in ase_dicts]
#      for template, ase_dict, name in zip(all_data, ase_dicts, all_names):
#        self._save_file(name, template, ase_dict, code = code)
      return





    def savefiles(self, prefix: str = '', files_data: List[dict] = [], ext: str = 'in', code: str = 'ph', ase_dict: dict = {}):
      """
      Use ase's espresso module to save files.

      Args:
        files_data (List[dict]): List of dictionaries containing the input variables. 
        ase_dict: other parameters such as additional cards which are passed to ase. 

      Returns:
        saved_files: List of saved files.
      """
      saved_files = []
      for i, data in enumerate(files_data):
        file = f'{prefix}_{i}.{ext}'
        with open(file, "w") as f:
          if code == 'pw': write_espresso_in(f, input_data = data, **ase_dict)
          if code == 'ph': write_espresso_ph(f, data, **ase_dict)
        saved_files.append(file)
      return saved_files


    def prepare_inputs(self, prefix: str = 'convfile', ext:str = 'in', code:str = 'pw', ase_dict:dict = {}, 
                        ase_hacks:bool = True, atomic_positions:str = 'crystal_sg', 
                        template = None, parameters = None, valuesets = None):
      """
      Express method for performing convergence. Use with care. The method:

      - Creates dicts for convergence which is to be carried out. 
      - Saves files 
      - Performs some ase hacks. using QEModifier class methods. 

      Args:
        prefix (str): File name prefix which to save. 

      Returns:
        saved_files (list): List of files saved. 

      """

      if valuesets is None: valuesets = self.valuesets
      
      all_files = self.conv_on(template = template, parameters = parameters, valuesets = valuesets) #No arguments passed, uses object parameters for inputs.
      print(ase_dict)
#      create another line for ase_dicts. Make the function check if parameter is in the template------------
      saved_files = self.savefiles(prefix = prefix, files_data = all_files, ext = ext, code = code, ase_dict = ase_dict) 

      #_____ASE Espresso hacks: Work arounds for modifying ASE output_______
      if ase_hacks: 
        for i in range(len(valuesets)):
          file = f'{prefix}_{i}.in'

          QEModifier.modify_file(QEModifier.remove_ibrav, file)
          QEModifier.modify_file(QEModifier.remove_cell_parameters, file)
          QEModifier.modify_file(QEModifier.modify_atomic_positions, file, atomic_positions = atomic_positions)

      return saved_files

    @staticmethod
    def read_total_energy(file):
      total_energy = extract_number(file, starts_with = '!')
      return total_energy
      


    def run_conv_one(self, files = [], folder = '.', prefix = '', ext = '.in', code = 'pw.x'):
      """
      Run convergence on one variable.

      Args:
        files = List of files on which to run convergence. 
      """
     
      if len(files) == 0: 
        files = list(Path(folder).glob(f'{prefix}*{ext}')) # Find files starting with 'name' and ending with '.in'
        files = sorted(files, key=lambda f: int(f.stem.split(f'{prefix}_')[-1]))



      convergence_param = []
      for f_in, vals in zip(files, self.valuesets):

        stem, f_out = Path(f_in).stem, (Path(f_in).stem + '.out')

        command = f"{code} < {f_in} > {f_out}"
        Basher.runcommand(command)
        convergence_param.append(self.read_total_energy(f'{f_out}'))

        plt.plot(convergence_param, marker = 's')
        plt.savefig('energy_conv.pdf')
        
        #check convergence criteria
        converged   = self.check_convergence(convergence_param)
        if converged: self.converged_val = vals

      
      return


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

