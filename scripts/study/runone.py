# Run a single computation using the study base classes.
from jhr.codes.espresso.io import QEio, QEModifier
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc


#SCF
mat_file = "sample-scf.json"
code = "pw.x"
update = {}


scf = QECalc(
    template=mat_file, code=code, files="scf", update=update, run=False
)
scf.ase_hacks(
    remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True
)
scf.run()
