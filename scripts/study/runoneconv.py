# Run a single computation using the study base classes.
from jhr.codes.espresso.io import QEio, QEModifier
from jhr.codes.espresso.study import BaseQEConvergenceCalculation

mat_file = "sample-scf.json"
template = QEio.from_flat_JSON(mat_file)

code = "pw.x"
update = {}
files = ["scf.in", "scf.out"]


calc1 = BaseQEConvergenceCalculation(template, parameters = {'ecutwfc': [2,4,5], 'ecutrho': [1,2,3]}, code = 'pw.x')

#======
#Figure if convergence is done 
# During run: check_convergence.
# 	Pass function to check convergence 

# Convergence param: 

# Read_TotalEnergy(fromfile = '', code = 'pw.x')


# Run:
##	Loop over calculations
##		Call calc.run()
##		Call check-convergence(conv_func, *arguments)



## conv_func(filetoread, whattoread, wheretowrite, threshold):
##	read filetoread
##	extract whatoread
##	write wheretowrite

##	see if threshold is met
