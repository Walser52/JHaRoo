import numpy as np

with open('aiida.wfc1', 'rb') as f:
    # Moves the cursor 4 bytes to the right
    f.seek(4)

    ik = np.fromfile(f, dtype='int32', count=1)
    xk = np.fromfile(f, dtype='float64', count=3)
    ispin = np.fromfile(f, dtype='int32', count=1)[0]
    gamma_only = bool(np.fromfile(f, dtype='int32', count=1)[0])
    scalef = np.fromfile(f, dtype='float64', count=1)[0]
    print("ik: ", ik)
    

    # Move the cursor 8 byte to the right
    f.seek(8, 1)

    ngw = np.fromfile(f, dtype='int32', count=1)[0]
    igwx = np.fromfile(f, dtype='int32', count=1)[0]
    npol = np.fromfile(f, dtype='int32', count=1)[0]
    nbnd = np.fromfile(f, dtype='int32', count=1)[0]


    # Move the cursor 8 byte to the right
    f.seek(8, 1)

    b1 = np.fromfile(f, dtype='float64', count=3)
    b2 = np.fromfile(f, dtype='float64', count=3)
    b3 = np.fromfile(f, dtype='float64', count=3)

    f.seek(8,1)
    
    mill = np.fromfile(f, dtype='int32', count=3*igwx)
    mill = mill.reshape( (igwx, 3) ) 

    evc = np.zeros( (nbnd, npol*igwx), dtype="complex128")

    f.seek(8,1)
    for i in range(nbnd):
        evc[i,:] = np.fromfile(f, dtype='complex128', count=npol*igwx)
        f.seek(8, 1)
