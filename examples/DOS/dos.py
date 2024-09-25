import matplotlib.pyplot as plt
import numpy as np

# define fermi energy
efermi = 2.298
title='CsPBBr3 DOS'

# Open and read the aiida.dos file
data_file= 'CsPBBr3.dos'
data = np.loadtxt(data_file)
energy, dos, idos = data.T

# Plot DOS 
plt.figure()
plt.title(title)
plt.plot(energy-efermi, dos, c= 'green')
plt.axvline(x=efermi-efermi, c='gray', linestyle='--', linewidth=1)
plt.xlabel('Energy (eV)')
plt.ylabel('DOS (eV)')

plt.xlim (-5, 10)
plt.ylim (0, 40)

plt.savefig ('CsPbBr3.svg', format = 'svg')
plt.show()