import matplotlib.pyplot as plt
import numpy as np
import os
import glob

title = 'CsPbBr3'
pdos_folder = r'../data/pdos_files/CsPBBr3_PDOS'
totaldosfile = 'aiida.pdos_tot'
saveto = '../plots/DFT_PDOS_atom_orb'
toskip = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':['p']}

efermi = 1.9671


#___________plotsettings
xrange = [0,3]
yrange = [-4,10]

plotTDOS = False

# Define the function to read multiple PDOS files
def r_dos(name):
    """Read files. Return energy and dos as numpy arrays"""
    data = np.loadtxt(name, usecols=(0, 1))
    energy, dos = data.T
    return energy, dos

def readfolder(folder, contains = 'all'):
  """Generate list of files subject to criteria"""
  files = glob.glob(os.path.join(folder, f'*{contains}*'))

  if not files:
      print(f"No files found containing {contains}.")
  else:
      print(f"Found {len(files)} {contains} files.")

  return files

    
def parsefilename(file):

  #_____Parse file name to extract atom and orbit details_____
  # Sample file name:       prefix.pdos_atm#1(Cs)_wfc#1(s)
  try:
    # Extract atom and orbital information using regex-like string splitting
    atom_info = file.split('_atm#')[1].split('_wfc#')[0]
    atom_type = atom_info.split('(')[1].split(')')[0]  # Extract atom (e.g., Cs, Pb)
    
    orbital_info = file.split('_wfc#')[1]
    orbital_type = orbital_info.split('(')[1].split(')')[0]  # Extract orbital type (e.g., s, p, d)
    parsed = {'atom': atom_type, 'atomNum': atom_info, 'orbit':orbital_type, 'orbitNum': orbital_info}

  except IndexError:
    parsed = {'atom': '', 'orbit': ''}      #REturns empty string for the total DOS file.
    print(f"Skipping file {file} due to parsing issues.")
 
  return parsed

def aggregateDOS(pdos_data, energy, dos, parsed, method = 'atom-orb'):
  """Aggregate the DOS according to requirements

  Args:
    method: ['separate', 'atom-orb']

  """

  if method == 'atom-orb': #aggregate by both atom and orbit.

    key = f"{parsed['atom']}-{parsed['orbit']}"
    if key not in pdos_data:
        pdos_data[key] = {'energy': energy, 'dos': np.zeros_like(dos)}

    # Accumulate DOS for the corresponding atom and orbital type
    pdos_data[key]['dos'] += dos
  
  elif method == 'separate':
    #key = f"{parsed['atom']}{parsed['atomNum']}-{parsed['orbit']}{parsed['orbitNum']}"
    pass;



  return pdos_data
  
def plotallDOS(all_pdos, plotTotal=True):
  # Initialize a dictionary to store energy and DOS for each atom and orbital type
  pdos_data = {}

  # Load PDOS files and store DOS for each atom and orbital
  for file in all_pdos:
#      print("FILE: ", file)
      #_____Read data________
      energy, dos = r_dos(file)
      if energy is None or dos is None:
          continue

      #____Parse filename and aggregate DOS if atom is not to be skipped______
      parsed = parsefilename(file)

      atom = parsed['atom']      
      orbit = parsed['orbit']
      if (atom in toskip.keys() and orbit in toskip[atom]) or atom == '':
        continue
      else:       
        pdos_data = aggregateDOS(pdos_data, energy, dos, parsed, method = 'atom-orb')

  # Read the total PDOS
  if plotTotal:
    energy_tot, dos_tot = r_dos(os.path.join(pdos_folder, totaldosfile))
  else:
    energy_tot, dos_tot = [], []
  
  

  return pdos_data, energy_tot, dos_tot

def plotDOS(pdos_data, energy_tot, dos_tot):
  #_________________PLOT________________________
# Create figure
  plt.figure()

  # Plot total DOS
  if plotTDOS:
    plt.plot(dos_tot, energy_tot - efermi, c='blue', label='Total DOS')

  # Plot PDOS for each atom and orbital type
  for key, data in pdos_data.items():
    plt.plot(data['dos'], data['energy'] - efermi, label=f'{key} orbitals')

  # Add labels and save the figure
  plt.title(title)
  plt.xlabel('DOS (states/eV)')
  plt.ylabel('Energy (eV)')
  plt.axhline(y=0, c='gray', linestyle='--', linewidth=1)

  plt.xlim(xrange)
  plt.ylim(yrange)
  plt.legend(frameon = False)

  # Save the plots
  #base_dir = os.path.dirname(os.path.abspath(__file__))
  svg_file = os.path.join(saveto, f"{title}")
  plt.savefig(svg_file + '.svg', format='svg', transparent=True)
  plt.savefig(svg_file + '.png', format='png', transparent=True, dpi=350)


  return

if __name__ == '__main__':

  all_pdos = readfolder(pdos_folder, contains = 'pdos')
  pdos_data, energy_tot, dos_tot = plotallDOS(all_pdos, plotTotal = plotTDOS)
  plotDOS(pdos_data, energy_tot, dos_tot)

  print(pdos_data['Pb-p'])

  plt.show()
  
