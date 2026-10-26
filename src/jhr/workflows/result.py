
from dataclasses import dataclass, field
from typing import Any

from ase import Atoms


@dataclass
class Result:
    """Scientific outputs from a completed calculation.

    All energies use eV and geometries use Å.

    Parameters
    ----------
    calculation_name:
        Name of the calculation that produced these results.
    energy:
        Final electronic energy in eV, if available.
    geometry:
        Final atomic geometry, if available.
    properties:
        Additional scientific properties, such as excitation
        energies, oscillator strengths, or dipole moments.
        Each property must have a documented unit.
    """

    calculation_name: str

    energy: float | None = None
    geometry: Atoms | None = None

    properties: dict[str, Any] = field(default_factory=dict)

    def get(self, name: str, default=None):
        """Retrieve an additional scientific property."""
        return self.properties.get(name, default)
