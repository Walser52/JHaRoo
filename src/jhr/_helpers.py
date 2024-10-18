# Simple helper routines. 

import numpy as np


def trunc(values, decs=0):
    """Truncate numpy numbers"""
    return np.trunc(values*10**decs)/(10**decs)
