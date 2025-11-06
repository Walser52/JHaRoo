from ase.build import bulk
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import LBFGS
from ase.io.espresso import write_espresso_in

rocksalt = bulk('NaCl', crystalstructure='rocksalt', a=6.0)

# Pseudopotentials from SSSP Efficiency v1.3.0
pseudopotentials = {'Na': 'na_pbe_v1.5.uspp.F.UPF', 'Cl': 'cl_pbe_v1.4.uspp.F.UPF'}

# Optionally create profile to override paths in ASE configuration:
profile = EspressoProfile(
    command='/path/to/pw.x', pseudo_dir='/path/to/pseudopotentials'
)

#calc = Espresso(profile=profile, pseudopotentials=pseudopotentials)

input_data = {
    'system': {'ecutwfc': 60, 'ecutrho': 480},
    'disk_io': 'low',  # Automatically put into the 'control' section
}

calc = Espresso(
    profile=profile
    pseudopotentials=pseudopotentials,
    tstress=True,  # deprecated, put in input_data
    tprnfor=True,  # deprecated, put in input_data
    input_data=input_data,
)

write('pw.in', atoms, input_data=input_data, format='espresso-in')

# Hubbard is not implemented in the write_espresso_in function, we can add it manually
additional_cards = ['HUBBARD (ortho-atomic)', 'U Mn-3d 5.0', 'U Ni-3d 6.0']

write(
    'pw_hubbard.in',
    atoms,
    input_data=input_data,
    additional_cards=additional_cards,
    format='espresso-in',
)

rocksalt.calc = calc

rocksalt.get_potential_energy()  # This will run a single point calculation

opt = LBFGS(rocksalt)

opt.run(fmax=0.005)  # This will run a geometry optimization using ASE's LBFGS algorithm

# Print lattice constant...
print((8 * rocksalt.get_volume() / len(rocksalt)) ** (1.0 / 3.0))
