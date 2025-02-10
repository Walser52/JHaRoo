from typing import Union, Optional
from typing import List, Tuple, Dict, Any
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.codes.espresso.io import QEModifier
import re
from pathlib import Path
from jhr.io.base import Basher
import matplotlib.pyplot as plt
from ase import Atoms

from jhr.core.convergers import BaseConverger

from jhr._error import Error

import logging 


logging.basicConfig(
  filename = "app.log",
  format="{message} - {asctime} - {levelname}",
   style="{",
   datefmt="%Y-%m-%d %H:%M",
   level=logging.INFO)


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

    def gen_atoms_from_template(self, template):
      """
      Extract atoms object from template. 

      Returns: 
        atoms: ase's atoms object. 
        template: modified template.
      """
      #Create atoms object from template
      atoms_dict = {}
      for key in ['positions', 'cell', 'pbc']:
        if key in template.keys(): atoms_dict[key] = template.pop(key)
      symbols = template.pop('atoms')

      atoms = Atoms(symbols, **atoms_dict)

      return atoms, template

    def extract_ase_dict(self, template, return_atoms = False):
      """
      Pops out ase_dict elements from template. 

      Args: template
      Returns: 
        ase_dict 
        template: modified by popping ase_dict 
      """
      atoms, template = self.gen_atoms_from_template(template)

      #Create ase dict for other options
      ase_dict = {'atoms': atoms}
      for key in ['pseudopotentials', 'kpts', 'crystal_coordinates', 'additional_cards', 'koffset', 'kspacing']:
          if key in template.keys(): ase_dict[key] = template.pop(key)
      
      if return_atoms: return ase_dict, template, atoms

      return ase_dict, template

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
        ase_dict, template = self.extract_ase_dict(template)


#        #Create atoms object from template
#        atoms_dict = {}
#        for key in ['positions', 'cell', 'pbc']:
#          if key in template.keys(): atoms_dict[key] = template.pop(key)
#        symbols = template.pop('atoms')
#
#        atoms = Atoms(symbols, **atoms_dict)
#
#        #Create ase dict for other options
#        ase_dict = {'atoms': atoms}
#        for key in ['pseudopotentials', 'kpts', 'crystal_coordinates', 'additional_cards', 'koffset', 'kspacing']:
#            if key in template.keys(): ase_dict[key] = template.pop(key)


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


#    @staticmethod
#    def read_total_energy(file):
#      total_energy = extract_number(file, starts_with = '!')
#      return total_energy

    @staticmethod
    def read_convergence(in_file = None, what = 'total energy'):
      if read == 'total energy':
        total_energy = extract_number(file, starts_with = '!')

      return
      
    def run_conv_one(self, files = [], folder = '.', prefix = '', ext = '.in', code = 'pw.x', tolerance = 0.00001, 
                    relative = True, check_convergence = True, break_on_converge = True,
                    file_out = None):
      """
      Run convergence over 'files'. If files aren't given, look in `folder` for files starting with `prefix` and ending with `in'. 
      Run convergence using `code` and find converged value if `check_convergence` using `relative` error. 

      Args:
        files = List of files on which to run convergence. Uses prefix and ext to find files if none are given.
        folder, prefix, ext = If no files are given, then look for files starting with `prefix` and ending with `ext` in `folder`.
        tolerance   = threshold to use for convergence
        relative = Relative or absolute tolerance.
        check_convergence = Checks if convergence is met in parallel. Breaks convergence loop when threshold is met. 
        file_out = Output file for writing convergence results.
      Returns: 
        converged: Whether converged or not
        vals: values on which convergence was achieved
      """
#      if file_out is None:
#        raise ValueError("Provide output file name")
      Error().no_output_file(file_out)


      # If no files given then use the prefix and extension to find files in folder.
      if len(files) == 0: 
        files = list(Path(folder).glob(f'{prefix}*{ext}')) 
        files = sorted(files, key=lambda f: int(f.stem.split(f'{prefix}_')[-1]))  #Order files numerically?


      # Run convergence tests on files. 
      convergence_params = []
      converged = False
      for f_in, vals in zip(files, self.valuesets):
        #Run commands
        stem, f_out = Path(f_in).stem, (Path(f_in).stem + '.out')

        command = f"{code} < {f_in} > {f_out}"
        Basher.runcommand(command)

        #Read and update convergence params        
        conv_param = self.read_convergence(in_file = f'{f_out}', what = 'total energy')
        convergence_params.append(conv_param)

        #Plot convergence parameter and write to file
        plt.plot(convergence_params, marker = 's')
        plt.savefig(f'{file_out}.pdf')
    
        with open(file_out, 'a') as f: 
          f.write(f'{str(vals)}\t{str(conv_param)}\n')
        print(convergence_params)

        #Check if convergence has been achieved and return converged value
        if check_convergence:
          converged, self.converged_val = self.check_convergence(convergence_params, tolerance, relative)
          if converged: 
            logging.info(f"Conv achieved {self.converged_val=}")
            if break_on_converge:   #break loop if convergence achieved?
              return self.converged_val


#      TESTING
      logging.info(f"Conv not achieved or not tests {vals=}")
      print("TESTING: Convergence not tested. Last value being taken as converged value")
      self.converged_val = vals
      return self.converged_val


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

