from ase import Atoms

symbols = 'CC'
atoms_dict = {'positions': [[0.333333333, 0.666666666, 0.5, 0, 0, 0], [0.666666666, 0.333333333, 0.4]]}


atoms_dict['positions'] = [site[0:3] for site in atoms_dict['positions']]

print(atoms_dict)
atoms = Atoms(symbols, **atoms_dict)

