from ase.io import read

# Read the POSCAR file
atoms = read('POSCAR')
pbc = [1,1,1]
crystal_coordinates = True
# Access information


matdict = {'cell':      atoms.get_cell(), 
           'positions': atoms.get_positions(), 
           'atoms':     ''.join(atoms.get_chemical_symbols()),
           'pbc'  :     pbc,
#          'crystal_coordinates': crystal_coordinates
}


# Create a study object
# Create variants in relevant folder.

#=============


