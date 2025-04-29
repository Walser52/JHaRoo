#Take the output of calc1 (e.g. vcrelax.out)
#Use it to update calc2 (e.g. scf.in)


#Case I: Out file is there but calculation doesn't need running.
out_file = #vc relax

calc1 = QECalc(run = False)
calc2 = QECalc() 

QEChain = []


#Case II: Calc1 needs running to generate out file

#Case III: There is no chain. Simply connect files (if needed)

