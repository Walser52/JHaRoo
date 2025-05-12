from DFE_module import extract_tot_energy, extract_mu, chem_pot, energy_dict
from jhr.codes.espresso.io import QEOutParser


files = {
    'pristine': 'pwscf.out',
    'defected': 'pwscf copy.out',
    'Pb_mu' : 'pwscf copy.out',
    'Zn_mu' : 'pwscf.out'
}


n = {
    'Pb' : -1,
    'Zn':   23  
}


prs = QEOutParser('pw.x')

total_energies = {}

for label, file in files.items():
    df = prs.parser.Process(file)
    total_energy = df.loc['total_energy'][0]
    total_energies[label] = total_energy
print(total_energies)

# Separate the energies of files having _mu in their names that are further required for chemical potential term.
mu_energies = {k: v for k, v in total_energies.items() if '_mu' in k}
print(mu_energies)

# #calculate sum of (mui)*(ni)

tot_chem_pot = chem_pot(mu_energies, n)
print(f"Tot_chem_pot:{tot_chem_pot}")

# sxdefectalignplot (extract potential alignment value by reading plateau),
# sxdefectalignparse (extract energy correction) -> Final energy correction (Ecorr + delV)
# readVBM for EVBM (It also reads CBM that will be required to vary the fermi energy)
# Multiply q where it is required
#======== AND YOU HAVE DFE ==================