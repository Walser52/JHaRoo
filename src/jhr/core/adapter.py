"""
Interfaces for adapting scientific simulation codes to jhr.

This module defines the contract between code-independent scientific
calculations and code-specific input/output implementations.

The principal abstractions are:

- PreparedCalculation:
    An immutable collection of generated input files.

- CodeAdapter:
    An abstract interface for validating specifications, preparing
    inputs, parsing outputs, and evaluating scientific results.

Adapters do not execute scientific programs, manage working directories,
submit scheduler jobs, or store provenance.

These responsibilities belong to a separate execution layer, which
may use AiiDA or another execution system.

Notes
-----
A code adapter translates scientific intent into the native
representation required by a simulation program.

For example, an ORCA adapter may translate the generic task
``"optimization"`` into the ORCA keyword ``Opt``.

Similarly, a Quantum ESPRESSO adapter may translate the same task
into ``calculation = 'relax'``.

The adapter interface does not require these programs to support
identical scientific features.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any, ClassVar, Mapping

from jhr.core.calculation import (
    CalculationSpec,
    CalculationResult,
)


@dataclass(frozen=True)
class PreparedCalculation:
    """
    Represent the input files required for a scientific calculation.

    A PreparedCalculation contains the generated input files associated
    with one execution unit.

    It does not define the execution directory, executable, scheduler,
    computational resources, or process environment.

    Parameters
    ----------
    files : dict[str, str]
        Mapping from relative filenames to UTF-8 text contents.

        Keys represent paths relative to the eventual calculation
        working directory.

        Absolute paths and parent-directory traversal are prohibited.

        The file contents are held in memory until the execution
        layer writes them to a working directory.

    input_filename : str
        Name of the primary input file.

        This filename must exist in ``files``.

        Some scientific programs use a primary input file to select
        the calculation to execute.

    Attributes
    ----------
    files : Mapping[str, str]
        Immutable mapping of relative paths to file contents.

    input_filename : str
        Primary input filename.

    Notes
    -----
    The current representation supports UTF-8 text files only.

    Future extensions may introduce binary files, external file
    references, or structured staging instructions.

    PreparedCalculation is independent of any specific filesystem
    location.

    This allows the same prepared calculation to be used for local
    execution, Slurm submission, and AiiDA CalcJobs.

    Examples
    --------
    >>> prepared = PreparedCalculation(
    ...     files={
    ...         "S0_opt.inp": "! PBE0 def2-TZVP Opt\\n",
    ...     },
    ...     input_filename="S0_opt.inp",
    ... )

    >>> prepared.input_filename
    'S0_opt.inp'
    """

    files: Mapping[str, str] = field(default_factory=dict)
    input_filename: str = ""

    def __post_init__(self) -> None:
        """
        Validate and protect generated input files.

        Raises
        ------
        TypeError
            If the files collection, filenames, or file contents
            have unsupported types.

        ValueError
            If a path is invalid, the primary input file is missing,
            or a path would escape the calculation directory.
        """
        if not isinstance(self.files, dict):
            raise TypeError("files must be a dictionary.")

        if not isinstance(self.input_filename, str):
            raise TypeError("input_filename must be a string.")

        for filename, content in self.files.items():

            if not isinstance(filename, str):
                raise TypeError("File names must be strings.")

            if not isinstance(content, str):
                raise TypeError(
                    f"File contents must be text: {filename!r}"
                )

            if (
                not filename
                or "\\" in filename
                or "\x00" in filename
            ):
                raise ValueError(
                    f"Invalid relative filename: {filename!r}"
                )

            path = PurePosixPath(filename)

            if (
                path.is_absolute()
                or ".." in path.parts
                or "." in filename.split("/")
                or "" in filename.split("/")
            ):
                raise ValueError(
                    f"Invalid relative filename: {filename!r}"
                )

        if self.input_filename not in self.files:
            raise ValueError(
                "input_filename must reference a file "
                "present in files."
            )

        object.__setattr__(
            self,
            "files",
            MappingProxyType(dict(self.files)),
        )


class CodeAdapter(ABC):
    """
    Abstract interface between jhr and a scientific simulation code.

    A CodeAdapter translates code-independent calculation specifications
    into native simulation inputs and converts output data into
    structured scientific results.

    Concrete adapters implement the details of individual scientific
    programs, such as ORCA, Quantum ESPRESSO, or LAMMPS.

    Attributes
    ----------
    code : str
        Identifier of the supported scientific program.

        Concrete subclasses must override this attribute.

    Notes
    -----
    A CodeAdapter performs four operations:

    1. Validate a scientific specification.
    2. Prepare native simulation inputs.
    3. Parse simulation outputs.
    4. Validate the scientific results.

    The adapter does not execute a calculation.

    Execution, scheduler integration, resource allocation, working
    directories, retries, and provenance are delegated to an external
    execution system.

    Adapters should ideally be stateless. The result of input
    preparation should depend only on the supplied specification
    and physical system.

    This makes adapters reusable across local scripts, automated
    workflows, and high-throughput execution systems.

    Examples
    --------
    A concrete implementation might be used as follows:

    >>> # adapter = OrcaAdapter()
    >>> # adapter.validate_spec(spec)
    >>> # prepared = adapter.prepare(spec, atoms)
    >>> # result = adapter.parse(output_files)
    >>> # result = adapter.validate_result(spec, result)

    The ORCA adapter is not implemented by this base class.
    """

    code: ClassVar[str] = ""

    @abstractmethod
    def validate_spec(
        self,
        spec: CalculationSpec,
    ) -> None:
        """
        Validate a calculation specification for this code.

        Parameters
        ----------
        spec : CalculationSpec
            Scientific calculation specification to validate.

        Returns
        -------
        None
            Successful validation returns without a value.

        Raises
        ------
        TypeError
            If the specification has an invalid type.

        ValueError
            If the scientific code, task, parameters, or options
            are unsupported or inconsistent.

        Notes
        -----
        Validation should include checking that ``spec.code``
        matches the code supported by the adapter.

        This method does not generate files or execute calculations.
        """
        ...

    @abstractmethod
    def prepare(
        self,
        spec: CalculationSpec,
        system: Any,
    ) -> PreparedCalculation:
        """
        Generate native input files for a scientific calculation.

        Parameters
        ----------
        spec : CalculationSpec
            Scientific specification defining the requested operation.

        system : Any
            Physical system associated with the calculation.

            Initially, molecular and atomistic adapters may accept
            ASE Atoms objects.

            A common System abstraction may replace this provisional
            type in a later development stage.

        Returns
        -------
        PreparedCalculation
            Generated input files and primary input filename.

        Raises
        ------
        TypeError
            If the physical system has an unsupported representation.

        ValueError
            If the specification is inconsistent with the system
            or cannot be translated into valid inputs.

        Notes
        -----
        Implementations should call ``validate_spec`` before
        preparing the calculation.

        This method must not execute the scientific program.

        It should not depend on the current working directory.
        """
        ...

    @abstractmethod
    def parse(
        self,
        outputs: Mapping[str, str],
    ) -> CalculationResult:
        """
        Parse native output files into structured scientific results.

        Parameters
        ----------
        outputs : Mapping[str, str]
            Mapping of output filenames to their text contents.

            The execution layer is responsible for retrieving the
            relevant files and providing them to the parser.

        Returns
        -------
        CalculationResult
            Structured scientific data extracted from the outputs.

        Raises
        ------
        ValueError
            If output data are malformed or cannot be interpreted.

        Notes
        -----
        Parsing should distinguish unavailable properties from
        successfully extracted scientific quantities.

        The parser may return partial results when a calculation
        terminated before completing its requested operation.

        Parsers should not silently manufacture missing numerical
        values.
        """
        ...

    @abstractmethod
    def validate_result(
        self,
        spec: CalculationSpec,
        result: CalculationResult,
    ) -> CalculationResult:
        """
        Evaluate a parsed result against scientific completion criteria.

        Parameters
        ----------
        spec : CalculationSpec
            Original calculation specification.

        result : CalculationResult
            Parsed scientific result to validate.

        Returns
        -------
        CalculationResult
            Validated scientific result, including an appropriate
            status, convergence indicator, and diagnostic messages.

        Raises
        ------
        TypeError
            If the supplied specification or result has an invalid type.

        ValueError
            If the result cannot be associated with the requested
            scientific operation.

        Notes
        -----
        Validation criteria depend on the scientific task.

        For example, successful ORCA geometry optimization may require
        both electronic convergence and satisfaction of geometric
        convergence thresholds.

        Because CalculationResult is immutable, implementations should
        return a new result when validation changes its status,
        convergence information, or diagnostics.

        Scientific failure should ordinarily be represented by the
        returned result rather than by an exception.

        Exceptions are reserved for failures of the adapter itself
        or invalid API usage.
        """
        ...