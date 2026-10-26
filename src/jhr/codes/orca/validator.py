"""
Scientific validation of ORCA calculation outputs.

This module inspects ORCA output text to determine whether a requested
scientific operation completed successfully.

It distinguishes normal program termination, the presence of electronic
energy data, geometry convergence, and TDDFT root completeness.

Validation does not execute ORCA and does not require filesystem access.

The module also provides backward-compatible file-based validation
methods for use in existing standalone ORCA workflows.

Notes
-----
Normal ORCA termination is not sufficient evidence of successful
geometry optimization.

Validation must be based on the scientific task and the corresponding
completion criteria.

For high-throughput workflows, the inspection interface returns a
structured report rather than raising an exception for ordinary
calculation failures.
"""

from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


ValidationTask = Literal[
    "single_point",
    "optimization",
    "excited_states",
]


@dataclass(frozen=True)
class ValidationReport:
    """
    Describe the scientific validation outcome of an ORCA calculation.

    Parameters
    ----------
    status : {"completed", "partial", "failed"}
        Scientific completion status.

        ``"completed"`` means that the supported completion checks
        for the requested task passed.

        ``"partial"`` means the task did not fully pass validation,
        but potentially useful scientific data were detected.

        ``"failed"`` means the task did not pass validation and
        no usable result was established by these checks.

    terminated_normally : bool
        Whether the ORCA normal-termination marker was detected.

    energy_found : bool
        Whether a final single-point energy record was detected.

    optimization_converged : bool or None
        Whether successful geometry convergence was reported.

        None indicates that geometry convergence was not applicable.

    singlet_roots : int
        Number of distinct singlet TDDFT root indices detected.

    triplet_roots : int
        Number of distinct triplet TDDFT root indices detected.

    warnings : tuple[str, ...]
        Nonfatal diagnostic messages.

    errors : tuple[str, ...]
        Reasons why the requested scientific operation did not
        pass validation.

    Notes
    -----
    The report captures observations from the ORCA output.

    It does not contain numerical energies, optimized structures,
    oscillator strengths, or other parsed scientific properties.

    Those quantities belong to CalculationResult.

    Absence of a recognized marker is not always proof that a
    physical calculation failed. It may indicate an unsupported
    output format, truncated file, or incomplete parser.

    Such situations should be treated conservatively.
    """

    status: Literal["completed", "partial", "failed"]

    terminated_normally: bool
    energy_found: bool

    optimization_converged: bool | None = None

    singlet_roots: int = 0
    triplet_roots: int = 0

    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    @property
    def successful(self) -> bool:
        """
        Indicate whether all supported task-completion checks passed.

        Returns
        -------
        bool
            True if status is ``"completed"``; otherwise False.
        """
        return self.status == "completed"


