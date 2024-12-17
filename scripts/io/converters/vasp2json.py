from ase.io import read

# Read the POSCAR file
atoms = read('POSCAR')

# Access information


matdict = {'cell':      atoms.get_cell(), 
           'positions': atoms.get_positions(), 
           'atoms':     ''.join(atoms.get_chemical_symbols())

}


[print(p) for p in dir(atoms)]
#=============


