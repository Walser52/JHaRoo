# Simple helper routines. 

import numpy as np
import glob
import os

class Constants():
    BOHRtoA = 0.529177249
    RYtoeV = 13.605698066



def trunc(values, decs=0):
    """Truncate numpy numbers"""
    return np.trunc(values*10**decs)/(10**decs)


#+++++++Dicter+++++++++
class Dicter():
    def __init__(self):
        pass

    @classmethod
    def flatten_dict(cls, d):
      """
      Flattens a nested dict by removing parents. Helps in reading scf input file.
      """
      items = []
      for k, v in d.items():
          new_key = f"{k}" 

          try:
            v = v.data
          except:
            pass

          if isinstance(v, dict):
              items.extend(cls.flatten_dict(v).items())
          else:
              items.append((new_key, v))

      return dict(items)       

#++++++++File Handlers++++++++++++
def fileswith(pattern, infolder):
  found_files = glob.glob(os.path.join(infolder, '**', pattern), recursive=True)
  return found_files
