import numpy as np
import matplotlib.pyplot as plt
import os
import glob


def DOSHandlerQE(pdos_folder, totaldosfile, spin_polarized_atoms, toskip = {}, plotTDOS = False, efermi = 0):
  """
  Density of States Handler for Quantum Espresso (QE)
  """

  all_pdos = reader(pdos_folder, contains = 'pdos')

  pdos_data, energy_tot, dos_tot = prepareDOS(all_pdos, pdos_folder, totaldosfile, toskip, plotTotal = plotTDOS, spin_polarized_atoms= spin_polarized_atoms)

  #____Also plot TDOS_____
  if plotTDOS == True:
    pdos_data['Total DOS'] = {}
    pdos_data['Total DOS']['energy'] = energy_tot
    pdos_data['Total DOS']['dos'] = dos_tot

  #_____Convert pdos_data (dictionary) to makeplot format_____
  x = []
  y = []
  labels = []

  # for key in pdos_data.keys():
  #     labels.append(key)
  #     x.append(pdos_data[key]['dos'])
  #     y.append(pdos_data[key]['energy'])
  # y = np.array(y)
  # y = y.T
  # y -= efermi

  # x = np.array(x)
  # x = x.T
  
  # return x, y, labels

  for key, info in pdos_data.items():
          energy = np.array(info['energy']) - efermi

          if 'dos_dw' in info and info['dos_dw'] is not None:
              # Spin-polarized: plot up as positive, down as negative
              x.append(info['dos'])
              x.append(-info['dos_dw'])
              y.append(energy)
              y.append(energy)
              labels.extend([f"{key} ↑", f"{key} ↓"])
          else:
              # Non-spin case
              x.append(info['dos'])
              y.append(energy)
              labels.append(key)

  x, y = np.array(x).T, np.array(y).T
  return x, y, labels



#++++++++++++++++++++++ PDOS ATOM ORB ROUTINES++++++++++++++++++++++++++
# Define the function to read multiple PDOS files
def r_dos(name, atom, spin_polarized_atoms = None, is_spin= False):
    """Read files. Return energy and dos as numpy arrays"""
    # data = np.loadtxt(name, usecols=(0, 1))
    # energy, dos = data.T
    # return energy, dos
    
    # Default: no spin polarization
        # Access the global spin_polarized_atoms variable
    # if caller gave a spin_polarized_atoms list, use it to determine is_spin
    if spin_polarized_atoms is not None:
        # sensible safety: allow items like 'Mn' to match filenames like 'Mn9'
        is_spin = atom in spin_polarized_atoms
    
    if is_spin:
        # File format: col1=Energy, col2=Up, col3=Down
        data = np.loadtxt(name, usecols=(0, 1, 2))
        energy, dos_up, dos_down = data.T
    else:
        # File format: col1=Energy, col2=DOS (non-spin)
        data = np.loadtxt(name, usecols=(0, 1))
        energy, dos_up = data.T
        dos_down = None

    return energy, dos_up, dos_down

def reader(folder, contains = 'all'):
  """Generate list of files subject to criteria"""
  files = glob.glob(os.path.join(folder, f'*{contains}*'))

  if not files:
      print(f"No files found containing {contains}.")
  else:
      print(f"Found {len(files)} {contains} files.")

  return files

    
def parsefilename(file, spin_polarized_atoms=None):

  #_____Parse file name to extract atom and orbit details_____
  # Sample file name:       prefix.pdos_atm#1(Cs)_wfc#1(s)
  try:
    # Extract atom and orbital information using regex-like string splitting
    atom_info = file.split('_atm#')[1].split('_wfc#')[0]
    atom_type = atom_info.split('(')[1].split(')')[0]  # Extract atom (e.g., Cs, Pb)
    
    orbital_info = file.split('_wfc#')[1]
    orbital_type = orbital_info.split('(')[1].split(')')[0]  # Extract orbital type (e.g., s, p, d)
    is_spin = atom_type in (spin_polarized_atoms or [])
    parsed = {'atom': atom_type, 'atomNum': atom_info, 'orbit':orbital_type, 'orbitNum': orbital_info, 'is_spin': is_spin}

  except IndexError:
    parsed = {'atom': '', 'orbit': '','is_spin': False}      #REturns empty string for the total DOS file.
    print(f"Skipping file {file} due to parsing issues.")
 
  return parsed

def aggregateDOS(pdos_data, energy, dos, parsed, method = 'atom-orb', spin=None):
  """Aggregate the DOS according to requirements

  Args:
    method: ['separate', 'atom-orb']

  """

  if method == 'atom-orb': #aggregate by both atom and orbit.

    key = f"{parsed['atom']}-{parsed['orbit']}"
    if key not in pdos_data:
        pdos_data[key] = {'energy': energy, 'dos': np.zeros_like(dos)}
    if spin == 'down':
            if pdos_data[key].get('dos_dw') is None:
                pdos_data[key]['dos_dw'] = np.zeros_like(dos)
            pdos_data[key]['dos_dw'] += dos
    else:
        # spin == 'up' or spin is None -> accumulate into 'dos'
        pdos_data[key]['dos'] += dos

    # Accumulate DOS for the corresponding atom and orbital type
    pdos_data[key]['dos'] += dos
  
  elif method == 'separate':
    #key = f"{parsed['atom']}{parsed['atomNum']}-{parsed['orbit']}{parsed['orbitNum']}"
    pass;



  return pdos_data
  
def prepareDOS(all_pdos, pdos_folder, totaldosfile, toskip, plotTotal=True, spin_polarized_atoms=None):
  """
  Calls aggregateDOS one by one to create a complete dataset for all the files in the folder.
  """

  # Initialize a dictionary to store energy and DOS for each atom and orbital type
  
  pdos_data = {}
  spin_polarized_atoms = spin_polarized_atoms or []
  # Load PDOS files and store DOS for each atom and orbital
  for file in all_pdos:
    parsed = parsefilename(file)

    atom = parsed['atom']      
    orbit = parsed['orbit']
    
    if (atom in toskip.keys() and orbit in toskip[atom]) or atom == '':
      continue
#      print("FILE: ", file)
      #_____Read data________
    is_spin = atom in spin_polarized_atoms
    
    energy, dos_up, dos_dw = r_dos(file, atom, is_spin = is_spin)
    
    if energy is None or dos_up is None:
        continue

      #____Parse filename and aggregate DOS if atom is not to be skipped______
      
    
    # Aggregate DOS (handle spin cases separately)
    if is_spin and dos_dw is not None:
        # Store both spin-up and spin-down separately
        pdos_data = aggregateDOS(pdos_data, energy, dos_up, parsed, method='atom-orb', spin='up')
        pdos_data = aggregateDOS(pdos_data, energy, dos_dw, parsed, method='atom-orb', spin='down')
    else:       
      pdos_data = aggregateDOS(pdos_data, energy, dos_up, parsed, method = 'atom-orb')

  # Read the total PDOS
  if plotTotal:
      # The total DOS is spin-polarized if any atom is spin-polarized
      total_is_spin = len(spin_polarized_atoms) > 0

      energy_tot, dos_up_tot, dos_dw_tot = r_dos(
          os.path.join(pdos_folder, totaldosfile),
          atom='Total',
          is_spin=total_is_spin
      )

      if dos_dw_tot is not None:
          dos_tot = dos_up_tot + dos_dw_tot
      else:
          dos_tot = dos_up_tot

  return pdos_data, energy_tot, dos_tot

