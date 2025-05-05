import json
import os
import re
import tempfile
from pathlib import Path

import sys
import numpy as np

import pandas as pd
from ase import Atoms
from ase.io.espresso import read_espresso_in

from jhr._helpers import Constants, Dicter
from jhr.io.base import FileHandler


class QEFileHandler(FileHandler):
    # Card list in different QE input files.
    cards = {
        "pw.x": ["k_points", "atomic_positions", "atomic_species"],
        "ph.x": ["qPointsSpecs"],
    }

    # convert to list
    card_list = []
    for k, v in cards.items():
        card_list.extend(v)

    def __init__(self, template):
        """
        Args:
            template (str|path): File path with template. Could be json or qe input.
        """

        filepath = Path(template)
        name, ext = filepath.stem, filepath.suffix

        if ext == ".in":
            new_file = filepath.with_suffix(".json")
            self.qeinput2json(file_in=template, file_out=new_file, update={})

        self.contents = self.from_flat_JSON(new_file)

        return

    @classmethod
    def from_scfin(cls):

        return

    def additional_cards_splitter(self, additional_cards):
        keywords = ["ATOMIC_SPECIES", "ATOMIC_POSITIONS", "K_POINTS"]
        cards_dict = self.fortran_card_splitter(additional_cards, keywords)

        for k in cards_dict.keys():
            # parse each key.
            if "K_POINTS" in k.upper():
                #     print(cards_dict[k][0].split())
                pass
        return cards_dict
    
    @classmethod
    def from_flat_JSON(cls, file):
        """
        Create ase.Atoms object from a json file and a dictionary of settings. The dict is used to create a template which may be used to perform convergence.

        Args: json file with structure.

              {"template":
                {"calculation": "scf",
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
                  "pseudopotentials": {"Cs": "C.pbe-n-rrkjus_psl.0.1.UPF",
                                    "Pb": "C.pbe-n-rrkjus_psl.0.1.UPF",
                                    "I": "C.pbe-n-rrkjus_psl.0.1.UPF"},
                  "kpts": [2,2,2],
                  "cell": [1, 1, 1],
                  "pbc": [1, 1, 1],
                  "positions": [[0.5, 0.5, 0.5],
                            [0,   0,  0],
                            [0,   0,  0.5]],
                  "crystal_coordinates": true
              }

        """
        # Create input files
        with open(file) as json_file:
            matdict = json.load(json_file)

        return matdict

    def card_parser(self, cards_dict, card_id="k_points"):
        """
        For parsing additional_cards.
        Args:
            card_id
        Returns:
            Dictionary with two keys 'setting' and 'values'

        Example:
            For:
            k_points automatic
            4 4 4 0 0 0

            Returns:
            {'setting': automatic, 'values': [4,4,4,0,0,0]


        """

        def splitter(row, card_id="k_points"):
            """
            Split a row of additional_cards.
            """

            def convert_value(value):
                """
                Convert value to float, int or return as string
                """
                try:
                    if "." in value:  # Check if it's a float
                        return float(value)
                    return int(value)  # Otherwise, try converting to int
                except ValueError:
                    return value  # If conversion fails, return as string

            return [convert_value(v) for v in row.split()]

        # ------------------------------------------------

        # Find the key with k_points in it.
        for key in cards_dict.keys():
            if key.lower().startswith(card_id):
                parts = key.split()  # Split at the first underscore
                setting = parts[1] if len(parts) > 1 else ""
                break

        # Extract values and return dict
        values = cards_dict[key]
        splitted_values = []

        for val in values:
            split_val = splitter(val, card_id)
            splitted_values.append(split_val)

        return {card_id: {"setting": setting, "values": splitted_values}}

    def card2dict(self, card_dict):
        """
        Args:
          card_dict (dict): Dict with two keys 'settings' and 'values'
        """

        to_ase = {}

        for key in card_dict.keys():
            values = card_dict[key]["values"]
            setting = card_dict[key]["setting"]

            if key == "k_points":
                to_ase["kpts"] = values[0]

            elif key == "atomic_positions":
                to_ase["positions"], to_ase["atoms"] = [], ""
                for val in values:
                    to_ase["positions"].append(val[1:])
                    to_ase["atoms"] += val[0]

            elif key == "atomic_species":
                to_ase["pseudopotentials"] = {val[0]: val[2] for val in values}

        return to_ase

    def qeinput2json(self, file_in="scf.in", file_out="scf.json", update={}):
        """
        Convert qe input file to json.

        file_in: qe input file
        file_out: json output file
        update (dict): any other updates that you want to write to json. e.g. {'pbc':[1,1,1]}
        """
        # Read input file
        input_data, additional_cards = self.read_fortran_namelists(file_in)

        # Split cards according to QE namelists and cards.
        cards_dict = self.additional_cards_splitter(additional_cards)
        flattened_dict = Dicter.flatten_dict(input_data)

        # Parse cards into dictionaries.
        parsed = {}
        for k in self.card_list:
            try:
                parsed.update(self.card_parser(cards_dict, card_id=k))
            except:
                pass

        # Convert dict to dict suitable for json input file in JHR.
        ase_dict = self.card2dict(parsed)

        flattened_dict.update(ase_dict)
        flattened_dict.update(update)

        # Write to json.
        with open(file_out, "w") as fp:
            json.dump(flattened_dict, fp)

        return


