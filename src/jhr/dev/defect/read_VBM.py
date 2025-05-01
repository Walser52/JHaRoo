import numpy as np
import re

from jhr.codes.espresso.io import QEOutParser


file = "../../../../../jhr/data/outfiles/scf/pwscf.out"        

prs = QEOutParser('pw.x')
df = prs.parser.Process(file)
array_dict = prs.parser.band_occupancy(file)

#print(array_dict.keys())

occ =    array_dict['occupancy_array'] 
bands =    array_dict['bands_array'] 

occ = np.where(occ > 0.9, 1, 0)
bocc = bands*occ
print("VBM: ", bocc.max())



#bands_blocks = array_dict['bands (ev):']
#occs_blocks = array_dict['occupation numbers']
#
## Flatten all occupied band energies where occupation == 1.0
#occupied_bands = [
#    for bands, occs in zip(bands_blocks, occs_blocks)
#    for b, o in zip(bands, occs)
#    if o == 1.0
#]
#
#if occupied_bands:
#    max_occupied = max(occupied_bands)
#    print(f'Global maximum of occupied bands (VBM): {max_occupied} ev')
#else:
#    print("\nNo occupied bands found with occupation = 1.0.")
#    
