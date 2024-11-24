from ase.io.espresso import write_espresso_in
from ase import Atoms
from ase.io import write
d = 1.1
atoms = Atoms('CO', positions=[(0, 0, 0), (0, 0, d)])


input_data = {
    'calculation': 'relax',
    'restart_mode': 'from_scratch',
    'tprnfor': True,
    'etot_conv_thr': 1e-5,
    'forc_conv_thr': 1e-4,
    'ecutwfc': 60,
    'ecutrho': 480,
    'input_dft': 'rpbe',
    'vdw_corr': 'dft-d3',
    'occupations': 'smearing',
    'degauss': 0.01,
    'smearing': 'cold',
    'conv_thr': 1e-8,
    'mixing_mode': 'local-TF',
    'mixing_beta': 0.35,
    'diagonalization': 'david',
    'ion_dynamics': 'bfgs',
    'bfgs_ndim': 6,
    'startingwfc': 'random',
}  # This flat dictionary will be converted to a nested dictionary where, for example, "calculation" will be put into the "control" section

#write('pw.in', atoms, input_data=input_data, format='espresso-in')

# Hubbard is not implemented in the write_espresso_in function, we can add it manually
additional_cards = ['HUBBARD (ortho-atomic)', 'U Mn-3d 5.0', 'U Ni-3d 6.0']

#write(
#    'pw_hubbard.in',
#    atoms,
#    input_data=input_data,
#    additional_cards=additional_cards,
#    format='espresso-in',
#)

with open('pw_hubbard.in', "w") as fd:
  write_espresso_in(
      fd,
      atoms = atoms,
      pseudopotentials = {'O': 'abc', 'C': 'def'},
      input_data=input_data,
      additional_cards=additional_cards,
  #    format='espresso-in',
  )

#  if additional_cards:
#    if isinstance(additional_cards, list):
#        additional_cards = "\n".join(additional_cards)
#        additional_cards += "\n"
#
#    fd.write(additional_cards)
