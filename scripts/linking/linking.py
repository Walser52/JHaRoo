#Take the output of calc1 (e.g. vcrelax.out)
#Use it to update calc2 (e.g. scf.in)



#from jhr.codes.espresso.io import QEio
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv
from jhr.codes.espresso.study import QEChain

#Case I: Out file is there but calculation doesn't need running.
#out_file = #vc relax


#Templates to use
relax_in = 'relax.in'
scf_in = 'scf.in'
nscf_in = 'nscf.in'

update = {}


#Case II: Calc1 needs running to generate out file
relax = QECalc(template=relax_in, 
              code="qe/pw.x", 
              files="relax", 
              update=update, run=False)

scf = QECalc(template=scf_in, 
            code="qe/pw.x", 
            files="scf", 
            update=update, run=False)

nscf = QECalc(template=nscf_in, 
              code="qe/pw.x", 
              files="nscf", 
              update=update, run=False)

#link1 = QELinker(link = 'atomic_positions', source = relax, target = [scf, nscf])

 
#chain = QEChain([relax, scf, nscf]) 

#chain.link()
#
chain.run()
#

#Case III: There is no chain. Simply connect files (if needed)

