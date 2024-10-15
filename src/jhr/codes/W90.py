#Routines for Wannier 90
import numpy as np

def readSpread(file_path):
    """Read wannier function spread from W90 output file."""

    start_marker = 'Final State' 
    end_marker = 'Sum of centres'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    collecting = False
    last_numbers = []

    for line in lines:
        if start_marker in line:
            collecting = True
            continue  # Skip the start marker line
        if end_marker in line:
            collecting = False
            continue  # Stop before the end marker

        if collecting:
            # Split the line and get the last element, which is the number
            last_number = line.strip().split()[-1]  # Get the last element
            last_numbers.append(float(last_number))

    return last_numbers

# This reads the hamiltonian elements for a specific unit cell coordinate.  
# Wannier90 reports them by unit cell (x,y,z, i,j) where (1,0,0, 1,1) is the overlap of
# wavefunction 1 in the 0,0,0 cell with wavefunction 1 translated by one unit cell in the x direction.
def GetOneCell(hr, x,y,z, num_basis = 12 ):
    hrtrim = hr[(hr[:,0]==x) & (hr[:,1]==y) & (hr[:,2]==z)]
    hrtrim = hrtrim[:,3:]
    H = np.zeros((num_basis,num_basis), dtype='complex')
    for r in hrtrim[:]:
        i = int(r[0])-1
        j = int(r[1])-1
        overlap = complex(r[2], r[3])
        H[i, j] = overlap
    return H

def GetHomePlusNeighbors(hr, num_basis = 12):
    # Get contribution from six nearest neighbors

    H = GetOneCell(hr, 0,0,0, num_basis = num_basis)

    H += GetOneCell(hr, 1,0,0, num_basis = num_basis)
    H += GetOneCell(hr, 0,1,0, num_basis = num_basis)
    H += GetOneCell(hr, 0,0,1, num_basis = num_basis)
    H += GetOneCell(hr, -1,0,0, num_basis = num_basis)
    H += GetOneCell(hr, 0,-1,0, num_basis = num_basis)
    H += GetOneCell(hr, 0,0,-1, num_basis = num_basis)

    return H

def GetAllContributions(hr, num_basis = 12):
    # Now build it using every element.
    H = np.zeros((num_basis,num_basis), dtype='complex')
    for r in hr[:]:
        x = int(r[0])
        y = int(r[1])
        z = int(r[2])
        i = int(r[3])-1
        j = int(r[4])-1
        overlap = complex(r[5], r[6])
        H[i, j] += overlap

#    print(eig(H)[0])

    return H