# =================Modifiers==================
from jhr.io.modifiers import Modifier


class QEModifier(Modifier):
    """
    Class for modifiying espresso input files.
    """

    @staticmethod
    def remove_ibrav(lines: list):
        """
        Removes ibrav from lines read from a file.
        """
        new_lines = []
        for line in lines:
            if "ibrav" not in line.lower():
                new_lines.append(line)  # Keep the lines that don't contain 'ibrav'
        return new_lines

    @staticmethod
    def modify_atomic_positions(lines, atomic_positions: str = ""):
        """
        Modify the ATOMIC_POSITIONS line to 'ATOMIC POSITIONS crystal_sg' e.g.
        or to a user-specified atomic_positions string.
        """
        new_lines = []
        for line in lines:
            # Modify the ATOMIC_POSITIONS line if the atomic_positions string is provided
            if "atomic_positions" in line.lower() and len(atomic_positions) > 0:
                new_lines.append(f"ATOMIC_POSITIONS {atomic_positions}\n")
            else:
                new_lines.append(line)

        return new_lines

    @staticmethod
    def remove_cell_parameters(lines):
        """
        Remove the line containing 'CELL_PARAMETERS' and the following 3 lines.
        """
        new_lines = []
        skip_next_lines = 0  # Flag to keep track of how many lines to skip
        for line in lines:
            # Check for 'CELL_PARAMETERS' line and set skip_next_lines
            if "cell_parameters" in line.lower():
                skip_next_lines = 3  # Skip the next 3 lines after 'CELL_PARAMETERS'
                continue  # Skip the 'CELL_PARAMETERS' line itself
            # Skip the next lines if flagged
            if skip_next_lines > 0:
                skip_next_lines -= 1
            else:
                new_lines.append(line)  # Keep this line if we are not skipping it

        return new_lines

    @staticmethod
    def remove_ibrav_and_read(input_filename):
        """
        Sets ibrav to 0 in a temp file and reads because ase does not read qe input file if ibrav != 0.

        Returns;
          atoms
          parameters
        """
        # Read the original input file
        with open(input_filename, "r") as f:
            lines = f.readlines()

        # Modify lines: set any ibrav parameter to 0
        new_lines = []
        for line in lines:
            if "ibrav" in line.lower():
                # Use a regular expression to replace the value after 'ibrav ='
                line = re.sub(r"(ibrav\s*=\s*)\S+", r"\1 0", line, flags=re.IGNORECASE)
            new_lines.append(line)

        # Write modified content to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".in") as tmp:
            temp_filename = tmp.name
            tmp.writelines(new_lines)

        # Read the temporary file using ASE's read_espresso_in function
        atoms, parameters = read_espresso_in(temp_filename)

        # Delete the temporary file
        os.remove(temp_filename)

        return atoms, parameters


class QEOutParser:
    def __init__(self, code, file = None):
        """
        Determine which parser to use.
        """
        self.file = file
        if code == "pw.x":
            self.parser = PWParse(self.file)
        return


class PWParse:
    """
    From: https://blog.levilentz.com/parse-quantum-espresso-output-file/

    Takes a pw.x output file and reads all the relevant values.

    Example:
      test = PWParse()
      test.Process("vc.out")

      print(test.to_JSON())


    """


    def __init__(self, file = None):
        self.file = file
        self.BOHRtoA = Constants.BOHRtoA
        self.RYtoeV = Constants.RYtoeV
