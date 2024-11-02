#Routines for Wannier 90
import numpy as np

def readSpread(files):
    """Read wannier function spread from W90 output file.
    Args:
      files: List of files. Could be one file path as well.

    Returns: 
      spreads_All: List of spreads. 

    """
    if type(files) is not list: files = [files]


    start_marker = 'Final State' 
    end_marker = 'Sum of centres'

    spreads_all = []

    for file_path in files:
      with open(file_path, 'r') as file:
          lines = file.readlines()

      collecting = False
      spreads = []

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
              spreads.append(float(last_number))
      spreads_all.append(spreads)

    return spreads_all

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

def GetTBHam(datfiles, num_basis, getfor = 'neighbors', verbose = False):
  """
  Convenience function for processing a list of hr.dat files. 
  Args:
    datfiles: List of _hr.dat files from W90.
    getfor (str) or list/tuple: 'neighbors', 'all'. Note that 'neighbors' is going to include [0,0,0] too. 
                                For home or any other cell, just pass [0,0,0] or corresponding cell list. 
    verbose (bool): Prints eigenvalues.
  Returns: 
    H_all: list of hamiltonians for datfiles passed. 
  """
  
  H_all = []
  for f in datfiles:
    hr = np.genfromtxt(f, skip_header=52)
    if type(getfor) is not str: H = GetOneCell(hr, getfor[0],getfor[1],getfor[2], num_basis = num_basis)
    elif getfor == 'neighbors': H = GetHomePlusNeighbors(hr, num_basis = num_basis)
    elif getfor == 'all': H = GetAllContributions(hr, num_basis = num_basis)

    if getfor == 'home': H = GetOneCell(hr, 0,0,0, num_basis = num_basis)

    if verbose: 
      print("Hamiltonian shape: ", hr.shape)
      print("Eigenvalues: ", eig(H)[0])

    H_all.append(H)


  return H_all 


