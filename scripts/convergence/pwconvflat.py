# Run convergence over several parameters. 

from jhr.convergers.base import QEConverger
from jhr.io.modifiers import QEModifier
from jhr.io.base import QEio



mat_file = 'sample2.json'
prefix = 'CsPbI3'



#Convergence parameters 1
label = 'ecutwfc'
parameters = ['ecutwfc']
valuesets=[5,6,8]
code = 'pw'
ext = 'in'
name = f'{prefix}{label}'


all_conv_parameters = [['ecutwfc'], ['ecutrho']]
all_conv_valuesets = [[1,2,3], [4,5,6]]

template = QEio.from_flat_JSON(mat_file)

#Convergence ecutwfc
conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)
saved_files = conv.prepare_variants(template, parameters, valuesets, code)
conv_val = conv.run_conv_one(files = saved_files, code = 'pw.x')
print(conv_val)

#find converged value


#Converge second

