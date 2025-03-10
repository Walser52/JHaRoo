from jhr.codes.espresso.io import QEio
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv
from jhr.codes.espresso.study import QEChain

mat_file = "sample-scf.json"

# ------SCF/Relax-------
update = {}

#-------define calcs-------
relax = QECalc(template=mat_file, code="pw.x", files="scf", update=update, run=False)
convergence = QEConv(template=mat_file, parameters={"ecutwfc": [2, 4, 5], "ecutrho": [10, 20, 30]}, criteria="total energy", code="qe/pw.x")


#------modifications------
relax.ase_hacks(remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True)
for each_calc in convergence:
  each_calc.ase_hacks(remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True)

#------create chain------

chain = QEChain([relax, convergence])
chain.run()









