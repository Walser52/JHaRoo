from typing import Union, Optional
from typing import List, Tuple
from ase.io.espresso import write_espresso_ph, read_espresso_ph, write_espresso_in, read_espresso_in


class BaseConverger:
    def __init__(self):
        # Initialize any attributes or settings if needed
        return

    @staticmethod
    def conv_on(template=None, parameters=None, valuesets=None):
        """
        Create convergence files changing parameters according to values sets.

        "template" (dict): Contains parameters. See ASE documentation
        "parameters" (list of strings): Parameters to change.
        "valuesets" (list of lists)   : sets of values.
        """

        all_files = []

        # Loop over the valuesets and adjust the template

        for values in valuesets:
            new_template = template.copy()  # Make a copy to avoid modifying the original
            for i, p in enumerate(parameters):
#                print(valuesets)
                if isinstance(values, (list, tuple)) and len(values) > 1:
                  new_template[p] = values[i]
                else: 
                  values = [values]
                  new_template[p] = values[i]
            
            all_files.append(new_template)

        return all_files



class QEConverger(BaseConverger):
    def savefiles(self, prefix: str = '', files_data: List[dict] = [], ext: str = 'in', code: str = 'ph', ase_dict: dict = {}) -> None:
      """
      Args:
        files_data: input variables. 
        ase_dict: other parameters such as additional cards which are passed to ase. 
      """
      #phonon files write
      for i, data in enumerate(files_data):
        file = f'{prefix}_{i}.{ext}'
        with open(file, "w") as f:
          if code == 'pw': write_espresso_in(f, input_data = data, **ase_dict)
          if code == 'ph': write_espresso_ph(f, data, **ase_dict)
      return
      
