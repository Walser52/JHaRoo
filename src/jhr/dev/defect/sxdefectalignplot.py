

import numpy as np
import matplotlib.pyplot as plt
from DFE_module import find_plateau
# Load the file
filename = "vline-eV-a1.dat"
data = np.loadtxt(filename)

# Assign columns
z = data[:, 0]          # First column
V_long = data[:, 1]     # Second column
V_diff = data[:, 2]     # Third column
V_short = data[:, 3]    # Fourth column

# 🛠 User Input: Define defect and search region manually
defect_pos = 0           # Example: Defect at z = 0
start_z = 10             # Search for plateau starting from z = 20
end_z = 13               # Search until z = 80

plateau_value = find_plateau(z, V_short, start_z, end_z)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(z, V_long, label="V_long (Long-range)", color="blue")
plt.plot(z, V_diff, label="V_diff (Defect - Ref)", color="green")
plt.plot(z, V_short, label="V_short (Short-range)", color="red")





# Plot formatting
plt.xlabel("z (Bohr)", fontsize=12)
plt.ylabel("Potential (eV)", fontsize=12)
# plt.title("Planar Averages", fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

