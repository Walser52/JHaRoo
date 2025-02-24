#study level classes.
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.io.base import Basher
import logging 


logging.basicConfig(
  filename = "app.log",
  format="{message} - {asctime} - {levelname}",
   style="{",
   datefmt="%Y-%m-%d %H:%M",
   level=logging.INFO)




class Chain():
  def __init__(self):
    pipe = ['pw_convA', 'pw_convB','pw_convC']
    pass

  def createCalculators():
    #Create calculators corresponding to pipes. 
      #Convergence type
      #Single type
    pass



class Calculation():
    """
    Args:
    calc_type = 'normal', 'convergence'
    suite: 'QE', 'Yambo'
    code:   'pw.x'
    """
    def __init__(self,  template = None, code = '', mode = 'normal', settings = {}, files = ['', ''], run = False):
        """
        Args:
        code = '{suite}/{code}' e.g. 'qe/pw.x'. Use '/' to separate suite and code.
        files = ('file_abc', 'file_xyz') or 'file' which becomes ('file.in', 'file.out')
        """
        self.suite =  code.lower().split('/')[0]
        self.code =   code.lower().split('/')[1]
        self.mode =   mode.lower()
        if self.suite == 'qe' or self.suite == 'espresso':
            if self.mode == 'normal': 
                self.calc = BaseQENormalCalculation(template, code, files = files, run = run)
            elif self.mode == 'convergence': 
                self.calc = BaseQEConvergenceCalculation(template, code, settings, run)
        return 
      

    def from_json(self, template, parameters, code = None):
        """
        parameters (dict): 
        """
      
        if kind == 'normal': 
          #create a single base caclulation
          self.template = [BaseNormalCalculation(template, code)]

        elif kind == 'convergence':
    #      self.template = [BaseConvergenceCalculation()] * len(parameters.keys())

          for i in len(parameters.keys()):
            #create base convergence calculation.
            pass

          for param, values in parameters.keys():
            n = len(values)
            variants = []
            for val in values:
              variants.append(BaseNormalCalculation(template, {param:val}, code))
            pass
          #create several base calculations
          
          #How many BaseCalculation objects are needed.
          #[BaseCalculation]* n

          #Need: template; parameters; valuesets 
          pass
        return


