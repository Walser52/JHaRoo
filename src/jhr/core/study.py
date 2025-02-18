#study level classes.

# Study




class Chain():
  def __init__(self):
    pipe = ['pw_convA', 'pw_convB','pw_convC']
    pass

  def createCalculators():
    #Create calculators corresponding to pipes. 
      #Convergence type
      #Single type



class Calculation(self, kind = 'normal'):
  """
  calc_type = 'normal', 'convergence'
  """
  

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

class BaseConvergenceCalculation():
  pass

class BaseNormalCalculation(template, update = {}, code = None, files = ('',''), run = False):
  """
  code
  
  Args:
  	stem = File stem to save. Input files 
  	files = ('file_abc', 'file_xyz') or 'file' which becomes ('file.in', 'file.out')
  
  """

  def __init__():
    self.template = template
    self.update = update
    self.code = code
    self.result = None

	# update file
    if update != {}:
      #update template.
      pass
    
    #save file?
    #run calc?
    if run:
    	#Run calculation immediately.
    	pass
    return
    
  def update_template(update = {}):

    return

  @staticmethod
  def run():
    #run calculation
    pass

