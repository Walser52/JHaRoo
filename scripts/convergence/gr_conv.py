# Run convergence over several parameters. 

from jhr.convergers.base import QEConverger
from jhr.io.modifiers import QEModifier
from jhr.io.base import QEio



mat_file = 'gr.json'
prefix = 'gr'
ase_hacks = False

def converge(template, parameters, valuesets, code, label, tolerance):
  conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)
  saved_files = conv.prepare_variants(template, parameters, valuesets, code, label = label, ase_hacks = False)
  conv_val = conv.run_conv_one(files = saved_files, code = code, tolerance = tolerance)
  return conv_val



#Convergence parameters 1
label = 'ecutwfc'
parameters = ['ecutwfc']
valuesets=[45, 50, 55]
code = 'pw.x'
ext = 'in'
name = f'{prefix}{label}'
tolerance = 0.001

template = QEio.from_flat_JSON(mat_file)
conv_val = converge(template, parameters, valuesets, code, label, tolerance)

# update template.
if conv_val is None: template[parameters[0]] = valuesets[-1]
else: template[parameters[0]] = conv_val



# # Second convergence
# label = 'degauss'
# parameters = ['degauss']
# valuesets=[0.1,0.2,0.3]
# code = 'pw.x'
# ext = 'in'
# name = f'{prefix}{label}'
# tolerance = 0.001

# conv_val = converge(template, parameters, valuesets, code, label, tolerance)


from jhr.io.base import Basher

Basher.runcommand('pw.x < nscf.in > nscf.out')
Basher.runcommand('bands.x < bands.in > bands.out')
# Basher.runcommand('dos.x < dos.in > dos.out')
# Restart option?
# Converge on kpts
# Run without convergence? 
  # Verify nscf runs. => Basher.runcommand('pw.x < input > output')
  # Verify bands. => Basher.runcommand('pw.x < input > output')
  # Verify DOS. => Basher.runcommand('pw.x < input > output')
# Create logger. 

# ====
# Verify for ph.x
