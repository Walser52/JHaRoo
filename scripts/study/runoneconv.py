# Run a single computation using the study base classes.
from jhr.codes.espresso.io import QEio, QEModifier
from jhr.codes.espresso.study import BaseQEConvergenceCalculation

mat_file = "sample-scf.json"
template = QEio.from_flat_JSON(mat_file)

code = "pw.x"
update = {}
files = ["scf.in", "scf.out"]


calc1 = BaseQEConvergenceCalculation(template, parameters = {'ecutwfc': [2,4,5]}, code = 'pw.x')

