from jhr.core.study import Calculation
from jhr.codes.espresso.io import QEio, QEModifier

mat_file = 'sample-scf.json'
template = QEio.from_flat_JSON(mat_file)

calc1 = Calculation(template = template, code = 'qe/pw.x', mode = 'normal', files = ['scf.in', 'scf.out'], run = False)

