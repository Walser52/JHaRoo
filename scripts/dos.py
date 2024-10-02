import os
import matplotlib.pyplot as plt
import numpy as np
base_dir = os.path.dirname(os.path.abspath(__file__))
# define fermi energy
efermi = 1.9671

title='CsPBBr3'

# Open and read the aiida.dos file
data_file_DOS = os.path.join(base_dir, '..', 'data', 'dos_files', 'CsPBBr3.dos')
data = np.loadtxt(data_file_DOS)
energy, dos, idos = data.T

# Plot DOS 
plt.figure()
plt.title(title)
plt.plot(dos, energy-efermi,  c= 'green')
plt.axhline(y=efermi-efermi, c='gray', linestyle='--', linewidth=1)
plt.xlabel('DOS (eV)')
plt.ylabel('Energy (eV)')

plt.xlim (0, 45)
plt.ylim (-4, 10)

svg_file = os.path.join(base_dir, '..', 'plots', 'DFT_DOS', f"{title}")
plt.savefig(svg_file+'.svg', format='svg', transparent=True)
plt.savefig(svg_file+'.png', format='png', transparent=True)
plt.show()