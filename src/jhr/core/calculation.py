"""
Core abstractions for scientific calculations.

This module defines code-independent representations of scientific
calculations. These representations describe what should be calculated
without prescribing how, where, or when the calculation is executed.

The principal abstraction is :class:`CalculationSpec`, which captures
the scientific intent of a calculation.

Design principles
-----------------
1. Scientific specifications are independent of execution infrastructure.
2. Shared scientific concepts are distinguished from code-specific options.
3. Specifications are serializable to JSON-compatible dictionaries.
4. Specifications are immutable after construction.
5. The module does not depend on AiiDA, ASE, or individual simulation codes.

The translation of a CalculationSpec into an executable input is the
responsibility of a code-specific adapter.

Examples
--------
>>> spec = CalculationSpec(
...     name="S0_opt",
...     code="orca",
...     task="optimization",
...     parameters={
...         "method": "PBE0",
...         "basis": "def2-TZVP",
...         "charge": 0,
...         "multiplicity": 1,
...     },
...     code_options={
...         "dispersion": "D3BJ",
...         "scf": "TightSCF",
...     },
... )

>>> spec.task
'optimization'

>>> spec.parameters["method"]
'PBE0'
"""

from __future__ import annotations

import json

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _freeze(value: Any) -> Any:
    """
    Recursively convert JSON-compatible data into immutable values.

    Parameters
    ----------
    value : Any
        A JSON-compatible Python value.

    Returns
    -------
    Any
        An immutable representation of the input. Dictionaries become
        read-only mappings, and lists become tuples.

    Raises
    ------
    TypeError
        If an unsupported Python type is encountered.
    ValueError
        If a floating-point value is not JSON-compatible.

    Notes
    -----
    This function deliberately does not accept arbitrary Python objects.
    Scientific objects such as ASE Atoms must be represented separately
    or explicitly serialized before inclusion in a specification.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not json.loads(json.dumps(value, allow_nan=False)) == value:
            raise ValueError("Invalid floating-point value.")
        return value

    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("Dictionary keys must be strings.")

        return MappingProxyType({
            key: _freeze(item)
            for key, item in value.items()
        })

    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)

    raise TypeError(
        f"Unsupported parameter type: {type(value).__name__}"
    )


def _thaw(value: Any) -> Any:
    """
    Convert an immutable parameter structure into JSON-compatible data.

    Parameters
    ----------
    value : Any
        An immutable value produced by :func:`_freeze`.

    Returns
    -------
    Any
        A JSON-compatible value containing ordinary dictionaries,
        lists, and scalar values.
    """
    if isinstance(value, Mapping):
        return {
            key: _thaw(item)
            for key, item in value.items()
        }

    if isinstance(value, tuple):
        return [_thaw(item) for item in value]

    return value


@dataclass(frozen=True)
class CalculationSpec:
    """
    Describe a scientific calculation independently of its execution.

    A CalculationSpec is a declarative representation of a single
    logical scientific calculation.

    It identifies the target simulation code, scientific task,
    general calculation parameters, and code-specific configuration.

    The specification does not contain molecular structures,
    execution resources, filesystem paths, or scheduler settings.

    Parameters
    ----------
    name : str
        Human-readable identifier for the calculation.

        Examples include ``"S0_opt"``, ``"TDDFT_vertical"``,
        and ``"SCF"``.

        The name identifies the calculation within a scientific
        workflow. It is not required to be globally unique.

    code : str
        Identifier of the scientific code responsible for implementing
        the calculation.

        Examples include ``"orca"``, ``"qe"``, and ``"lammps"``.

        The identifier is normalized to lowercase.

    task : str
        Code-independent description of the scientific operation.

        Examples include ``"optimization"``, ``"single_point"``,
        ``"excited_states"``, and ``"molecular_dynamics"``.

        The task is normalized to lowercase.

        Recognition and validation of specific task names are delegated
        to the relevant code adapter.

    parameters : dict[str, Any], optional
        General scientific settings associated with the calculation.

        Examples include electronic-structure methods, basis sets,
        charge, and spin multiplicity.

        Parameter values must be JSON-compatible.

        Nested dictionaries and lists are permitted.

    code_options : dict[str, Any], optional
        Code-specific settings that do not belong in the shared
        scientific parameter vocabulary.

        For ORCA, examples include SCF keywords, convergence settings,
        and native input blocks.

        These values must also be JSON-compatible.

    Attributes
    ----------
    name : str
        Calculation identifier.

    code : str
        Normalized scientific code identifier.

    task : str
        Normalized scientific task identifier.

    parameters : Mapping[str, Any]
        Immutable scientific parameters.

    code_options : Mapping[str, Any]
        Immutable code-specific options.

    Notes
    -----
    A CalculationSpec describes one logical scientific operation.

    It does not necessarily correspond to one operating-system process
    or one scheduler job.

    For example, ORCA may execute multiple scientific operations within
    a Compound calculation. The relationship between specifications and
    execution units will be represented by a separate abstraction.

    This class does not verify that a particular method, basis set,
    task, or code option is supported by the target scientific code.
    Such validation belongs to the code-specific adapter.

    The class is immutable. Nested parameters are recursively converted
    to read-only representations during initialization.

    Examples
    --------
    Define an ORCA geometry optimization:

    >>> spec = CalculationSpec(
    ...     name="S0_opt",
    ...     code="orca",
    ...     task="optimization",
    ...     parameters={
    ...         "method": "PBE0",
    ...         "basis": "def2-TZVP",
    ...         "charge": 0,
    ...         "multiplicity": 1,
    ...     },
    ...     code_options={
    ...         "dispersion": "D3BJ",
    ...         "scf": "TightSCF",
    ...     },
    ... )

    Convert the specification into a dictionary:

    >>> data = spec.to_dict()

    Reconstruct an equivalent specification:

    >>> restored = CalculationSpec.from_dict(data)
    >>> restored == spec
    True
    """

    name: str
    code: str
    task: str

    parameters: Mapping[str, Any] = field(default_factory=dict)
    code_options: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Validate and normalize the calculation specification.

        Raises
        ------
        TypeError
            If identifiers or parameter containers have invalid types,
            or parameter values are not JSON-compatible.
        ValueError
            If an identifier is empty or a numeric value is not
            JSON-compatible.
        """
        for attribute in ("name", "code", "task"):
            value = getattr(self, attribute)

            if not isinstance(value, str):
                raise TypeError(
                    f"{attribute!r} must be a string."
                )

            if not value.strip():
                raise ValueError(
                    f"{attribute!r} cannot be empty."
                )

        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "code", self.code.strip().lower())
        object.__setattr__(self, "task", self.task.strip().lower())

        for attribute in ("parameters", "code_options"):
            value = getattr(self, attribute)

            if not isinstance(value, dict):
                raise TypeError(
                    f"{attribute!r} must be a dictionary."
                )

            object.__setattr__(
                self,
                attribute,
                _freeze(value),
            )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the specification into a plain Python dictionary.

        Returns
        -------
        dict[str, Any]
            A JSON-compatible dictionary containing all specification
            fields.

        Notes
        -----
        The resulting dictionary is independent of the specification.
        Modifying it does not change the original object.

        This representation can be used for JSON serialization,
        configuration files, and AiiDA Dict nodes.

        Examples
        --------
        >>> spec = CalculationSpec(
        ...     name="test",
        ...     code="orca",
        ...     task="single_point",
        ... )
        >>> spec.to_dict()["task"]
        'single_point'
        """
        return {
            "name": self.name,
            "code": self.code,
            "task": self.task,
            "parameters": _thaw(self.parameters),
            "code_options": _thaw(self.code_options),
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> CalculationSpec:
        """
        Construct a calculation specification from a dictionary.

        Parameters
        ----------
        data : Mapping[str, Any]
            Serialized calculation specification.

            The keys ``name``, ``code``, and ``task`` are required.
            The keys ``parameters`` and ``code_options`` are optional.

        Returns
        -------
        CalculationSpec
            Reconstructed calculation specification.

        Raises
        ------
        TypeError
            If the input is not a mapping or contains invalid values.
        KeyError
            If a required field is missing.
        ValueError
            If an identifier or parameter value is invalid.

        Examples
        --------
        >>> data = {
        ...     "name": "S0_opt",
        ...     "code": "orca",
        ...     "task": "optimization",
        ... }
        >>> spec = CalculationSpec.from_dict(data)
        >>> spec.code
        'orca'
        """
        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping.")

        return cls(
            name=data["name"],
            code=data["code"],
            task=data["task"],
            parameters=data.get("parameters", {}),
            code_options=data.get("code_options", {}),
        )


from typing import Literal


CalculationStatus = Literal["completed", "partial", "failed"]


@dataclass(frozen=True)
class CalculationResult:
    """
    Represent the scientific outcome of a calculation.

    A CalculationResult contains structured scientific properties,
    convergence information, diagnostic messages, and metadata.

    The class is independent of the scientific code used to produce
    the results and the infrastructure used to execute the calculation.

    Parameters
    ----------
    status : {"completed", "partial", "failed"}
        Scientific outcome of the calculation.

        ``"completed"``
            The requested scientific operation finished successfully
            according to the applicable validation criteria.

        ``"partial"``
            The operation did not fully satisfy its completion criteria,
            but produced potentially useful intermediate results.

        ``"failed"``
            The requested operation failed. Diagnostic information
            should be provided through the ``errors`` field.

        This status describes the scientific outcome, not the operating
        system exit status or AiiDA process state.

    converged : bool or None, optional
        Whether the relevant numerical convergence criteria were met.

        ``True``
            Numerical convergence was verified.

        ``False``
            Numerical convergence was attempted but not achieved.

        ``None``
            Convergence was not evaluated or is not applicable.

        The meaning of convergence depends on the scientific task.
        For example, an optimization may require both electronic
        and geometric convergence.

    properties : dict[str, Any], optional
        Computed scientific quantities.

        Values must be JSON-compatible and may include scalars,
        lists, and nested dictionaries.

        Examples include total energy, excitation energies,
        dipole moments, forces, and other calculated properties.

        Large numerical arrays and complete atomic structures may
        eventually require dedicated scientific data containers
        rather than direct inclusion in this dictionary.

    units : dict[str, str], optional
        Physical units associated with entries in ``properties``.

        Each key must correspond to a property name.

        Only properties requiring a unit need an entry.

        Unit strings are descriptive at this stage; dimensional
        compatibility and unit conversion are not performed.

    metadata : dict[str, Any], optional
        Additional information about the calculation and its analysis.

        Examples include the number of SCF iterations, convergence
        thresholds, and parser-specific information.

        Values must be JSON-compatible.

        Metadata should not duplicate execution provenance already
        managed by AiiDA.

    warnings : list[str], optional
        Nonfatal diagnostic messages produced during parsing
        or scientific validation.

    errors : list[str], optional
        Diagnostic messages explaining scientific failures.

    Attributes
    ----------
    status : str
        Validated scientific outcome.

    converged : bool or None
        Numerical convergence indicator.

    properties : Mapping[str, Any]
        Immutable scientific property data.

    units : Mapping[str, str]
        Immutable unit definitions.

    metadata : Mapping[str, Any]
        Immutable calculation metadata.

    warnings : tuple[str, ...]
        Diagnostic warnings.

    errors : tuple[str, ...]
        Diagnostic errors.

    Notes
    -----
    CalculationResult represents one logical scientific calculation.

    It does not own the raw output files, calculation working directory,
    scheduler information, or execution history.

    Those responsibilities belong to the execution layer and, when
    available, AiiDA provenance.

    A failed calculation may still contain scientific properties.

    For example, an unsuccessful geometry optimization may produce
    an energy and intermediate geometry. Such properties must not
    automatically be interpreted as converged results.

    The status and convergence fields are deliberately independent.
    A completed calculation may have ``converged=None`` if numerical
    convergence is not applicable to that operation.

    The class does not decide whether scientific validation has passed.
    That determination belongs to a code-specific parser or validator.

    Examples
    --------
    Represent a successful electronic-structure calculation:

    >>> result = CalculationResult(
    ...     status="completed",
    ...     converged=True,
    ...     properties={
    ...         "total_energy": -1042.673,
    ...     },
    ...     units={
    ...         "total_energy": "eV",
    ...     },
    ... )

    >>> result.properties["total_energy"]
    -1042.673

    Represent a partially successful calculation:

    >>> partial = CalculationResult(
    ...     status="partial",
    ...     converged=False,
    ...     properties={"total_energy": -1042.5},
    ...     units={"total_energy": "eV"},
    ...     warnings=["Geometry optimization did not converge."],
    ... )
    """

    status: CalculationStatus
    converged: bool | None = None

    properties: Mapping[str, Any] = field(default_factory=dict)
    units: Mapping[str, str] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Validate and normalize scientific results.

        Raises
        ------
        TypeError
            If convergence, properties, units, metadata, or diagnostic
            messages have unsupported types.

        ValueError
            If the status is invalid, an unsupported numeric value
            is encountered, or a unit refers to an unknown property.

        Notes
        -----
        Nested scientific data are frozen recursively to prevent
        accidental modification after construction.
        """
        valid_statuses = {"completed", "partial", "failed"}

        if self.status not in valid_statuses:
            raise ValueError(
                f"Invalid calculation status: {self.status!r}. "
                f"Expected one of {sorted(valid_statuses)}."
            )

        if self.converged is not None:
            if not isinstance(self.converged, bool):
                raise TypeError(
                    "converged must be a boolean or None."
                )

        for attribute in ("properties", "units", "metadata"):
            value = getattr(self, attribute)

            if not isinstance(value, dict):
                raise TypeError(
                    f"{attribute!r} must be a dictionary."
                )

            object.__setattr__(
                self,
                attribute,
                _freeze(value),
            )

        for property_name, unit in self.units.items():
            if property_name not in self.properties:
                raise ValueError(
                    f"Unit defined for unknown property "
                    f"{property_name!r}."
                )

            if not isinstance(unit, str) or not unit.strip():
                raise ValueError(
                    f"Unit for {property_name!r} "
                    "must be a non-empty string."
                )

        for attribute in ("warnings", "errors"):
            value = getattr(self, attribute)

            if not isinstance(value, (list, tuple)):
                raise TypeError(
                    f"{attribute!r} must be a list or tuple."
                )

            if not all(isinstance(item, str) for item in value):
                raise TypeError(
                    f"Every entry in {attribute!r} must be a string."
                )

            object.__setattr__(
                self,
                attribute,
                tuple(value),
            )

    @property
    def successful(self) -> bool:
        """
        Indicate whether the requested scientific operation completed.

        Returns
        -------
        bool
            ``True`` when the scientific status is ``"completed"``.
            Otherwise, ``False``.

        Notes
        -----
        Scientific completion does not necessarily imply that every
        possible numerical convergence criterion was evaluated.

        Use ``converged`` separately when numerical convergence is
        relevant to the scientific workflow.
        """
        return self.status == "completed"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result into a JSON-compatible dictionary.

        Returns
        -------
        dict[str, Any]
            A dictionary containing scientific properties, units,
            metadata, convergence status, and diagnostic messages.

        Notes
        -----
        The returned dictionary contains independent mutable copies
        of the result data.

        This representation is suitable for JSON serialization and
        storage in an AiiDA Dict node, subject to the usual practical
        limits on data size.
        """
        return {
            "status": self.status,
            "converged": self.converged,
            "properties": _thaw(self.properties),
            "units": _thaw(self.units),
            "metadata": _thaw(self.metadata),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> CalculationResult:
        """
        Reconstruct a calculation result from serialized data.

        Parameters
        ----------
        data : Mapping[str, Any]
            Serialized calculation result.

            The ``status`` field is required. Other fields are
            optional and use the constructor defaults when absent.

        Returns
        -------
        CalculationResult
            Reconstructed immutable scientific result.

        Raises
        ------
        TypeError
            If the input is not a mapping or contains invalid values.

        KeyError
            If the required status field is missing.

        ValueError
            If the serialized contents fail validation.
        """
        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping.")

        return cls(
            status=data["status"],
            converged=data.get("converged"),
            properties=data.get("properties", {}),
            units=data.get("units", {}),
            metadata=data.get("metadata", {}),
            warnings=data.get("warnings", []),
            errors=data.get("errors", []),
        )