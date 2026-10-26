"""
Result containers for ORCA Compound calculations.

ORCA Compound calculations may execute multiple logical scientific
calculations through one invocation of the ORCA executable.

This module represents their results without combining distinct
scientific operations into a single CalculationResult.

Each Compound step has an independent scientific result, while
the CompoundResult records the overall execution structure.

These containers do not own raw output files or perform parsing.
"""

from __future__ import annotations

from dataclasses import dataclass

from jhr.core.calculation import CalculationResult


@dataclass(frozen=True)
class CompoundStepResult:
    """
    Associate a scientific result with an ORCA Compound step.

    Parameters
    ----------
    index : int
        One-based step index reported by ORCA.

    result : CalculationResult
        Structured scientific result associated with the step.

    Raises
    ------
    TypeError
        If index is not an integer or result is not a
        CalculationResult.

    ValueError
        If index is not positive.

    Notes
    -----
    The index identifies a step within the Compound execution.

    It is not a globally unique calculation identifier.

    Scientific names such as ``"S0_opt"`` can eventually be associated
    with steps using their original CalculationSpec objects.
    """

    index: int
    result: CalculationResult

    def __post_init__(self) -> None:
        """Validate the Compound step index and scientific result."""
        if type(self.index) is not int:
            raise TypeError("index must be an integer.")

        if self.index < 1:
            raise ValueError("index must be positive.")

        if not isinstance(self.result, CalculationResult):
            raise TypeError(
                "result must be a CalculationResult."
            )


@dataclass(frozen=True)
class CompoundResult:
    """
    Represent the results of one ORCA Compound execution.

    Parameters
    ----------
    steps : tuple[CompoundStepResult, ...]
        Ordered scientific results belonging to the Compound job.

    terminated_normally : bool
        Whether ORCA reported normal termination of the overall
        Compound execution.

    Notes
    -----
    Normal execution termination and scientific success are separate.

    For example, a Compound job may terminate normally even if
    a geometry optimization did not satisfy convergence criteria.

    Each step must therefore be validated independently.

    The container does not infer scientific completion from the
    overall termination marker.

    Examples
    --------
    >>> result = CompoundResult(
    ...     steps=(
    ...         CompoundStepResult(
    ...             index=1,
    ...             result=CalculationResult(status="partial"),
    ...         ),
    ...     ),
    ...     terminated_normally=True,
    ... )
    >>> result.step(1).status
    'partial'
    """

    steps: tuple[CompoundStepResult, ...]
    terminated_normally: bool

    def __post_init__(self) -> None:
        """
        Validate the Compound result structure.

        Raises
        ------
        TypeError
            If steps or terminated_normally have invalid types.

        ValueError
            If steps are missing, duplicated, or out of order.
        """
        if not isinstance(self.steps, tuple):
            raise TypeError("steps must be a tuple.")

        if not self.steps:
            raise ValueError(
                "CompoundResult requires at least one step."
            )

        indices = []

        for step in self.steps:
            if not isinstance(step, CompoundStepResult):
                raise TypeError(
                    "Every step must be a CompoundStepResult."
                )

            indices.append(step.index)

        if indices != sorted(set(indices)):
            raise ValueError(
                "Compound step indices must be unique and ordered."
            )

        if type(self.terminated_normally) is not bool:
            raise TypeError(
                "terminated_normally must be a boolean."
            )

    def step(self, index: int) -> CalculationResult:
        """
        Retrieve the scientific result for a Compound step.

        Parameters
        ----------
        index : int
            One-based ORCA Compound step index.

        Returns
        -------
        CalculationResult
            Scientific result associated with the requested step.

        Raises
        ------
        KeyError
            If the requested step does not exist.
        """
        for item in self.steps:
            if item.index == index:
                return item.result

        raise KeyError(
            f"Compound step {index} does not exist."
        )