class ORCAValidator:
    """
    Inspect ORCA output for scientific completion and convergence.

    The primary interface is :meth:`inspect`, which operates on
    output text and returns a ValidationReport.

    File-based validation methods are retained for compatibility
    with existing standalone ORCA workflows.

    The validator does not parse numerical scientific properties
    or execute calculations.

    Supported tasks
    ---------------
    single_point
        Requires normal termination and a final energy record.

    optimization
        Requires normal termination, a final energy record,
        and explicit geometry convergence.

    excited_states
        Requires normal termination, a final energy record,
        and the requested number of distinct singlet TDDFT roots.

    Notes
    -----
    These criteria are deliberately conservative.

    In particular, the presence of a normal-termination marker
    does not establish geometry convergence.

    This initial implementation targets conventional ORCA outputs.
    Compound calculations and specialized excited-state methods
    will require additional handling.
    """

    TERMINATION_MARKER = "ORCA TERMINATED NORMALLY"
    OPTIMIZATION_MARKER = "THE OPTIMIZATION HAS CONVERGED"

    ENERGY_PATTERN = re.compile(
        r"^\s*FINAL SINGLE POINT ENERGY\s+"
        r"[-+]?\d+(?:\.\d+)?(?:[EeDd][-+]?\d+)?",
        flags=re.MULTILINE,
    )

    STATE_PATTERN = re.compile(
        r"^\s*STATE\s+(\d+)\s*:",
        flags=re.IGNORECASE,
    )

    SPIN_SECTION_PATTERN = re.compile(
        r"EXCITED STATES\s*\((SINGLETS|TRIPLETS)\)",
        flags=re.IGNORECASE,
    )

    @classmethod
    def _count_roots(
        cls,
        text: str,
    ) -> tuple[int, int]:
        """
        Count distinct TDDFT root indices by spin section.

        Parameters
        ----------
        text : str
            Complete ORCA output text.

        Returns
        -------
        tuple[int, int]
            Number of distinct singlet and triplet root indices,
            respectively.

        Notes
        -----
        ORCA may print multiple excited-state sections.

        This method recognizes explicit singlet and triplet headings
        and accumulates distinct state indices separately.

        Root counting does not establish that excitation energies
        or transition properties were parsed successfully.

        If the output lacks recognizable spin-section headings,
        root counts remain zero.
        """
        singlets = set()
        triplets = set()

        active_section = None

        for line in text.splitlines():

            section_match = cls.SPIN_SECTION_PATTERN.search(line)

            if section_match:
                active_section = section_match.group(1).lower()
                continue

            state_match = cls.STATE_PATTERN.match(line)

            if not state_match:
                continue

            root = int(state_match.group(1))

            if active_section == "singlets":
                singlets.add(root)

            elif active_section == "triplets":
                triplets.add(root)

        return len(singlets), len(triplets)

    @classmethod
    def inspect(
        cls,
        text: str,
        task: ValidationTask = "single_point",
        require_termination: bool = True,
        expected_roots: int = 5,
    ) -> ValidationReport:
        """
        Inspect ORCA output against task-specific completion criteria.

        Parameters
        ----------
        text : str
            Complete ORCA standard output.

        task : {"single_point", "optimization", "excited_states"}, optional
            Scientific task to validate.

        expected_roots : int, optional
            Minimum number of distinct singlet TDDFT roots required
            for an excited-state calculation.

            The default is 5.

            This parameter is ignored for other tasks.

                    require_termination : bool, optional
            Whether the inspected text must contain the ORCA
            normal-termination marker.

            Default is True for standalone calculations.

            Set to False when validating individual steps of an ORCA
            Compound calculation, because the overall termination marker
            belongs to the Compound execution rather than each step.

            Disabling this check does not establish that the step was
            executed successfully. The caller must ensure that the
            corresponding step output is complete.

        Returns
        -------
        ValidationReport
            Structured validation outcome and diagnostics.

        Raises
        ------
        TypeError
            If text is not a string.

        ValueError
            If the task is unsupported or expected_roots is invalid.

        Notes
        -----
        Ordinary scientific failures do not raise exceptions.

        Instead, an appropriate status and diagnostic messages
        are returned.

        The status is determined as follows:

        - completed: All supported task-specific checks passed.
        - partial: Validation failed, but an energy or excited-state
          root record was detected.
        - failed: Validation failed without those data records.

        For optimization, convergence is explicitly reported.

        For other tasks, the report does not claim to establish
        detailed numerical convergence from the termination marker.

        Examples
        --------
        >>> text = (
        ...     "FINAL SINGLE POINT ENERGY -100.0\\n"
        ...     "ORCA TERMINATED NORMALLY\\n"
        ... )
        >>> report = ORCAValidator.inspect(text)
        >>> report.successful
        True
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        valid_tasks = {
            "single_point",
            "optimization",
            "excited_states",
        }

        if task not in valid_tasks:
            raise ValueError(
                f"Unsupported validation task: {task!r}"
            )

        if type(expected_roots) is not int or expected_roots < 1:
            raise ValueError(
                "expected_roots must be a positive integer."
            )

        terminated = cls.TERMINATION_MARKER in text

        energy_found = bool(
            cls.ENERGY_PATTERN.search(text)
        )

        singlet_roots, triplet_roots = cls._count_roots(text)

        optimization_converged = None

        errors = []
        warnings = []

        if not isinstance(require_termination, bool):
            raise TypeError("require_termination must be a boolean.")

        if require_termination and not terminated:
            errors.append(
                "ORCA normal termination was not confirmed."
            )
        if not energy_found:
            errors.append(
                "No final single-point energy was detected."
            )

        if task == "optimization":

            optimization_converged = (
                cls.OPTIMIZATION_MARKER in text
            )

            if not optimization_converged:
                errors.append(
                    "Geometry optimization convergence "
                    "was not confirmed."
                )

        elif task == "excited_states":

            if singlet_roots < expected_roots:
                errors.append(
                    f"Expected at least {expected_roots} singlet "
                    f"TDDFT roots; found {singlet_roots}."
                )

            if triplet_roots:
                warnings.append(
                    f"Detected {triplet_roots} triplet roots; "
                    "triplet completeness was not validated."
                )

        if not errors:
            status = "completed"

        elif energy_found or singlet_roots or triplet_roots:
            status = "partial"

        else:
            status = "failed"

        return ValidationReport(
            status=status,
            terminated_normally=terminated,
            energy_found=energy_found,
            optimization_converged=optimization_converged,
            singlet_roots=singlet_roots,
            triplet_roots=triplet_roots,
            warnings=tuple(warnings),
            errors=tuple(errors),
        )
