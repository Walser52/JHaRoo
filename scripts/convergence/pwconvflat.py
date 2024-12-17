# Run convergence over several parameters. 

from jhr.convergers.base import QEConverger
from jhr.io.modifiers import QEModifier
from jhr.io.base import QEio



mat_file = 'sample2.json'
prefix = 'CsPbI3'

def converge(template, parameters, valuesets, code, label, tolerance):
  conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)
  saved_files = conv.prepare_variants(template, parameters, valuesets, code, label = label)
  conv_val = conv.run_conv_one(files = saved_files, code = code, tolerance = tolerance)
  return conv_val



#Convergence parameters 1
label = 'ecutwfc'
parameters = ['ecutwfc']
valuesets=[5,6,8]
code = 'pw.x'
ext = 'in'
name = f'{prefix}{label}'
tolerance = 0.001

template = QEio.from_flat_JSON(mat_file)

#Convergence ecutwfc
conv_val = converge(template, parameters, valuesets, code, label, tolerance)

# update template.
template[parameters[0]] = conv_val

# Second convergence
label = 'degauss'
parameters = ['degauss']
valuesets=[0.1,0.2,0.3]
code = 'pw.x'
ext = 'in'
name = f'{prefix}{label}'
tolerance = 0.001

#Converge second
conv_val = converge(template, parameters, valuesets, code, label, tolerance)

# Restart option?
# Converge on kpts
# Run without convergence? 
  # Verify nscf runs. => Basher.runcommand('pw.x < input > output')
  # Verify bands. => Basher.runcommand('pw.x < input > output')
  # Verify DOS. => Basher.runcommand('pw.x < input > output')


# ====
# Verify for ph.x
