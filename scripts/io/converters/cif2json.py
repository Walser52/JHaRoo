#load a cif file in ase. 
#

from ase import io

path = "../../../data/cif/CsPbI3.cif"
template = {}

# Load the CIF file
atoms = io.read(path)

# Print atomic positions
print(atoms)

# Get atomic symbols and positions
print("Atomic symbols:", atoms.get_chemical_symbols())
print("Atomic positions:\n", atoms.get_positions())

# Get lattice vectors
print("Lattice vectors:\n", atoms.get_cell())

template["prefix"] = atoms 
template["positions"] = atoms.get_positions()

