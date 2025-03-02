from jhr.codes.espresso.study import QEChain
from jhr.codes.espresso.study import BaseQENormalCalculation
from jhr.codes.espresso.study import BaseQEConvergenceCalculation
from jhr.codes.espresso.io import QEio

mat_file = "sample-scf.json"
template = QEio.from_flat_JSON(mat_file)


#Change 1: 
#Read the template from the file or pass explicitly
#If template is a "string" instead of dictionary then treat it as a path

if not isinstance(template, dict): #template maybe a path
    QEio.from_flat_JSON(template) 

#Change 2:
#For output
#for files:
# if no file is given
if file is None:
    try:
        file_in = template['prefix']+'.in'
        file_out = template['prefix']+'.out'
    except:
        raise Exception("Couldn't read prefix from template. Consider adding 'prefix' to template or provide file name(s) for io files")
elif isinstance(file, str):
    file_in = file+'.in'
    file_out = file+'.out'
elif isinstance(file, list):
    file_in = file[0]
    file_out = file[1]


#------Calc 1-------
code = "pw.x"
update = {}
files = ["scf.in", "scf.out"]

scf = BaseQENormalCalculation(template, code, update=update, files=files, run=False) 


#------Calc 2-------
convergence = BaseQEConvergenceCalculation(template, parameters = {'ecutwfc': [2,4,5], 'ecutrho': [1,2,3]}, code = 'pw.x')

#-----Chain-------
calcs = [scf, convergence]


chain = QEChain(calcs)
chain.run()
