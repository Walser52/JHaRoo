# Reads a cif
# Creates a supercell
# Removes atoms according to requirement

from ase.io import read, write
from ase.build import make_supercell

#_____________Create supercell______________
# Load the CIF file into an ASE Atoms object
structure = read("../../data/cif/CsPbI3.cif")  # Replace 'structure.cif' with your file name
transformation_matrix = [
    [2, 0, 0],  # Scale in the x-direction
    [0, 2, 0],  # Scale in the y-direction
    [0, 0, 2]   # Scale in the z-direction
]

# Create the supercell
supercell = make_supercell(structure, transformation_matrix)
write("supercell.cif", supercell)


#____________Symmetry reduction_________ (Delete unnecessary atoms)



#___________Create espresso input/Relaxation/Convergence_______
    #_________Create input______
    #_________Verify threshold met or not_____







## Create QE file
## Relaxation
## Convergence tests



