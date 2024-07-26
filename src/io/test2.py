import numpy as np

with open('test.wfc.dat', 'rb') as f:
    # Moves the cursor 4 bytes to the right
    f.seek(4)

    ik = np.fromfile(f, dtype='int32', count=1)[0]
    
    # xk = np.fromfile(f, dtype='float64', count=3)
    # ispin = np.fromfile(f, dtype='int32', count=1)[0]
    # gamma_only = bool(np.fromfile(f, dtype='int32', count=1)[0])
    # scalef = np.fromfile(f, dtype='float64', count=1)[0]
    # print("ik: ", ik)
    

with open('aiida.wfc1', 'rb') as f:
    # Moves the cursor 4 bytes to the right
    f.seek(4)

    ik = np.fromfile(f, dtype='int32', count=1)[0]
    
    # xk = np.fromfile(f, dtype='float64', count=3)
    # ispin = np.fromfile(f, dtype='int32', count=1)[0]
    # gamma_only = bool(np.fromfile(f, dtype='int32', count=1)[0])
    # scalef = np.fromfile(f, dtype='float64', count=1)[0]
    print("ik: ", ik)