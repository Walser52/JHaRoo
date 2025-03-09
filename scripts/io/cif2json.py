from jhr.io.base import FileHandler
from jhr.codes.espresso.io import QEFileHandler as FH




FH().qeinput2json(file_in = 'pwscf.in', file_out = 'scf.json', update = {'crystal_coordinates' : True})




    
    


#==============
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc
mat_file = "scf.json"
code = "qe/pw.x"
update = {}


scf = QECalc(
    template=mat_file, code=code, files="scf", update=update, run=False
)

scf.run()

