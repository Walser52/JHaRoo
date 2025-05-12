from jhr.codes.espresso.io import QEOutParser
from jhr.io.linkers import QELinker
from jhr.codes.espresso.study import BaseQENormalCalculation as QECalc
from jhr.codes.espresso.study import BaseQEConvergenceCalculation as QEConv
from jhr.codes.espresso.study import QEChain

#prs = QEOutParser('pw.x')
#file = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/jhr/scripts/study/scf.out'
#df = prs.parser.Process(file)
#
#pos = prs.parser.atomic_positions()
#print(pos)
relax_in = 'relax.in'
scf_in = 'scf.in'
nscf_in = 'nscf.in'

update = {}

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


from jhr.io.linkers import Linker
#chain = QEChain([relax, scf, nscf]) 

#chain = QEChain([relax, scf, nscf]) 
#chain.run()

qelink = QELinker(link = 'atomic_positions', source = relax, target = [scf, nscf])
relax.parser.outparser.Process()
qelink.link()


