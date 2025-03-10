# study level classes.
import logging
import re
from collections import defaultdict
from itertools import product
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ase.io.espresso import (read_espresso_in, read_espresso_ph,
                             write_espresso_in, write_espresso_ph)

from jhr.codes.espresso.io import QEFileHandler, QEModifier
from jhr.io.base import Basher

logging.basicConfig(
    filename="app.log",
    format="{message} - {asctime} - {levelname}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)


class Chain:
    def __init__(self):
        pipe = ["pw_convA", "pw_convB", "pw_convC"]
        pass

    def createCalculators():
        # Create calculators corresponding to pipes.
        # Convergence type
        # Single type
        pass


class Calculation:
    """
    Args:
    calc_type = 'normal', 'convergence'
    suite: 'QE', 'Yambo'
    code:   'pw.x'
    """

    def __init__(
        self,
        template=None,
        code="",
        mode="normal",
        settings={},
        files=["", ""],
        run=False,
    ):
        """
        Args:
        code = '{suite}/{code}' e.g. 'qe/pw.x'. Use '/' to separate suite and code.
        files = ('file_abc', 'file_xyz') or 'file' which becomes ('file.in', 'file.out')
        """
        self.suite = code.lower().split("/")[0]
        self.code = code.lower().split("/")[1]
        self.mode = mode.lower()
        if self.suite == "qe" or self.suite == "espresso":
            if self.mode == "normal":
                self.calc = BaseQENormalCalculation(
                    template, code, files=files, run=run
                )
            elif self.mode == "convergence":
                self.calc = BaseQEConvergenceCalculation(template, code, settings, run)
        return


class BaseConvergenceCalculation:
    """
    Base class for convergence calculations
    """

    def __init__(
        self, template, parameters, code="", method="grid", update={}, grepper=None
    ):
        """
        Args:
          template (dict|str|path): Read template either from a dictionary or a json file path.
          code (str): code to use
          criteria = convergence criteria (i.e. parameter e.g. 'Total Energy')
          update: Global updates that maybe needed for the template.
          grepper: Grepper class object for reading output files (to be provided by the code specific convergence class)
        """

        self.suite = code.split("/")[0]
        self.code = code.split("/")[1]
        self.template = self.read_template(template, update)
        self.parameters = parameters.keys()
        self.grepper = grepper
        self.converged = np.nan
        # create an appropriate grepper depending on suite/code.

        # Create convergence value table
        def separate_params(parameters):
            """
            Separate parameters into convergence labels and values.

            Args:
                parameters (dict): {'kx, ky, kz':[[4,4,2], [6,6,4]],
                                    'ecutwfc': [10, 15, 30]
                                    }
            Returns:
                convs: List of parameters over which convergence is performed.
                vals: List of list of value sets over which convergence is performed.
            """
            convs = []
            vals = []
            for each_conv in parameters.keys():
                convs.append(
                    each_conv.split(",")
                )  # split keys because they maybe comma separated.
                vals.append(parameters[each_conv])
            convs = [x for xs in convs for x in xs]
            return convs, vals

        convs, vals = separate_params(parameters)

        def conv_method(convs, vals):
            # Whether to do nested convergence or grid?
            """
            Sorts values according to whether convergence is in grid or nested format.
            """
            if method == "nested":
                [print(f"performing convergence on {c}") for c in convs]
                print("NOT YET IMPLEMENTED")
                raise Exception("Sorry, nested convergence not implemented")
            elif method == "grid":
                combinations = self.convergence_combos(vals)
            return combinations

        self.params = convs
        self.vals = conv_method(convs, vals)

        # initialize self.calcs (for creating an iterator)
        self.calcs = [None] * len(vals)

        return

    def read_template(self, template, update):
        """
        Read template from file depending on code.
        """
        if not isinstance(template, dict):
            if self.suite == "qe":
                template = QEFileHandler.from_flat_JSON(template)
        template.update({k: update[k] for k in update.keys()})

        return template

    def convergence_combos(self, vals):
        """
        Create outer product for convergence
        """
        combinations = list(product(*vals))
        return combinations

    def run(
        self,
        command="",
        prepend="",
        check_conv=False,
        conv_threshold = 1e-6,
        break_on_conv = False
    ):
        """
        Args:
            check_conv (bool): True. Check convergence in parallel
        """

        def to_tsv(filename, calc_x, calc_y, mode):
            """Append only the latest convergence result to a TSV file."""
            formatted_x = (
                "\t".join(map(str, calc_x))
                if isinstance(calc_x, (list, tuple))
                else str(calc_x)
            )
            formatted_y = (
                "\t".join(map(str, calc_y))
                if isinstance(calc_y, (list, tuple))
                else str(calc_y)
            )

            with open(filename, mode=mode) as file:  # 'mode' controls overwrite/append
                file.write(
                    f"{formatted_x}\t{formatted_y}\n"
                )  # Write values separated by a tab

            return

        def plot_tsv(filename, output_pdf="plot.pdf"):
            """Reads a TSV file and plots scatter or line plots based on column count."""
            data = []

            # Read TSV file
            with open(filename, "r") as file:
                for line in file:
                    values = line.strip().split("\t")  # Split by tab
                    try:
                        values = [float(v) for v in values]  # Convert to numbers
                        data.append(values)
                    except ValueError:
                        continue  # Skip non-numeric rows

            data = np.array(data, dtype=object)  # Convert to NumPy array

            plt.figure(figsize=(6, 4))  # Set figure size

            if data.shape[1] == 2:  # Case: Two columns (x, y)
                plt.scatter(data[:, 0], data[:, 1], color="blue", label="Data")
                plt.xlabel("X-axis")
                plt.ylabel("Y-axis")

            elif data.shape[1] == 3:  # Case: Three columns (x, category, y)
                line_data = defaultdict(
                    list
                )  # Dictionary to store data for each category

                for row in data:
                    x, category, y = row
                    line_data[category].append((x, y))  # Group by category

                for category, points in line_data.items():
                    points.sort()  # Sort by x for proper line plotting
                    xs, ys = zip(*points)
                    plt.plot(xs, ys, marker="o", label=f"Category {category}")

                plt.xlabel("X-axis")
                plt.ylabel("Y-axis")
                plt.legend(title="Categories")

            plt.savefig(output_pdf)  # Save as PDF
            plt.close()  # Close figure to free memory
            return

        out_prefix = "converged"
        file_out = out_prefix + ".dat"
        plot_out = out_prefix + ".pdf"

        to_tsv(
            file_out,
            "\t".join(self.params),
            self.grepper.criteria.replace(" ", "_"),
            "w",
        )

        #Loop over calculations
        converged_x = []
        converged_y = []

        for each_calc, vals in zip(self.calcs, self.vals):
            each_calc.run(command, prepend)

            # grep deta, save data, and plot
            calc_x, calc_y = vals, self.grepper.fetch(each_calc.file_out)
            converged_y.append(calc_y)
            converged_x.append(calc_x)

            to_tsv(file_out, calc_x, calc_y, mode="a")
            plot_tsv(file_out, plot_out)

            #check convergence and possibly break loop
            if check_conv:
                conv_res = self.find_convergence(file_out, threshold = conv_threshold)
                if conv_res: 
                    self.converged = conv_res
                    print(f"Convergence achieved at {','.join(self.params)} = {conv_res}")
                    if break_on_conv: 
                        print("Breaking loop")
                        return self.converged;

        return 



    def find_convergence(self, filename, threshold):
        """
        Reads a TSV file and finds the first x value where y is within the convergence threshold.
        
        Parameters:
        - filename (str): Path to the TSV file.
        - threshold (float): Convergence criterion for y.
        
        Returns:
        - float or None: The x value where convergence is first met, or None if not found.
        """

        data = np.array(pd.read_csv (filename, sep = '\t'))

        if data.shape[1] == 2:  # Case: Two columns (x, y)
            y_values = data[:, 1]
            for i in range(1, len(y_values)):  # Start from the second row
                if abs(y_values[i] - y_values[i - 1]) <= threshold:
                    return data[i, 0]  # Return x where convergence is met

        elif data.shape[1] == 3:  # Case: Three columns (x, category, y)
            category_data = {}

            for x, category, y in data:
                category = int(category)  # Ensure categories are integers
                if category not in category_data:
                    category_data[category] = []
                category_data[category].append((x, y))

            category_convergence = {}

            for category, points in category_data.items():
                points.sort()  # Ensure sorted by x
                for i in range(1, len(points)):
                    if abs(points[i][1] - points[i - 1][1]) <= threshold:
                        category_convergence[category] = points[i][0]  # Store first x where convergence is met
                        break  # Stop checking once we find the first convergence

            return category_convergence if category_convergence else None  # Return dict for categories
        return None  # Return None if no convergence found

    def check_convergence(
        self,
        tolerance=0.00001,
        relative=True,
        check_convergence=True,
        break_on_converge=True,
    ):
        """
        Check if convergence has been achieved.
        """

        # Check if convergence has been achieved and return converged value
        converged, self.converged_val = self.check_convergence(
            convergence_params, tolerance, relative
        )
        if converged:
            logging.info(f"Conv achieved {self.converged_val=}")
            if break_on_converge:  # break loop if convergence achieved?
                return self.converged_val

        return

    @staticmethod
    def check_convergence(values, tolerance=0.01, relative=True):
        """
        Check if the successive values in the list have converged based on relative error.

        Args:
            values (list): A list of numerical values.
            tolerance (float): The convergence tolerance in percentage (default is 0.01%).

        Returns:
            converged (bool): True if converged, False otherwise.
            value (convergence value): np.nan for not converged
        """
        converged = False
        value = np.nan
        if len(values) > 1:

            #          for i in range(1, len(values)):
            # Calculate the relative error between successive values
            relative_error = abs(values[-1] - values[-2]) / abs(values[-2]) * 100

            # Check if the relative error is within the tolerance
            if relative_error < tolerance:
                print("Convergence achieved")
                converged = True

        return converged, value

    @property
    def converged_val(self):
        """Getter for the converged_val attribute"""
        return self._converged_val

    @converged_val.setter
    def converged_val(self, value: float):
        """Setter for the converged_val attribute to enforce a condition"""
        self._converged_val = value

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        """
        Returns next base calculation
        """
        if self.index >= len(self.calcs):
            raise StopIteration
        next_calc = self.calcs[self.index]
        self.index += 1
        return next_calc

    def __len__(self):
        return len(self.calcs)

    def __str__(self):
        return "Convergence calculation QE"


class BaseNormalCalculation:
    """
    Args:
    calc_type = 'normal', 'convergence'
    suite: 'QE', 'Yambo'
    code:   'pw.x'
    """

    def __init__(self, template=None, code="", update={}, files=None):
        """
        Args:
          template (dict|str|path): Read template either from a dictionary or a json file path.
          code (str): suite and code to use. 'qe/pw.x'
          files: Names to use for files.
                  If None given: Read from template['prefix']
                  If str given: Use that (append '.in' and '.out' for input and output
                  If list given: Use the first two as file names.
        """

        self.suite = code.split("/")[0]
        self.code = code.split("/")[1]
        self.template = self.read_template(template, update)

        self.file_in, self.file_out = self.figure_file_names(files, template)
        return

    def read_template(self, template, update):
        """
        Read template from file depending on code.
        """
        if not isinstance(template, dict):
            # if extension is .json
            if self.suite == "qe":
                template = QEFileHandler.from_flat_JSON(template)
            # If extension is .in
        template.update({k: update[k] for k in update.keys()})

        return template

    def figure_file_names(self, files=None, template=None):
        """
        Figures out file names to use.
        Args:
            files (str) | (list): If str. Use {files}.in and {files}.out. If list then use the first two as file names.

        Returns:
            file names.
        """

        if isinstance(files, str):
            file_in = files + ".in"
            file_out = files + ".out"
        elif isinstance(files, list):
            file_in = files[0]
            file_out = files[1]
        return file_in, file_out

    def run(self, command="", prepend=""):
        """
        Execute command
        """
        if command == "":
            command = f"{prepend} {self.code} < {self.file_in} > {self.file_out}"
        Basher.runcommand(command)

        return


class Grepper:
    """
    Class for handling reading and writing. Every code should implement its own grepper e.g. QEGrepper.
    """

    def __init__(self, criteria=""):
        """
        Args:
            grep (str): a string for the thing which is to be grepped. e.g. 'total energy'. Each code specific grepper will have its own methods for processing any possible `grep`.
        """
        self.criteria = criteria
        return

    def extract_number(self, file_path, starts_with="!") -> float:
        """
        Finds the line starting with '!' and extracts the number from it.

        Args:
            file_path (str): Path to the file to be read.

        Returns:
            float: The number found in the comment line, or None if not found.
        """
        with open(file_path, "r") as file:
            for line in file:
                if line.lstrip().startswith(starts_with):
                    # Using regular expression to find numbers (integers or floating-point)
                    match = re.search(r"!.*\s*(-?\d+(\.\d+)?)", line)
                    if match:
                        return float(match.group(1))  # Return the number as a float
        return None  # If no line starting with '!' is found
