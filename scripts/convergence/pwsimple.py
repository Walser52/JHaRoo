from ase.io.espresso import write_espresso_in
from ase import Atoms


# Working: sample3.json============
# matdict = {"template": 
#   {"calculation": "scf", 
#     "pseudo_dir": "../pseudo/", 
#     "outdir": "../tmp/", 
#     "prefix": "CsPbI3", 
#     "a": 6.27514229,
#     "nat": 3, "ntyp": 3, 
#     "space_group": 221, 
#     "occupations": "smearing", 
#     "smearing": "cold", 
#     "degauss": 0.0146997236, 
#     "ecutwfc": 5, 
#     "conv_thr": 1e-06}, 
# "atoms": "CsPbI", 
# "pseudopotentials": {"Cs": "C.pbe-n-rrkjus_psl.0.1.UPF", 
#                       "Pb": "C.pbe-n-rrkjus_psl.0.1.UPF", 
#                       "I": "C.pbe-n-rrkjus_psl.0.1.UPF"}, 
# "kpts": [2,2,2], 
# "cell": [1, 1, 1], 
# "pbc": [1, 1, 1], 
# "positions": [[0.5, 0.5, 0.5], 
#               [0,   0,  0],
#               [0,   0,  0.5]], 
# "crystal_coordinates": True
# }

# atoms = Atoms(matdict['atoms'], 
#         positions = matdict['positions'], 
#         cell  = matdict['cell'], 
#         pbc   = matdict['pbc']
#         )
# print(atoms)
# ase_dict = dict(atoms = atoms, 
#                 crystal_coordinates = matdict['crystal_coordinates'], 
#                 pseudopotentials   = matdict['pseudopotentials'], 
#                 kpts               = matdict['kpts'])
# template = matdict['template']
# +++++++++++++++++++++++++++++++++++++++++++++++

# NOT Working: sample2.json=================
template = {"calculation": "scf", 
    "pseudo_dir": "../pseudo/", 
    "outdir": "../tmp/", 
    "prefix": "CsPbI3", 
    "a": 6.27514229,
    "nat": 3, "ntyp": 3, 
    "space_group": 221, 
    "occupations": "smearing", 
    "smearing": "cold", 
    "degauss": 0.0146997236, 
    "ecutwfc": 5, 
    "conv_thr": 1e-06, 

    "atoms": "CsPbI", 
    "pseudopotentials": {"Cs": "C.pbe-n-rrkjus_psl.0.1.UPF", 
                      "Pb": "C.pbe-n-rrkjus_psl.0.1.UPF", 
                      "I": "C.pbe-n-rrkjus_psl.0.1.UPF"}, 
    "kpts": [2,2,2], 
    "cell": [1, 1, 1], 
    "pbc": [1, 1, 1], 
    "positions": [[0.5, 0.5, 0.5], 
              [0,   0,  0],
              [0,   0,  0.5]], 
    "crystal_coordinates": true
}

atoms = Atoms(template['atoms'], 
                positions = template['positions'], 
                cell  = template['cell'], 
                pbc   = template['pbc']
                )
ase_dict =  {'atoms': atoms, 
            'pseudopotentials': template['pseudopotentials'], 
            'kpts': template['kpts'], 
            'crystal_coordinates': template['crystal_coordinates'] }
[template.pop() for p in ['atoms', 'kpts', 'crystal_coordinates']]
#+++++++++++++++++++++++++++++++++++++++++++


with open('sample.in', 'w') as fd:
    write_espresso_in(
        fd,
        input_data=template,
        **ase_dict
        # additional_cards=additional_cards,
        # format='espresso-in',
    )




# matdict = {"calculation": "scf", 
#     "pseudo_dir": "../pseudo/", 
#     "outdir": "../tmp/", 
#     "prefix": "CsPbI3", 
#     "a": 6.27514229,
#     "nat": 3, "ntyp": 3, 
#     "space_group": 221, 
#     "occupations": "smearing", 
#     "smearing": "cold", 
#     "degauss": 0.0146997236, 
#     "ecutwfc": 5, 
#     "conv_thr": 1e-06, 

#     "atoms": "CsPbI", 
#     "pseudopotentials": {"Cs": "C.pbe-n-rrkjus_psl.0.1.UPF", 
#                       "Pb": "C.pbe-n-rrkjus_psl.0.1.UPF", 
#                       "I": "C.pbe-n-rrkjus_psl.0.1.UPF"}, 
#     "kpts": [2,2,2], 
#     "cell": [1, 1, 1], 
#     "pbc": [1, 1, 1], 
#     "positions": [[0.5, 0.5, 0.5], 
#               [0,   0,  0],
#               [0,   0,  0.5]], 
#     "crystal_coordinates": true
# }
# atoms = Atoms(matdict['atoms'], 
#         positions = matdict['positions'], 
#         cell  = matdict['cell'], 
#         pbc   = matdict['pbc']
# 
# 
#         )
# atoms = 
# ase_dict = {'atoms': Atoms(symbols='CsPbI', pbc=True, cell=[1.0, 1.0, 1.0]), 
#             'pseudopotentials': {'Cs': 'C.pbe-n-rrkjus_psl.0.1.UPF', 'Pb': 'C.pbe-n-rrkjus_psl.0.1.UPF', 'I': 'C.pbe-n-rrkjus_psl.0.1.UPF'}, 
#             'kpts': [2, 2, 2], 
#             'crystal_coordinates': True}
# template = {'calculation': 'scf', 'pseudo_dir': '../pseudo/', 'outdir': '../tmp/', 'prefix': 'CsPbI3', 'a': 6.27514229, 'nat': 3, 'ntyp': 3, 'space_group': 221, 'occupations': 'smearing', 'smearing': 'cold', 'degauss': 0.0146997236, 'ecutwfc': 5, 'conv_thr': 1e-06, 'atoms': 'CsPbI', 'cell': [1, 1, 1], 'pbc': [1, 1, 1], 'positions': [[0.5, 0.5, 0.5], [0, 0, 0], [0, 0, 0.5]]}
