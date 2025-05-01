import numpy as np
import re


def KS_states(file):
    with open(file, 'r') as file:
        for line in file:
            if "number of Kohn-Sham states=" in line:
                KS_states = line.split('=')[1].strip()
                
                return int(KS_states)  


def extract_values(file, keywords, num_KS_states):
    with open(file, 'r') as file:
        text = file.read()
        
    arrays={}
    
    for keyword in keywords:
        parts = text.split(keyword)
        print(f"Found {len(parts)-1} occurrences of {keyword}")
        numbers = []
        for part in parts[1:]:
            lines = part.splitlines()
            
            values = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                for word in line.split():
                    try:
                        values.append(float(word))
                        if len(values) == num_KS_states:
                            break
                    except ValueError:
                        continue
                if len(values) == num_KS_states:
                    break
            numbers.append(np.array(values))
            arrays[keyword] = numbers
    return arrays
        
        
file = 'pwscf.out'    
keywords = ['k = ', 'bands (ev):', 'occupation numbers']
num_KS_states = KS_states(file)
print(f'KS_states: {num_KS_states}')

keyword_array = extract_values(file, keywords, num_KS_states)

for key in keyword_array:
    print(f"\n Result for {key}:")
    print(keyword_array[key][9])
        
    
    
bands_blocks = keyword_array['bands (ev):']
occs_blocks = keyword_array['occupation numbers']

# Flatten all occupied band energies where occupation == 1.0
occupied_bands = [
    b
    for bands, occs in zip(bands_blocks, occs_blocks)
    for b, o in zip(bands, occs)
    if o == 1.0
]

if occupied_bands:
    max_occupied = max(occupied_bands)
    print(f'Global maximum of occupied bands (VBM): {max_occupied} ev')
else:
    print("\nNo occupied bands found with occupation = 1.0.")
    
