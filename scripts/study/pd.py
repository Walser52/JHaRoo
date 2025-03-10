import pandas as pd
import numpy as np

data = pd.read_csv ("converged.dat", sep = '\t')

print(np.array(data))
