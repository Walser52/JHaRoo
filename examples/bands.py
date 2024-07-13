import matplotlib.pyplot as plt
import numpy as np
data = np.loadtxt('aiida.bands.gnu')
# k = np.unique(data[:,0])
# bands = np.reshape(data[:,1], [-1, len(k)])
nbnd = len(np.where(np.diff(data[:, 0]) < 0)[0]) + 1
lenk = int(data.shape[0] / nbnd)
k = data[:lenk, 0]
bands = np.reshape(data[:, 1], (-1, lenk))
for band in range (len(bands)):
    plt.plot(k,bands[band, :], c = 'blue')
plt.title("CsPbI3 Bands")
plt.xlabel("High Symmetry Points")
plt.ylabel("Energy (eV)")

plt.show()


