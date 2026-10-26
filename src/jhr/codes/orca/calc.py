from io import StringIO
from pathlib import Path
import shutil
import subprocess

from pathlib import Path
from jhr.codes.orca.validator import ORCAValidator

from ase.io.orca import write_orca
from ase import Atoms
from ase.io import read

class OrcaIO:
    """Construct, write, and organize ORCA input files."""

    def __init__(self, config=None, root="calculations"):
        # self.config = {**CONFIG, **(config or {})}
        self.config = config
        self.root = Path(root)

    # ========================================================
    # ORCA input construction
    # ========================================================

    def make_orcasimpleinput(self, state=None):
        """
        Construct the ORCA simple-input keyword string.

        Parameters
        ----------
        state : dict or None, optional
            Calculation-specific configuration.

            Values in state take precedence over instance defaults.

        Returns
        -------
        str
            Space-separated ORCA simple-input keywords.

        Raises
        ------
        ValueError
            If the method or basis set is not provided by either
            the state or the instance configuration.
        """
        state = state or {}
        config = self.config or {}

        method = state.get("method")
        if method is None:
            method = config.get("method")

        basis = state.get("basis")
        if basis is None:
            basis = config.get("basis")

        if not method or not basis:
            raise ValueError(
                "Both method and basis must be specified."
            )

        keywords = state.get("keywords")

        if keywords is None:
            keywords = [
                config[key]
                for key in ("dispersion", "scf", "optimization")
                if config.get(key)
            ]

        return " ".join([method, basis, *keywords])

    def make_orcablocks(self, state, include_resources=True):
        """
        Construct the native ORCA input blocks.

        Parameters
        ----------
        state : dict
            Configuration containing optional native ORCA blocks.

            Blocks are represented by nested dictionaries. Each outer
            key identifies an ORCA block, while its corresponding value
            contains the options belonging to that block.

        include_resources : bool, optional
            Whether to include the parallel execution and memory settings
            from ``self.config``.

            The default is True to preserve the existing behavior of
            standalone ORCA input generation.

            When False, only scientifically specified ORCA blocks are
            generated. This is appropriate when resource configuration
            will be supplied separately by an execution system.

        Returns
        -------
        str
            Formatted ORCA blocks suitable for inclusion in an input file.

        Notes
        -----
        Resource settings such as ``%pal`` and ``%maxcore`` are execution
        parameters rather than scientific parameters.

        Excluding them allows the execution layer to determine resource
        allocation independently of the scientific specification.
        """
        blocks = []

        if include_resources:
            blocks.extend([
                f"%pal nprocs {self.config['nprocs']} end",
                f"%maxcore {self.config['maxcore']}",
            ])

        for block_name, options in state.get("blocks", {}).items():
            lines = [f"%{block_name}"]

            for key, value in options.items():
                lines.append(f"    {key} {value}")

            lines.append("end")
            blocks.append("\n".join(lines))

        return "\n\n".join(blocks)
    
    def render_orca_input(
        self,
        atoms,
        state,
        include_resources=False,
    ):
        """
        Generate a conventional ORCA input entirely in memory.

        Parameters
        ----------
        atoms : ase.Atoms
            Atomic structure used as the initial molecular geometry.

            Atomic positions are interpreted in Angstrom, following
            ASE conventions.

        state : dict
            ORCA calculation configuration.

            Supported keys include:

            - ``method``: Electronic-structure method.
            - ``basis``: Basis set.
            - ``charge``: Total molecular charge.
            - ``mult``: Spin multiplicity.
            - ``keywords``: Additional ORCA simple-input keywords.
            - ``blocks``: Native ORCA input blocks.

        include_resources : bool, optional
            Whether resource configuration should be included in the
            generated input.

            The default is False because execution resources should
            ordinarily be controlled by the execution layer.

        Returns
        -------
        str
            Complete ORCA input file contents.

        Raises
        ------
        TypeError
            If atoms is not an ASE Atoms object.

        Notes
        -----
        This method performs no filesystem operations and does not
        execute ORCA.

        The returned string can be written to a file, inspected,
        validated, or passed to an automated execution framework.

        Examples
        --------
        >>> from ase import Atoms
        >>> atoms = Atoms("H2", positions=[
        ...     [0, 0, 0],
        ...     [0, 0, 0.74],
        ... ])
        >>> text = io.render_orca_input(atoms, state)
        """
        if not isinstance(atoms, Atoms):
            raise TypeError("atoms must be an ASE Atoms object.")

        params = {
            "orcasimpleinput": self.make_orcasimpleinput(state),
            "orcablocks": self.make_orcablocks(
                state,
                include_resources=include_resources,
            ),
            "charge": state.get("charge", 0),
            "mult": state.get("mult", 1),
        }

        buffer = StringIO()
        write_orca(buffer, atoms, params)

        return buffer.getvalue()

    def make_compound_input(self, atoms, steps):
        """Generate an ORCA Compound input string."""
        lines = [
            "# Generated by OrcaIO",
            "",
            "%pal",
            f"    nprocs {self.config['nprocs']}",
            "end",
            f"%maxcore {self.config['maxcore']}",
            "",
            "%Compound",
        ]

        for index, step in enumerate(steps):
            lines.extend([
                "",
                f"    # Step {index + 1}: {step['name']}",
                "    NewStep",
                (
                    f"        ! {step.get('method', self.config['method'])} "
                    f"{step.get('basis', self.config['basis'])} "
                    + " ".join(
                        step.get(
                            "keywords",
                            [
                                self.config["dispersion"],
                                self.config["scf"],
                            ],
                        )
                    )
                ),
            ])

            # Only the first step defines the initial geometry.
            if index == 0:
                lines.append(
                    f"        * xyz {step.get('charge', 0)} "
                    f"{step.get('mult', 1)}"
                )

                for symbol, position in zip(
                    atoms.get_chemical_symbols(),
                    atoms.get_positions(),
                ):
                    x, y, z = position
                    lines.append(
                        f"            {symbol:2s} "
                        f"{x: .10f} {y: .10f} {z: .10f}"
                    )

                lines.append("        *")

            # Optional geometry reset to an earlier Compound step.
            if "read_geom" in step:
                # Note: Read_Geom must be positioned before NewStep
                # in the final Compound input. See note below.

                pass

            for block_name, options in step.get("blocks", {}).items():
                lines.append(f"        %{block_name}")

                for key, value in options.items():
                    lines.append(f"            {key} {value}")

                lines.append("        end")

            lines.append("    StepEnd")

        lines.extend(["End", ""])
        return "\n".join(lines)

    # ========================================================
    # File writing
    # ========================================================

    def write_orca_input(self, filename, atoms, state):
        """Write a conventional, standalone ORCA input."""
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        params = {
            "orcasimpleinput": self.make_orcasimpleinput(state),
            "orcablocks": self.make_orcablocks(state),
            "charge": state.get("charge", 0),
            "mult": state.get("mult", 1),
        }

        with filename.open("w") as fd:
            write_orca(fd, atoms, params)

        print(f"Created: {filename}")
        return filename

    def write_compound_input(self, filename, atoms, steps):
        """Write an ORCA Compound input."""
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        filename.write_text(
            self.make_compound_input(atoms, steps)
        )

        print(f"Created: {filename}")
        return filename

    # ========================================================
    # Calculation organization
    # ========================================================

    def prepare_calculation(self, atoms, molecule_id, inputs):
        """
        Create separate input files for the supplied electronic states.

        Parameters
        ----------
        atoms : ase.Atoms
            Geometry used to initialize the calculations.
        molecule_id : str
            Molecule identifier.
        inputs : dict
            Mapping of state names to ORCA state configurations.
        """
        created_files = {}
        molecule_dir = self.root / molecule_id

        for state_name, state in inputs.items():
            state_dir = molecule_dir / state_name
            input_file = state_dir / "opt.inp"

            self.write_orca_input(input_file, atoms, state)
            created_files[state_name] = input_file

        return created_files

    def prepare_compound_calculation(
        self, atoms, molecule_id, calculation_name, steps, input_file = "calc.inp"
    ):
        """Create a Compound input in its own calculation directory."""
        calculation_dir = self.root / molecule_id / calculation_name
        input_file = calculation_dir / input_file

        return self.write_compound_input(
            input_file,
            atoms,
            steps,
        )

class ORCARunner:
    """Execute ORCA calculations with standardized output filenames."""

    def __init__(self, executable="orca"):
        self.executable = shutil.which(executable)
        if self.executable is None:
            raise FileNotFoundError(
                f"ORCA executable not found: {executable}"
            )

    def run(self, input_file, timeout=None):
        input_file = Path(input_file).resolve()

        if not input_file.is_file():
            raise FileNotFoundError(input_file)

        output_file = input_file.with_suffix(".out")
        error_file = input_file.with_suffix(".err")

        with output_file.open("w") as out, error_file.open("w") as err:
            result = subprocess.run(
                [self.executable, input_file.name],
                cwd=input_file.parent,
                stdout=out,
                stderr=err,
                timeout=timeout,
                check=False,
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"ORCA failed with exit code {result.returncode}. "
                f"See {output_file} and {error_file}"
            )

        return output_file
