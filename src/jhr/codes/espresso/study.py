import logging
from typing import Dict, List, Union

import numpy as np
from ase import Atoms
from ase.io.espresso import (read_espresso_in, read_espresso_ph,
                             write_espresso_in, write_espresso_ph)

from jhr.codes.espresso.io import QEModifier
from jhr.core.study import BaseConvergenceCalculation, BaseNormalCalculation

logging.basicConfig(
    filename="app.log",
    format="{message} - {asctime} - {levelname}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)


class QEStudy:
    """
    Connects two or more chains. Essentially a DAG (Directed Acyclic Graph).
    """

    pass


class QEChain:
    """
    Create QE computaiton chains.
    """

    def __init__(self, chain=[]):
        self.chain = chain

    def run(self, command="", prepend=""):
        for each_calc in self.chain:
            each_calc.run(command, prepend)


class BaseQEConvergenceCalculation(BaseConvergenceCalculation):
    def __init__(
        self, template, parameters, criteria="", code="", method="grid", update={}
    ):
        """
        Convergence is performed over a grid. Nested convergence is to be done manually (for now)

        Args:
          template: Template to modify
          parameters: Parameters dict to modify in each template.
          convergence_style: nested/grid.

        Example:
          parameters = {'ecutwfc': [1,2,3], 'ecutrho': [4,5,6], 'nx,ny,nz':[[2,2,2],[4,4,4]]}


        """
        grepper = QEGrepper(criteria)
        super().__init__(template = template, 
                         parameters = parameters, 
                         code = code, 
                         method = method, 
                         update = update, 
                         grepper = grepper
                         )
        self.prefix = self.template["prefix"]

        #Create calculation set for convergence.
        self.calcs = self.create_base_calcs(template, self.params, self.vals)

        return

    def create_base_calcs(self, template, convs, vals):
        """
        Create base calcs. Returns a list of base normal calc objects.
        """
        calcs = []
        name = "_".join(convs)
        for i, combo in enumerate(vals):
            update = {k: v for (k, v) in zip(convs, combo)}

            files = [f"{self.prefix}{name}{i}.in", f"{self.prefix}{name}{i}.out"]
            calcs.append(
                BaseQENormalCalculation(
                    self.template.copy(),
                    self.code,
                    files=files,
                    run=False,
                )
            )
        return calcs


class BaseQENormalCalculation(BaseNormalCalculation):
    """
    code
    Functionality: Use json template to save QE input. Run QE input.

    Args:
    stem = File stem to save. Input files
    files = ('file_abc', 'file_xyz') or 'file' which becomes ('file.in', 'file.out')
    """

    def __init__(
        self,
        template=None,
        code="",
        update={},
        files=None,
        run=False,
        command="",
        **kwargs,
    ):
        """
        Args:
          template (dict|str|path): Read template either from a dictionary or a json file path.
          code (str): code to use
          files: Names to use for files.
                  If None given: Read from template['prefix']
                  If str given: Use that (append '.in' and '.out' for input and output
                  If list given: Use the first two as file names.
        """
        # Read and update template; set code; decide file names to use for .in/.out files
        super().__init__(template, code, update, files)

        self.result = np.nan

        ase_dict, qe_template = self.extract_ase_dict(self.template)
        self._save_file(self.file_in, qe_template, ase_dict, self.code)

        if run:
            self.run()
        return

    def extract_ase_dict(self, template, return_atoms=False):
        """
        Pops out ase_dict elements from template.

        Args: template
        Returns:
        ase_dict
        template: modified by popping ase_dict
        """

        atoms, template = self.gen_atoms_from_template(template)

        # Create ase dict for other options
        ase_dict = {"atoms": atoms}
        for key in [
            "pseudopotentials",
            "kpts",
            "crystal_coordinates",
            "additional_cards",
            "koffset",
            "kspacing",
        ]:
            if key in template.keys():
                ase_dict[key] = template.pop(key)

        if return_atoms:
            return ase_dict, template, atoms

        return ase_dict, template

    def gen_atoms_from_template(self, template):
        """
        Extract atoms object from template.

        Returns:
          atoms: ase's atoms object.
          template: modified template.
        """
        # Create atoms object from template
        atoms_dict = {}
        for key in ["positions", "cell", "pbc"]:
            if key in template.keys():
                atoms_dict[key] = template.pop(key)
        symbols = template.pop("atoms")

        atoms = Atoms(symbols, **atoms_dict)

        return atoms, template

    def _save_file(self, filename, template, ase_dict: dict = {}, code: str = "ph.x"):
        """
        Save file
        Args:
          filename: File name
          template: template to pass to ase's espresso module methods.
          code: code which to pass to.
          ase_dict: other options. See ase's documentation.

        """
        #        print(filename, template, ase_dict)

        with open(filename, "w") as f:
            if code == "pw.x":
                write_espresso_in(f, input_data=template, **ase_dict)
            if code == "ph.x":
                write_espresso_ph(f, template, **ase_dict)

        logging.info(f"Saved {filename=}")
        return

    def ase_hacks(
        self,
        remove_ibrav=False,
        remove_cell_parameters=False,
        modify_atomic_positions=False,
        atomic_positions: str = "crystal_sg",
        verbose=False,
    ):
        """
        Some hacks for writing ase files for QE.
        """
        if remove_ibrav:
            QEModifier.modify_file(
                QEModifier.remove_ibrav, self.file_in, verbose=verbose
            )
        if remove_cell_parameters:
            QEModifier.modify_file(
                QEModifier.remove_cell_parameters, self.file_in, verbose=verbose
            )
        if modify_atomic_positions:
            QEModifier.modify_file(
                QEModifier.modify_atomic_positions,
                self.file_in,
                atomic_positions=atomic_positions,
                verbose=verbose,
            )

        return


    def _separate_args(self, templates: Union[Dict, List[Dict]]):
        """
        Sifts dictionary template into a format for ase. The file template is separated from other arguments.

        Args:
        templates

        Returns:
        mod_templates: modified by popping out unnecessary keys. Accepts a single dict or a list of dicts.
        ase_dicts: other options to be passed to ase.
        """

        if isinstance(templates, dict):
            templates = [templates]

        ase_dicts, mod_templates = [], []

        for template in templates:
            ase_dict, template = self.extract_ase_dict(template)

        mod_templates.append(template)
        ase_dicts.append(ase_dict)

        return mod_templates, ase_dicts



class Grepper():
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

class QEGrepper(Grepper):
    def read_criteria(self, in_file = None, what = 'total energy'):
        if what == 'total energy':
            criteria = self.extract_number(in_file, starts_with = '!')
        return criteria
     

