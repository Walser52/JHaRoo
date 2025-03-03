# Run a single computation using the study base classes.
from jhr.codes.espresso.io import QEio, QEModifier
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv

mat_file = "sample-scf.json"
code = "pw.x"
update = {}



scf_conv = QEConv(mat_file, parameters = {'ecutwfc': [2,4,5], 'ecutrho': [10,20,30]}, code = 'pw.x')

for each_calc in scf_conv:
    each_calc.ase_hacks(
        remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True
    )
scf_conv.run()