#        self.program_version = ""
#        self.volume = 0.0
#        self.alat = 0.0
#        self.natoms = 0
#        self.nat = 0
#        self.nelect = 0
#        self.Ecut = 0.0
#        self.RhoCut = 0.0
#        self.Econv = 0.0
#        self.beta = 0.0
#        self.Exch = ""
#        self.energy = 0.0
#        self.natoms = 0
#        self.bandgap = 0.0
#        self.bands = 0
#        self.lattice = {"a": np.zeros(3), "b": np.zeros(3), "c": np.zeros(3)}
#        self.atoms = []
#        self.norms = {"a": 0.0, "b": 0.0, "c": 0.0}
#        self.angles = {"alpha": 0.0, "beta": 0.0, "gamma": 0.0}
#        self.kpts = 0
#        self.bnddiagram = np.zeros(0)
#        self.FermiTest = False
#        self.Fermi = 0.0
    def Process(self, file_path = None):
        """
        Parses a passed file for standard parsing. Uses self.file if no file is passed. 
        """
        if file_path is None: file_path = self.file

        self.data = pd.DataFrame(columns=["value", "unit", "description"])
        self.lattice = {"a": [0, 0, 0], "b": [0, 0, 0], "c": [0, 0, 0]}
        self.norms = {}
        self.angles = {}
        self.atoms = []

        f = open(file_path, "r")

        for linenum, i in enumerate(f):
            if linenum < 1000:
                if "number of k points=" in i:
                    val = int(i.split()[4])
                    self.data.loc["kpoints"] = [val, "unitless", "Number of k-points in the Brillouin zone"]
                    continue
                if "Program PWSCF" in i:
                    val = i.split()[2]
                    self.data.loc["program_version"] = [val, "N/A", "Quantum ESPRESSO version"]
                    continue
                if "lattice parameter (alat)" in i:
                    val = float(i.split()[4]) * self.BOHRtoA
                    self.data.loc["alat"] = [val, "Å", "Lattice parameter (alat)"]
                    continue
                if "number of Kohn-Sham states" in i:
                    val = int(i.split()[4])
                    self.data.loc["bands"] = [val, "unitless", "Number of Kohn-Sham states (bands)"]
                    continue
                if "unit-cell volume" in i and "new" not in i:
                    val = float(i.split()[3]) * (self.BOHRtoA**3.0)
                    self.data.loc["volume"] = [val, "Å³", "Unit cell volume"]
                    continue
                if "number of atoms/cell" in i:
                    val = int(i.split()[4])
                    self.data.loc["natoms"] = [val, "unitless", "Number of atoms per unit cell"]
                    continue
                if "number of atomic types" in i:
                    val = int(i.split()[5])
                    self.data.loc["natypes"] = [val, "unitless", "Number of atomic types"]
                    continue
                if "number of electrons" in i:
                    val = float(i.split()[4])
                    self.data.loc["nelectrons"] = [val, "unitless", "Number of electrons"]
                    continue
                if "kinetic-energy cutoff" in i:
                    val = float(i.split()[3]) * self.RYtoeV
                    self.data.loc["ecut"] = [val, "eV", "Kinetic energy cutoff"]
                    continue
                if "charge density cutoff" in i:
                    val = float(i.split()[4]) * self.RYtoeV
                    self.data.loc["rhocut"] = [val, "eV", "Charge density cutoff"]
                    continue
                if "convergence threshold" in i:
                    val = float(i.split()[4])
                    self.data.loc["econvergence"] = [val, "unitless", "Electronic convergence threshold"]
                    continue
                if "mixing beta" in i:
                    val = float(i.split()[3])
                    self.data.loc["mixing_beta"] = [val, "unitless", "Mixing beta parameter"]
                    continue
                if "Exchange-correlation" in i:
                    val = i.split()[1]
                    self.data.loc["xc_functional"] = [val, "N/A", "Exchange-correlation functional"]
                    continue

                if "a(1) =" in i:
                    tmp = i.split()
                    val = [float(tmp[j + 3]) for j in range(3)]
                    self.data.loc["a_vector"] = [val, "alat units", "Lattice vector a"]
                    continue
                if "a(2) =" in i:
                    tmp = i.split()
                    val = [float(tmp[j + 3]) for j in range(3)]
                    self.data.loc["b_vector"] = [val, "alat units", "Lattice vector b"]
                    continue
                if "a(3) =" in i:
                    tmp = i.split()
                    val = [float(tmp[j + 3]) for j in range(3)]
                    self.data.loc["c_vector"] = [val, "alat units", "Lattice vector c"]
                    continue
                if "site n.     atom                  positions (alat units)" in i:
                    atoms = []
                    for j in range(self.data.loc["natoms", "value"]):
                        line = next(f).split()
                        atoms.append(
                            [
                                line[1],
                                float(line[6]) * self.data.loc["alat", "value"],
                                float(line[7]) * self.data.loc["alat", "value"],
                                float(line[8]) * self.data.loc["alat", "value"],
                            ]
                        )
                    self.data.loc["atomic_positions"] = [atoms, "Å", "List of atomic species and positions"]
                    continue
            if "!" in i:
                val = float(i.split()[4]) * self.RYtoeV
                self.data.loc["total_energy"] = [val, "eV", "Total energy"]
                continue
            if "new unit-cell volume" in i:
                val = float(i.split()[4]) * (self.BOHRtoA**3)
                self.data.loc["new_volume"] = [val, "Å³", "Updated unit cell volume"]
                continue
            if "Begin final coordinates" in i:
                while True:
                    line = next(f)
                    if "End final coordinates" in line:
                        break
                    if "CELL_PARAMETERS" in line:
                        self.alat = float(line.replace(")", "").split()[2]) * self.BOHRtoA
                        for j, vec in zip(["a", "b", "c"], ["a_vector_final", "b_vector_final", "c_vector_final"]):
                            line = next(f)
                            tmp = [self.alat * float(x) for x in line.split()]
                            self.lattice[j] = tmp
                            self.data.loc[vec] = [tmp, "Å", f"Final lattice vector {j}"]
                    if "ATOMIC_POSITIONS" in line:
                        positions = []
                        for j in range(self.data.loc['natoms', 'value']):
                            line = next(f).split()
                            pos = [
                                line[0],
                                float(line[1]),
                                float(line[2]),
                                float(line[3]),
                            ]
                            positions.append(pos)
                        self.data.loc["final_atomic_positions"] = [positions, "Å", "Final atomic positions"]
            if "End of self-consistent calculation" in i:
                bands = int(self.data.loc["bands","value"])
                kpts = int(self.data.loc["kpoints","value"])
                #numlines = int(np.floor(self.bands / 8.0)) + 1
                numlines = int(np.floor(bands / 8.0)) + 1

                bnddiagram = np.zeros((kpts, bands),dtype=float)
                counter = 0
                while counter < kpts:
                    line = next(f)
                    if "k =" in line:
                        line = next(f)
                        idx = 0
                        for _ in range(numlines):
                            line = next(f).split()
                            for val in line:
                                bnddiagram[counter][idx] = float(val)
                                idx += 1
                        counter += 1
                self.data.loc["bnddiagram"] = [bnddiagram.tolist(), "N/A", "Band diagram"]
                continue
            if "highest occupied, lowest unoccupied level (ev)" in i:
                val = float(i.split()[7]) - float(i.split()[6])
                self.data.loc["bandgap_direct"] = [val, "eV", "Bandgap from DOS"]
                continue
            if "the Fermi energy is" in i:
                val = float(i.split()[4])
                self.data.loc["Fermi_energy"] = [val, "eV", "Fermi level"]
                continue

        f.close()
        return self.data
    def lattice_vectors(self):
        a_v = self.data.loc['a_vector'][0]
        b_v =  self.data.loc['b_vector'][0]
        c_v =  self.data.loc['c_vector'][0]
        alat = self.data.loc['alat'][0]

        if {a_v,b_v,c_v} == {[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]}:
            vals = {'cell': [1,1,1], 'a': alat}

        return vals
    def atomic_positions(self):
        atm = [at[0] for at in self.data.loc['atomic_positions'][0]]
        atoms = ''.join(atm)

        positions = [at[1:] for at in self.data.loc['atomic_positions'][0]]

        return {'atoms': atoms, 'positions': positions}

    def band_occupancy(self, file=None):
        def _extract_occupancy(file, keywords, num_KS_states):
            with open(file, 'r') as file:
                text = file.read()

            occupancy_dict={}

            for keyword in keywords:
                parts = text.split(keyword)
                print(f"Found {len(parts)-1} occurrences of {keyword}")
                numbers = []
                for part in parts[1:]:
                    lines = part.splitlines()

                    values = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        for word in line.split():
                            try:
                                values.append(float(word))
                                if len(values) == num_KS_states:
                                    break
                            except ValueError:
                                continue
                        if len(values) == num_KS_states:
                            break
                    numbers.append(np.array(values))
                    occupancy_dict[keyword] = np.array(numbers)

            return occupancy_dict
        def _find_kpoints(lines):
            """
            Extract kpoints from file
            """

            kpoints = []

            for line in lines:
                if 'k =' in line and 'wk =' not in line:
                    # Extract the first three floats after "k ="
                    floats = re.findall(r'[-+]?\d*\.\d+|\d+', line)
                    kpoints.append([float(f) for f in floats[:3]])
            k_array = np.array(kpoints)   
            return k_array

        if file is None: file = self.file

        num_KS_states = self.data.loc['bands'][0]

        keywords = ['bands (ev)', 'occupation numbers']
        occupancy_dict = _extract_occupancy(file, keywords, num_KS_states)
        
        occupancy_dict['bands_array'] = occupancy_dict.pop('bands (ev)')
        occupancy_dict['occupancy_array'] = occupancy_dict.pop('occupation numbers')

        with open(file, 'r') as f:
            lines = f.readlines()
            occupancy_dict['kpoint_array'] = _find_kpoints(lines)
 

        return occupancy_dict

            


    
