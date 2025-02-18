import spglib
from ase import io


def Crystal():
  def __init__():
    return
  def from_cif(self, file):
    self.atoms = io.read(file)
    return

  def find_spacegroup():
    """
    """
    cell = (self.atoms.get_cell(), self.atoms.get_scaled_positions(), self.atoms.get_atomic_numbers())

    spacegroup = spglib.get_spacegroup(cell, symprec=1e-3)

    print("Detected Space Group:", spacegroup)
    return

