import numpy as np
import re

from jhr.codes.espresso.io import QEOutParser


file = "pwscf copy.out"        

prs = QEOutParser('pw.x')
df = prs.parser.Process(file)
array_dict = prs.parser.band_occupancy(file)
Fermi = df.loc['Fermi_energy'][0]
print(Fermi)
#print(array_dict.keys())

occ =    array_dict['occupancy_array'] 
bands =    array_dict['bands_array'] 


VBM = np.max(bands[bands < Fermi])
CBM = np.min(bands[bands > Fermi])

print("VBM:", VBM)
print("CBM:", CBM)

