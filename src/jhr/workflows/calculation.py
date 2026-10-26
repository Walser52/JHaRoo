
from dataclasses import dataclass, field
from typing import Any, Literal

from ase import Atoms


CalculationType = Literal[
    "optimize",
    "single_point",
    "tddft",
    "frequencies",
]


@dataclass
class Calculation:
    """Describe a scientific calculation without executing it.

    Attributes
    ----------
    name:
        Human-readable calculation identifier.
    task:
        Scientific operation to perform.
    geometry:
        Initial atomic structure.
    method:
        Electronic-structure method.
    basis:
        Basis set.
    charge:
        Total molecular charge.
    multiplicity:
        Spin multiplicity (2S + 1).
    options:
        Additional calculation parameters.
    """

    name: str
    task: CalculationType
    geometry: Atoms

    method: str = "PBE0"
    basis: str = "def2-TZVP"

    charge: int = 0
    multiplicity: int = 1

    options: dict[str, Any] = field(default_factory=dict)
