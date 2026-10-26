"""
Scientific validation of ORCA Compound calculations.

An ORCA Compound calculation may contain several logical scientific
operations executed through one invocation of the ORCA program.

This module validates individual Compound steps against their
corresponding CalculationSpec objects.

The overall ORCA termination status is preserved independently of
the scientific validation outcome of each step.

Design principles
-----------------
1. Each step is associated with exactly one scientific specification.
2. Step-local output is used for step-specific validation.
3. Scientific properties already extracted by ORCAParser are preserved.
4. Validation does not modify existing CalculationResult objects.
5. The overall Compound termination status is not substituted for
   individual scientific convergence criteria.

Notes
-----
This implementation supports linear ORCA Compound calculations
consisting of sequential, numbered steps.

Conditional Compound logic, loops, and nested execution structures
are not yet supported.
"""

from __future__ import annotations

from collections.abc import Sequence

from jhr.core.calculation import (
    CalculationSpec,
    CalculationResult,
)

from jhr.codes.orca.compound import (
    CompoundResult,
    CompoundStepResult,
)

from jhr.codes.orca.parser import ORCAParser
from jhr.codes.orca.validator import ORCAValidator


class ORCACompoundValidator:
    """
    Validate scientific results from an ORCA Compound execution.

    The validator matches each Compound step with its original
    CalculationSpec and applies the corresponding scientific
    completion criteria.

    It delegates task-specific checks to ORCAValidator.

    Notes
    -----
    The returned CompoundResult contains new CalculationResult
    instances. The original parsed result is not modified.

    Overall Compound termination is retained separately.

    Successful validation of an individual step does not necessarily
    imply that the overall Compound execution terminated normally.

    Examples
    --------
    >>> # parsed = ORCAParser.parse_compound(output_text)
    >>> # validated = ORCACompoundValidator.validate(
    >>> #     specs=[optimization_spec, tddft_spec],
    >>> #     compound=parsed,
    >>> #     text=output_text,
    >>> # )
    """

    @classmethod
    def validate(
        cls,
        specs: Sequence[CalculationSpec],
        compound: CompoundResult,
        text: str,
    ) -> CompoundResult:
        """
        Validate all steps of an ORCA Compound calculation.

        Parameters
        ----------
        specs : Sequence[CalculationSpec]
            Ordered scientific specifications corresponding to
            the Compound steps.

            The first specification describes Compound step 1,
            the second describes step 2, and so forth.

        compound : CompoundResult
            Parsed Compound calculation result.

        text : str
            Complete ORCA Compound standard-output text.

        Returns
        -------
        CompoundResult
            New Compound result containing independently validated
            scientific results for every step.

        Raises
        ------
        TypeError
            If inputs have unsupported types.

        ValueError
            If the number or indices of Compound steps do not
            correspond to the supplied specifications, or if a
            specification targets a code other than ORCA.

        Notes
        -----
        The following task-specific validation is currently supported:

        ``single_point``
            Requires a final-energy record.

        ``optimization``
            Requires a final-energy record and an explicit geometry
            convergence marker.

        ``excited_states``
            Requires a final-energy record and the requested number
            of singlet TDDFT roots.

        Individual step validation does not require the overall
        ORCA normal-termination marker.

        An optimization that satisfies its local convergence checks
        may therefore be reported as completed even when a later
        Compound step fails.

        The caller must consider the overall Compound termination
        status separately when deciding whether the execution as a
        whole was successful.
        """
        if not isinstance(specs, Sequence):
            raise TypeError(
                "specs must be an ordered sequence."
            )

        if not isinstance(compound, CompoundResult):
            raise TypeError(
                "compound must be a CompoundResult."
            )

        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        sections = ORCAParser.split_compound_steps(text)

        if len(specs) != len(compound.steps):
            raise ValueError(
                "Number of specifications does not match "
                "the number of parsed Compound steps."
            )

        if len(sections) != len(compound.steps):
            raise ValueError(
                "Number of output sections does not match "
                "the number of parsed Compound steps."
            )

        expected_indices = list(range(1, len(specs) + 1))

        parsed_indices = [
            step.index
            for step in compound.steps
        ]

        if parsed_indices != expected_indices:
            raise ValueError(
                "Compound step indices must be consecutive "
                "and start at 1."
            )

        if list(sections) != expected_indices:
            raise ValueError(
                "Output sections do not match the "
                "expected Compound step indices."
            )

        actual_termination = (
            "ORCA TERMINATED NORMALLY" in text
        )

        if actual_termination != compound.terminated_normally:
            raise ValueError(
                "Compound termination status is inconsistent "
                "with the supplied output text."
            )

        validated_steps = []

        for spec, step in zip(
            specs,
            compound.steps,
            strict=True,
        ):
            if not isinstance(spec, CalculationSpec):
                raise TypeError(
                    "Every specification must be a CalculationSpec."
                )

            if spec.code != "orca":
                raise ValueError(
                    f"Compound step {step.index} targets "
                    f"unsupported code {spec.code!r}."
                )

            step_text = sections[step.index]

            expected_roots = 5

            if spec.task == "excited_states":
                expected_roots = spec.code_options.get(
                    "nroots",
                    5,
                )

            report = ORCAValidator.inspect(
                text=step_text,
                task=spec.task,
                expected_roots=expected_roots,
                require_termination=False,
            )

            is_final_step = (
                step.index == len(compound.steps)
            )

            status = report.status
            additional_errors = []

            if (
                is_final_step
                and not actual_termination
                and status == "completed"
            ):
                status = "partial"
                additional_errors.append(
                    "Final Compound step has no confirmed "
                    "overall ORCA termination."
                )

            parsed_result = step.result

            metadata = dict(
                parsed_result.to_dict()["metadata"]
            )

            metadata["validation"] = {
                "terminated_normally": (
                    report.terminated_normally
                ),
                "energy_found": report.energy_found,
                "optimization_converged": (
                    report.optimization_converged
                ),
                "singlet_roots": report.singlet_roots,
                "triplet_roots": report.triplet_roots,
            }

            validated_result = CalculationResult(
                status=status,
                converged=report.optimization_converged,
                properties=parsed_result.to_dict()["properties"],
                units=parsed_result.to_dict()["units"],
                metadata=metadata,
                warnings=[
                    *parsed_result.warnings,
                    *report.warnings,
                ],
                errors=[
                    *parsed_result.errors,
                    *report.errors,
                    *additional_errors,
                ],
            )

            validated_steps.append(
                CompoundStepResult(
                    index=step.index,
                    result=validated_result,
                )
            )

        return CompoundResult(
            steps=tuple(validated_steps),
            terminated_normally=actual_termination,
        )