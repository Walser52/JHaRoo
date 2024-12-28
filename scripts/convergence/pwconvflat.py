# Run convergence over several parameters. 




from jhr.convergers.base import QEConverger
from jhr.io.modifiers import QEModifier
from jhr.io.base import QEio

#=======================INPUTS=====================

mat_file = 'sample-scf.json'
prefix = 'CsPbI3'

def converge(template, parameters, valuesets, code, label, tolerance, output_file, check_convergence):
  conv = QEConverger(parameters = parameters, valuesets = valuesets, template = template)   #Create converger object
  saved_files = conv.prepare_variants(template, parameters, valuesets, code, label = label) #Prepare input files for convergences
  conv_val = conv.run_conv_one(files = saved_files, code = code, 
             tolerance = tolerance, output_file = output_file, check_convergence = check_convergence)     #Run convergence and find converged value
  return conv_val                                                                           


conv_dict1 = dict(label = 'ecutwfc',         #label to use for convergence input files
                parameters = ['ecutwfc'],   #parameters on which to converge
                output_file = 'ecutwfc_conv',
                valuesets=[5,6,8],          #convergence values
                tolerance = 0.001)

conv_dict2 = dict(label = 'degauss',          #label to use for convergence input files
                  parameters = ['degauss'],   #parameters on which to converge
                  output_file = 'degauss_conv',
                  valuesets=[0.1,0.2,0.3],          #convergence values
                  tolerance = 0.001)

#conv_dict3 = dict(label = 'kpts',          #label to use for convergence input files
#                  parameters = ['kpts'],   #parameters on which to converge
#                  valuesets=[[1,1,1], [2,2,2]],          #convergence values
#                  tolerance = 0.001)
#

#=================================================

template = QEio.from_flat_JSON(mat_file)


#conv_val = converge(template, code = 'pw.x', check_convergence= False, **conv_dict1)  #Convergence 1: ecutwfc
#template[conv_dict1['parameters'][0]] = conv_val            #update template with converged value
#conv_val = converge(template, code = 'pw.x', check_convergence= False, **conv_dict2)  #Convergence 2: degauss
#template[conv_dict2['parameters'][0]] = conv_val            #update template with converged value
#conv_val = converge(template, code = 'pw.x', **conv_dict3)  #Convergence 3: kpoints


#====================NSCF==============
#Run nscf
from ase.io.espresso import read_espresso_in, write_espresso_in
mat_file = 'sample-nscfbands.json'
prefix = 'CsPbI3'
template = QEio.from_flat_JSON(mat_file)

print(template)
#write espresso file
write_espresso_in('nscfinp.in', input_data = template, **ase_dict)

# Restart option?
# Converge on kpts
# Run without convergence? 
  # Verify nscf runs. => Basher.runcommand('pw.x < input > output')
  # Verify bands. => Basher.runcommand('pw.x < input > output')
  # Verify DOS. => Basher.runcommand('pw.x < input > output')


# ====
# Verify for ph.x
