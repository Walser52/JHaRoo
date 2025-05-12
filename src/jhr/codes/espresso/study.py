import logging
import re
from typing import Dict, List, Union

import numpy as np
from ase import Atoms
from ase.io.espresso import (read_espresso_in, read_espresso_ph,
                             write_espresso_in, write_espresso_ph)

from jhr.codes.espresso.io import QEFileHandler, QEModifier, QEOutParser
from jhr.core.study import (BaseConvergenceCalculation, BaseNormalCalculation,
                            Grepper)
from jhr.io.linkers import QELinker

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

    def __init__(self, chain=[], linker = None):
        """
        QE Chain object for connecting calculations
        Args:
            chain = list of calculation objects
            linker = Linker object for linking outputs to inputs downstream.
        """
        self.chain = chain
        self.linker = linker

    def run(self, command="", prepend=""):
        for each_calc in self.chain:
            each_calc.run(command, prepend)

    def link(self, source = None, target = None, link = None):
        #Use the parser to extract data and update the other input templates downstream. 
        #Every calc has a parser. Invoke the parser.
        #source.parser(

        return


class BaseQEConvergenceCalculation(BaseConvergenceCalculation):
    """
    QE Convergence calcualtion class
    """

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
        # Create the grepper (and any other code specific tools and pass to base convergence calculator
        grepper = QEGrepper(criteria)
        super().__init__(
            template=template,
            parameters=parameters,
            code=code,
            method=method,
            update=update,
            grepper=grepper,
        )
        self.prefix = self.template["prefix"]

        # Create calculation set for convergence.
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
                    self.suite + "/" + self.code,
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
        #Determine: self.template, self.code, self.file_in, self.file_out, make updates, 
        super().__init__(template, code, update, files, QEFileHandler, QEOutParser)

        self.result = np.nan

        #Generate QE input file from self.template
        self.create_file_in()


        if run:
            self.run()
        return

    def create_file_in(self):
        """
        Write whatever self.template is to file given by self.file_in
        """
        ase_dict, qe_template = self._extract_ase_dict(self.template.copy())
        self._save_file(
            self.file_in, qe_template, ase_dict, self.code
        )  # create final .in


        return

    def _extract_ase_dict(self, template, return_atoms=False):
        """
        Pops out ase_dict elements from template.

        Args:
            template
        Returns:
        ase_dict
        template: modified by popping ase_dict
        """

        def gen_atoms_from_template(template):
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

            # saves any numbers after positions. Potentially dangerous
            atoms_ifpos = [site[4:] for site in atoms_dict["positions"]]
            atoms_dict["positions"] = [site[0:3] for site in atoms_dict["positions"]]

            atoms = Atoms(symbols, **atoms_dict)

            return atoms, template

        # Create Atoms object from template and pop atoms.
        atoms, template = gen_atoms_from_template(template)

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

    def _save_file(self, filename, template, ase_dict: dict = {}, code: str = "ph.x"):
        """
        Save file
        Args:
          filename: File name
          template: template to pass to ase's espresso module methods.
          code: code which to pass to.
          ase_dict: other options. See ase's documentation.

        """
        def write_file(filename, template, ase_dict = {}, code = None):
            """
            Write file
            """
            # write file
            print(filename)
            with open(filename, "w") as f:
                if code == "pw.x":
                    write_espresso_in(f, input_data=template, **ase_dict)
                if code == "ph.x":
                    write_espresso_ph(f, template, **ase_dict)

            return

        # return ibrav to its original value
        def update_ibrav(input_path, output_path=None, old_val="0", new_val=""):
            """
            Manually insert ibrav
            """
            with open(input_path, "r") as f:
                lines = f.readlines()

            updated_lines = []
            for line in lines:
                if "ibrav" in line:
                    # Replace only if ibrav = old_val (to avoid incorrect replacements)
                    line = re.sub(
                        rf"\bibrav\s*=\s*{old_val}\b", f"ibrav = {new_val}", line
                    )
                updated_lines.append(line)

            # Write to output (overwrite if output_path is None)
            if output_path is None:
                output_path = input_path

            with open(output_path, "w") as f:
                f.writelines(updated_lines)
            return
        #________________________________________________

        # set ibrav to 0 (because ase doesn't work with ibrav!=0)
        if "ibrav" in template.keys():
            ibrav = template["ibrav"]
            template["ibrav"] = 0
            write_file(filename, template, ase_dict, code = code)
            update_ibrav(filename, new_val=ibrav)
            if ibrav != 0: 
                self.ase_hacks(remove_cell_parameters = True)
        # if 
        else:
            write_file(filename, template, ase_dict, code = code)
        # log
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


class QEGrepper(Grepper):
    def __init__(self, criteria):
        super().__init__(criteria)

    def fetch(self, from_file=None):
        """ """
        if self.criteria == "total energy":
            val = self.extract_number(from_file, starts_with="!")
        return val

    def read_criteria(self, in_file=None, what="total energy"):
        if what == "total energy":
            criteria = self.extract_number(in_file, starts_with="!")
        return criteria
