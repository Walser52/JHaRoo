# Run a single computation using the study base classes.
#from jhr.codes.espresso.io import QEModifier
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv

mat_file = "sample-scf.json"
update = {}



scf_conv = QEConv(mat_file, parameters = {'ecutwfc': [2,4,5]}, code = 'qe/pw.x', criteria="total energy")

for each_calc in scf_conv:
    each_calc.ase_hacks(
        remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True
    )
scf_conv.run(check_conv = True, conv_threshold = 1e-6, break_on_conv = True)
