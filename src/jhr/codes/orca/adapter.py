"""
Adapter between jhr calculation specifications and ORCA.

This module translates code-independent scientific calculation
specifications into native ORCA input files.

The OrcaAdapter uses the existing OrcaIO implementation for input
construction. It does not execute ORCA, manage working directories,
or allocate computational resources.

The adapter follows the CodeAdapter interface defined in jhr.core.

Supported tasks
---------------
single_point
    Perform a single-point electronic-structure calculation.

optimization
    Optimize the molecular geometry.

excited_states
    Calculate vertical excited states using ORCA's TDDFT facilities.

Notes
-----
This initial implementation focuses on input preparation.

Output parsing and scientific validation will be connected to the
existing ORCAValidator in the next development stage.

No execution resources are included in the generated input.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from jhr.codes.orca.parser import ORCAParser
from jhr.codes.orca.validator import ORCAValidator

from ase import Atoms

from jhr.core.adapter import (
    CodeAdapter,
    PreparedCalculation,
)

from jhr.core.calculation import (
    CalculationSpec,
    CalculationResult,
)

from jhr.codes.orca.calc import OrcaIO


class OrcaAdapter(CodeAdapter):
    """
    Translate scientific calculation specifications into ORCA inputs.

    OrcaAdapter provides a code-specific implementation of the
    preparation interface defined by CodeAdapter.

    Parameters
    ----------
    io : OrcaIO, optional
        ORCA input generator.

        If omitted, an internal OrcaIO instance is created.
        Calculation-specific methods and basis sets are supplied
        by CalculationSpec rather than by global OrcaIO defaults.

    Attributes
    ----------
    code : str
        Scientific code identifier, equal to ``"orca"``.

    Notes
    -----
    The adapter is responsible for translating generic scientific
    operations into ORCA-native instructions.

    It does not manage parallel execution, memory allocation,
    working directories, or scheduler configuration.

    This separation allows the same adapter to be used for
    standalone Python workflows and AiiDA CalcJobs.

    Examples
    --------
    >>> adapter = OrcaAdapter()
    >>> prepared = adapter.prepare(spec, atoms)
    >>> print(prepared.files[prepared.input_filename])
    """

    code = "orca"

    TASK_KEYWORDS = {
        "single_point": "SP",
        "optimization": "Opt",
        "excited_states": "SP",
    }

    SUPPORTED_PARAMETERS = {
        "method",
        "basis",
        "charge",
        "multiplicity",
    }

    SUPPORTED_OPTIONS = {
        "dispersion",
        "scf",
        "keywords",
        "blocks",
        "nroots",
        "tda",
    }

    def __init__(self, io: OrcaIO | None = None):
        """
        Initialize the ORCA adapter.

        Parameters
        ----------
        io : OrcaIO or None, optional
            Existing ORCA input generator to reuse.

        Raises
        ------
        TypeError
            If io is not an OrcaIO instance or None.
        """
        if io is not None and not isinstance(io, OrcaIO):
            raise TypeError("io must be an OrcaIO instance.")

        self.io = io or OrcaIO(config={})

    def validate_spec(
        self,
        spec: CalculationSpec,
    ) -> None:
        """
        Validate a scientific specification for ORCA.

        Parameters
        ----------
        spec : CalculationSpec
            Scientific operation to validate.

        Returns
        -------
        None
            Returns normally when the specification is supported.

        Raises
        ------
        TypeError
            If spec is not a CalculationSpec.

        ValueError
            If the code, task, or scientific settings are unsupported.

        Notes
        -----
        This method validates the adapter's supported vocabulary.

        It does not attempt to establish whether every possible
        combination of ORCA method, basis set, and options is
        physically meaningful or supported by a particular ORCA version.
        """
        if not isinstance(spec, CalculationSpec):
            raise TypeError(
                "spec must be a CalculationSpec."
            )

        if spec.code != self.code:
            raise ValueError(
                f"OrcaAdapter cannot handle code {spec.code!r}."
            )

        if spec.task not in self.TASK_KEYWORDS:
            raise ValueError(
                f"Unsupported ORCA task: {spec.task!r}."
            )

        unknown_parameters = (
            set(spec.parameters) - self.SUPPORTED_PARAMETERS
        )

        if unknown_parameters:
            raise ValueError(
                "Unsupported scientific parameters: "
                f"{sorted(unknown_parameters)}"
            )

        unknown_options = (
            set(spec.code_options) - self.SUPPORTED_OPTIONS
        )

        if unknown_options:
            raise ValueError(
                "Unsupported ORCA options: "
                f"{sorted(unknown_options)}"
            )

        for required in ("method", "basis"):
            value = spec.parameters.get(required)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"ORCA requires a non-empty {required!r}."
                )

        charge = spec.parameters.get("charge", 0)
        multiplicity = spec.parameters.get("multiplicity", 1)

        if type(charge) is not int:
            raise ValueError("charge must be an integer.")

        if type(multiplicity) is not int or multiplicity < 1:
            raise ValueError(
                "multiplicity must be a positive integer."
            )

        if "keywords" in spec.code_options:
            keywords = spec.code_options["keywords"]

            if not isinstance(keywords, tuple):
                raise ValueError("keywords must be a list.")

            if not all(isinstance(k, str) for k in keywords):
                raise ValueError(
                    "Every ORCA keyword must be a string."
                )

        if "blocks" in spec.code_options:
            blocks = spec.code_options["blocks"]

            if not isinstance(blocks, Mapping):
                raise ValueError("blocks must be a dictionary.")

            for name, options in blocks.items():
                if not isinstance(options, Mapping):
                    raise ValueError(
                        f"ORCA block {name!r} must be a dictionary."
                    )

        if spec.task == "excited_states":
            nroots = spec.code_options.get("nroots", 5)

            if type(nroots) is not int or nroots < 1:
                raise ValueError(
                    "nroots must be a positive integer."
                )

            tda = spec.code_options.get("tda", False)

            if type(tda) is not bool:
                raise ValueError("tda must be a boolean.")

        elif any(
            key in spec.code_options
            for key in ("nroots", "tda")
        ):
            raise ValueError(
                "nroots and tda are supported only for "
                "the excited_states task."
            )

    def _build_state(
        self,
        spec: CalculationSpec,
    ) -> dict[str, Any]:
        """
        Translate a generic calculation specification into ORCA state.

        Parameters
        ----------
        spec : CalculationSpec
            Previously validated scientific specification.

        Returns
        -------
        dict[str, Any]
            ORCA-specific state dictionary compatible with OrcaIO.

        Notes
        -----
        Generic scientific tasks are mapped to native ORCA keywords.

        For vertical excited-state calculations, TDDFT options are
        placed in the corresponding native ORCA input block.

        The method does not allocate computational resources.
        """
        parameters = spec.parameters
        options = spec.code_options

        keywords = []

        for key in ("dispersion", "scf"):
            value = options.get(key)

            if value:
                keywords.append(value)

        keywords.append(self.TASK_KEYWORDS[spec.task])
        keywords.extend(options.get("keywords", ()))

        blocks = {
            name: dict(values)
            for name, values in options.get("blocks", {}).items()
        }

        if spec.task == "excited_states":
            tddft = blocks.setdefault("tddft", {})

            if "nroots" in tddft or "tda" in tddft:
                raise ValueError(
                    "Specify nroots and tda at the top level of "
                    "code_options, not inside the tddft block."
                )

            tddft["nroots"] = options.get("nroots", 5)
            tddft["tda"] = (
                "true" if options.get("tda", False) else "false"
            )

        return {
            "name": spec.name,
            "method": parameters["method"],
            "basis": parameters["basis"],
            "charge": parameters.get("charge", 0),
            "mult": parameters.get("multiplicity", 1),
            "keywords": keywords,
            "blocks": blocks,
        }

    def prepare(
        self,
        spec: CalculationSpec,
        system: Atoms,
    ) -> PreparedCalculation:
        """
        Prepare a conventional ORCA input without filesystem operations.

        Parameters
        ----------
        spec : CalculationSpec
            Scientific specification describing the calculation.

        system : ase.Atoms
            Initial molecular geometry.

            Coordinates are interpreted in Angstrom.

        Returns
        -------
        PreparedCalculation
            Immutable input bundle containing one ORCA input file.

        Raises
        ------
        TypeError
            If system is not an ASE Atoms object.

        ValueError
            If the specification is unsupported or inconsistent.

        Notes
        -----
        This method supports one conventional ORCA calculation.

        ORCA Compound calculations, which may represent several
        dependent scientific operations inside a single execution,
        will be implemented separately.

        The generated input intentionally excludes resource settings.
        An execution adapter will supply these when staging the job.
        """
        self.validate_spec(spec)

        if not isinstance(system, Atoms):
            raise TypeError(
                "system must be an ASE Atoms object."
            )

        state = self._build_state(spec)

        content = self.io.render_orca_input(
            system,
            state,
            include_resources=False,
        )

        # Use a fixed filename; the execution context supplies identity.
        filename = "calc.inp"

        return PreparedCalculation(
            files={filename: content},
            input_filename=filename,
        )

    def parse(
        self,
        outputs: Mapping[str, str],
    ) -> CalculationResult:
        """
        Parse retrieved ORCA output into structured scientific properties.

        Parameters
        ----------
        outputs : Mapping[str, str]
            Mapping from retrieved filenames to their text contents.

            The mapping must contain ``"calc.out"``.

        Returns
        -------
        CalculationResult
            Preliminary scientific result containing parsed properties.

            Completion status and convergence must subsequently be
            established through ``validate_result``.

        Raises
        ------
        TypeError
            If outputs is not a mapping or the output content is not text.

        ValueError
            If the required output file is missing.

        Notes
        -----
        This method delegates numerical extraction to ORCAParser.

        It does not perform scientific validation and does not access
        the filesystem.
        """
        if not isinstance(outputs, Mapping):
            raise TypeError("outputs must be a mapping.")

        if "calc.out" not in outputs:
            raise ValueError(
                "Required ORCA output 'calc.out' is missing."
            )

        text = outputs["calc.out"]

        if not isinstance(text, str):
            raise TypeError(
                "ORCA output contents must be text."
            )

        return ORCAParser.parse(text)

    def validate_result(
        self,
        spec: CalculationSpec,
        result: CalculationResult,
        outputs: Mapping[str, str],
    ) -> CalculationResult:
        """
        Validate a parsed ORCA result against its scientific specification.

        Parameters
        ----------
        spec : CalculationSpec
            Original scientific calculation specification.

        result : CalculationResult
            Preliminary result produced by the ORCA parser.

        outputs : Mapping[str, str]
            Retrieved ORCA output-file contents.

            The mapping must contain ``"calc.out"``.

        Returns
        -------
        CalculationResult
            New result incorporating the scientific validation outcome.

            Parsed scientific properties and units are preserved.

        Raises
        ------
        TypeError
            If the specification, result, or output data have invalid types.

        ValueError
            If the specification is unsupported or the required output
            is unavailable.

        Notes
        -----
        This method does not modify the supplied CalculationResult.

        It evaluates task-specific completion criteria through
        ORCAValidator and merges its findings with the parsed data.

        Numerical convergence is reported explicitly for geometry
        optimizations.

        For single-point and vertical excited-state calculations,
        convergence remains None because the current validator does not
        independently verify all numerical convergence criteria.
        """
        self.validate_spec(spec)

        if not isinstance(result, CalculationResult):
            raise TypeError(
                "result must be a CalculationResult."
            )

        if not isinstance(outputs, Mapping):
            raise TypeError("outputs must be a mapping.")

        if "calc.out" not in outputs:
            raise ValueError(
                "Required ORCA output 'calc.out' is missing."
            )

        text = outputs["calc.out"]

        if not isinstance(text, str):
            raise TypeError(
                "ORCA output contents must be text."
            )

        expected_roots = 5

        if spec.task == "excited_states":
            expected_roots = spec.code_options.get("nroots", 5)

        report = ORCAValidator.inspect(
            text,
            task=spec.task,
            expected_roots=expected_roots,
        )

        metadata = dict(result.metadata)

        metadata["validation"] = {
            "terminated_normally": report.terminated_normally,
            "energy_found": report.energy_found,
            "optimization_converged": report.optimization_converged,
            "singlet_roots": report.singlet_roots,
            "triplet_roots": report.triplet_roots,
        }

        return CalculationResult(
            status=report.status,
            converged=report.optimization_converged,
            properties=dict(result.to_dict()["properties"]),
            units=dict(result.units),
            metadata=metadata,
            warnings=[
                *result.warnings,
                *report.warnings,
            ],
            errors=[
                *result.errors,
                *report.errors,
            ],
        )