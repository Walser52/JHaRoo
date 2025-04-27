

#from jhr.codes.espresso.io import QEio
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv
from jhr.codes.espresso.study import QEChain

#from pathlib import Path

mat_file = "../input/relax/relax.in"
mat_file = "/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/jhr/scripts/inputfiles/relax/relax.in"
import os
print(os.getcwd())
mat_file = "./scripts/inputfiles/relax/relax.in"
# ------SCF/Relax-------
update = {}

#-------define calcs-------
#relax = QECalc(template=mat_file, code="qe/pw.x", files="scf", update=update, run=False)

from jhr.codes.espresso.io import PWParse

outfile = "/home/fahad/Documents/Work/repos/Abinitio-Codes/scripts/inputfiles/relax.out"



#convergence = QEConv(template=mat_file, parameters={"ecutwfc": [2, 4, 5], "ecutrho": [10, 20, 30]}, criteria="total energy", code="qe/pw.x")


#------modifications------
#relax.ase_hacks(remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True)
#for each_calc in convergence:
#  each_calc.ase_hacks(remove_ibrav=True, remove_cell_parameters=True, modify_atomic_positions=True)
#
#------create chain------

#chain = QEChain([relax, convergence])
#chain.run()
#

# relax.run()
# relax.find_converged and use it to update convergence template.








