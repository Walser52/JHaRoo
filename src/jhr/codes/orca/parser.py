"""
Parsing utilities for ORCA scientific output.

This module extracts numerical scientific quantities from ORCA output
text and converts them into code-independent CalculationResult objects.

The parser is responsible for data extraction only.

It does not determine whether a calculation converged, whether ORCA
terminated normally, or whether a result is scientifically acceptable.
Those decisions belong to ORCAValidator.

Currently supported properties
------------------------------
total_energy
    Last reported final single-point energy, in Hartree.

Notes
-----
ORCA may report multiple energies during a geometry optimization.

The parser uses the final occurrence of the energy record. This
normally corresponds to the last electronic-structure calculation
performed during the run.

For Compound calculations, the final occurrence may belong to a
different logical calculation step. Compound calculations will
therefore require a step-aware parser.
"""

from __future__ import annotations

import re

from jhr.core.calculation import CalculationResult
from jhr.codes.orca.compound import (
    CompoundResult,
    CompoundStepResult,
)

class ORCAParser:
    """
    Extract structured scientific quantities from ORCA output.

    The parser operates entirely on text and performs no filesystem
    operations.

    It returns a CalculationResult containing extracted properties,
    their physical units, and parsing diagnostics.

    Scientific convergence and completion are evaluated separately.

    Notes
    -----
    Parsing is intentionally conservative.

    Missing numerical quantities are not replaced by arbitrary
    defaults. If an expected quantity cannot be extracted, its
    absence is recorded through diagnostic information.

    The initial implementation supports conventional single-step
    ORCA calculations.
    """

    ENERGY_PATTERN = re.compile(
        r"^\s*FINAL SINGLE POINT ENERGY\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:[EeDd][-+]?\d+)?)",
        flags=re.MULTILINE,
    )

    COMPOUND_STEP_PATTERN = re.compile(
        r"^\s*COMPOUND JOB\s+(\d+)\s*$",
        flags=re.MULTILINE,
    )

    EXCITED_STATE_PATTERN = re.compile(
        r"^\s*STATE\s+(\d+)\s*:"
        r"\s*E=\s*([-+]?\d+(?:\.\d+)?)\s+au"
        r"\s+([-+]?\d+(?:\.\d+)?)\s+eV"
        r".*?\bMult\s+(\d+)",
        flags=re.MULTILINE,
    )
    @classmethod
    def split_compound_steps(
        cls,
        text: str,
    ) -> dict[int, str]:
        """
        Split an ORCA Compound output into numbered step sections.

        Parameters
        ----------
        text : str
            Complete ORCA Compound standard-output text.

        Returns
        -------
        dict[int, str]
            Mapping from one-based Compound step indices to the
            corresponding output-text sections.

            Sections are returned in execution order.

        Raises
        ------
        TypeError
            If text is not a string.

        ValueError
            If numbered Compound step markers are absent, duplicated,
            or not in ascending order.

        Notes
        -----
        A section begins at its ``COMPOUND JOB n`` marker and ends
        immediately before the next numbered Compound job marker.

        The final section extends to the end of the output.

        The unnumbered ``COMPOUND JOB MainJOB`` header is deliberately
        excluded.

        This method performs structural separation only. It does
        not parse numerical properties or establish convergence.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        matches = list(
            cls.COMPOUND_STEP_PATTERN.finditer(text)
        )

        if not matches:
            raise ValueError(
                "No numbered ORCA Compound steps were detected."
            )

        sections = {}
        previous_index = 0

        for position, match in enumerate(matches):
            index = int(match.group(1))

            if index <= previous_index:
                raise ValueError(
                    "Compound step indices must be unique "
                    "and strictly increasing."
                )

            previous_index = index

            start = match.start()

            if position + 1 < len(matches):
                end = matches[position + 1].start()
            else:
                end = len(text)

            sections[index] = text[start:end]

        return sections
    @classmethod
    def _parse_excited_states(
        cls,
        text: str,
    ) -> dict[str, list[dict]]:
        """
        Extract excited-state energies and spin multiplicities.

        Parameters
        ----------
        text : str
            ORCA output text belonging to one calculation step.

        Returns
        -------
        dict[str, list[dict]]
            Dictionary containing separate lists of singlet and
            triplet excited states.

            Each state record contains:

            - ``index``: ORCA state index.
            - ``energy_hartree``: Excitation energy in Hartree.
            - ``energy_ev``: Excitation energy in electronvolts.
            - ``multiplicity``: Spin multiplicity.

        Notes
        -----
        This parser uses the explicit multiplicity recorded on
        individual ORCA excited-state lines.

        It therefore supports ORCA outputs that number singlet and
        triplet roots consecutively.

        Only states matching the conventional TDDFT output format
        are extracted.

        The returned excitation energies are vertical excitation
        energies and are distinct from total electronic energies.
        """
        states = {
            "singlets": [],
            "triplets": [],
        }

        for match in cls.EXCITED_STATE_PATTERN.finditer(text):

            index = int(match.group(1))
            energy_hartree = float(match.group(2))
            energy_ev = float(match.group(3))
            multiplicity = int(match.group(4))

            record = {
                "index": index,
                "energy_hartree": energy_hartree,
                "energy_ev": energy_ev,
                "multiplicity": multiplicity,
            }

            if multiplicity == 1:
                states["singlets"].append(record)

            elif multiplicity == 3:
                states["triplets"].append(record)

        return states

    @classmethod
    def parse_compound(
        cls,
        text: str,
    ) -> CompoundResult:
        """
        Parse scientific results from an ORCA Compound calculation.

        Parameters
        ----------
        text : str
            Complete ORCA Compound standard-output text.

        Returns
        -------
        CompoundResult
            Ordered collection of scientific results, one per
            detected Compound step.

        Raises
        ------
        TypeError
            If text is not a string.

        ValueError
            If no numbered Compound step markers are detected.

        Notes
        -----
        The parser recognizes numbered ORCA Compound job boundaries.

        Each step is parsed independently so that final-energy
        records from different steps are not mixed.

        Excited-state energies are extracted when present.

        The final status of each CalculationResult remains preliminary.
        Scientific completion must subsequently be evaluated against
        the specification for that particular step.

        The overall normal-termination marker is recorded separately
        on the CompoundResult.

        This implementation does not yet handle nested Compound
        control flow, loops, or conditional branches.

        Examples
        --------
        >>> # compound = ORCAParser.parse_compound(output_text)
        >>> # optimization = compound.step(1)
        >>> # tddft = compound.step(2)
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        sections = cls.split_compound_steps(text)

        steps = []

        for index, step_text in sections.items():

            # Existing single-calculation energy parser.
            parsed = cls.parse(step_text)

            properties = dict(parsed.to_dict()["properties"])
            units = dict(parsed.units)
            metadata = dict(parsed.metadata)

            metadata["compound_step"] = index

            excited_states = cls._parse_excited_states(step_text)

            for spin, records in excited_states.items():

                if not records:
                    continue

                key = f"excitation_energies_{spin}"

                properties[key] = [
                    state["energy_ev"]
                    for state in records
                ]

                units[key] = "eV"

                metadata[f"{spin}_state_indices"] = [
                    state["index"]
                    for state in records
                ]

            result = CalculationResult(
                status=parsed.status,
                converged=None,
                properties=properties,
                units=units,
                metadata=metadata,
                warnings=list(parsed.warnings),
                errors=list(parsed.errors),
            )

            steps.append(
                CompoundStepResult(
                    index=index,
                    result=result,
                )
            )

        terminated_normally = (
            "ORCA TERMINATED NORMALLY" in text
        )

        return CompoundResult(
            steps=tuple(steps),
            terminated_normally=terminated_normally,
        )
    @classmethod
    def parse(cls, text: str) -> CalculationResult:
        """
        Parse scientific properties from ORCA standard output.

        Parameters
        ----------
        text : str
            Complete ORCA standard-output text.

        Returns
        -------
        CalculationResult
            Structured result containing extracted quantities.

            The preliminary status is ``"partial"`` when an energy
            is extracted, or ``"failed"`` otherwise.

            A completed status can only be assigned after scientific
            validation.

        Raises
        ------
        TypeError
            If text is not a string.

        Notes
        -----
        The parser selects the last valid final-energy record.

        Energies are retained in Hartree, their native ORCA unit.

        No scientific convergence assumptions are made.

        Examples
        --------
        >>> text = "FINAL SINGLE POINT ENERGY -100.123456"
        >>> result = ORCAParser.parse(text)
        >>> result.properties["total_energy"]
        -100.123456
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        properties = {}
        units = {}
        warnings = []

        matches = cls.ENERGY_PATTERN.findall(text)

        energies = []

        for match in matches:
            try:
                energy = float(
                    match.replace("D", "E").replace("d", "e")
                )
            except ValueError:
                continue

            energies.append(energy)

        if energies:
            properties["total_energy"] = energies[-1]
            units["total_energy"] = "Hartree"

            status = "partial"

        else:
            status = "failed"

            warnings.append(
                "No final single-point energy could be extracted."
            )

        metadata = {
            "energy_records": len(energies),
        }

        return CalculationResult(
            status=status,
            converged=None,
            properties=properties,
            units=units,
            metadata=metadata,
            warnings=warnings,
        )