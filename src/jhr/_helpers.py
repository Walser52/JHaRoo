# Simple helper routines. 

import numpy as np
import glob
import os


def trunc(values, decs=0):
    """Truncate numpy numbers"""
    return np.trunc(values*10**decs)/(10**decs)



#++++++++File Handlers++++++++++++
def fileswith(pattern, infolder):
  found_files = glob.glob(os.path.join(infolder, '**', pattern), recursive=True)
  return found_files
