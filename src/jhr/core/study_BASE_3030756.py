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

class BaseQEConvergenceCalculation():
  def __init__(self, template, parameters, values, code = '', method = 'nested'):
    """
    Convergence is performed over a grid. Nested convergence is to be done manually (for now)

    Args:
      template: Template to modify
      parameters: Parameters dict to modify in each template.
      convergence_style: nested/grid. 

    Example:
      parameters = {'ecutwfc': [1,2,3], 'ecutrho': [4,5,6], 'nx,ny,nz':[[2,2,2],[4,4,4]]}



    """
    self.template = template
    self.parameters = parameters
    self.values = values

    self.converged_val = np.nan

    self.parameters = parameters.keys()

    #Create convergence value table
    convs = []
    vals = []
    for each_conv in parameters.keys():
        convs.append(each_conv.split(','))
        vals.append(parameters[each_conv])

    if mode == 'nested':
        [print(f"performing convergence on {c}") for c in convs ]
        print("NOT YET IMPLEMENTED")
        raise Exception("Sorry, no numbers below zero")
    elif mode == 'grid':
        self.convergence_combos(parameters)
        # CREATE BASEQUENORMALCALCULATION OBJECT AND UPDATE TEMPLATE ACCORDING TO EACH CASE



    
    

    #Create multiple base calculations each with its own file. At the end run the calculations

    return 
  def convergence_combos(self, parameters):
    """
    Create outer product for convergence 
    """
    combinations = list(product(*vals))
    combinations_2d = [list(combo[:2]) + combo[2] for combo in combinations]

    # Print the results
#    for row in combinations_2d:
#        print(row)

    return combinations_2d

  def _prepare_variants():
    return


class BaseQENormalCalculation():
  """
  code
  Functionality: Use json template to save QE input. Run QE input.
  
  Args:
  	stem = File stem to save. Input files 
  	files = ('file_abc', 'file_xyz') or 'file' which becomes ('file.in', 'file.out')
  
  """

  def __init__(self, template, code, ase_dict = {}, update = {}, files = ['',''], run = False, command = '', **kwargs):
    """
    
    """
    self.template = template
    self.update = update
    self.code = code
    self.result = None
    self.ase_dict = ase_dict

    self.file_in = files[0]
    self.file_out = files[1]

#	# update file
#    if update != {}:
#      #update template.
#      pass
    
    #Create espresso file
    self._save_file(self.file_in, template, ase_dict, self.code)

#    #run calc?
#    if run:
#    	#Run calculation immediately.
#    	pass
    return

  def _save_file(self, filename, template, ase_dict: dict = {}, code: str = 'ph.x'):
    """
    Save file
    Args: 
      filename: File name
      template: template to pass to ase's espresso module methods.
      code: code which to pass to.
      ase_dict: other options. See ase's documentation.
    
    """
    with open(filename, "w") as f:
      if code == 'pw.x': write_espresso_in(f, input_data = template, **ase_dict)
      if code == 'ph.x': write_espresso_ph(f, template, **ase_dict)

    logging.info(f"Saved {filename=}")
    return

  def ase_hacks(self, filename, remove_ibrav = False, remove_cell_parameters = False, modify_atomic_positions = False, atomic_positions:str = 'crystal_sg', verbose = False):
    """
    Some hacks for writing ase files for QE. 
    """
    if remove_ibrav:
      QEModifier.modify_file(QEModifier.remove_ibrav, filename, verbose = verbose)
    if remove_cell_parameters:
      QEModifier.modify_file(QEModifier.remove_cell_parameters, filename,verbose = verbose)
    if modify_atomic_positions:
      QEModifier.modify_file(QEModifier.modify_atomic_positions, filename, atomic_positions = atomic_positions, verbose = verbose)


    return
    
  def run(self, command = ''):
#    command = f"{code} < {f_in} > {f_out}"
    if command == '':
      command = f"{self.code} < {self.file_in} > {self.file_out}"
    Basher.runcommand(command)

    return
    
  def update_template(update = {}):

    return


    def _separate_args(self, templates:Union[Dict, List[Dict]]):
        """
        Sifts dictionary template into a format for ase. The file template is separated from other arguments.

        Args: 
        templates 

        Returns:
        mod_templates: modified by popping out unnecessary keys. Accepts a single dict or a list of dicts. 
        ase_dicts: other options to be passed to ase. 
        """

        if isinstance(templates, dict): templates = [templates]

        ase_dicts, mod_templates = [], []

        for template in templates:
            ase_dict, template = self.extract_ase_dict(template)

        mod_templates.append(template)
        ase_dicts.append(ase_dict)

        return mod_templates, ase_dicts

    def extract_ase_dict(self, template, return_atoms = False):
        """
        Pops out ase_dict elements from template. 

        Args: template
        Returns: 
        ase_dict 
        template: modified by popping ase_dict 
        """
        atoms, template = self.gen_atoms_from_template(template)

        #Create ase dict for other options
        ase_dict = {'atoms': atoms}
        for key in ['pseudopotentials', 'kpts', 'crystal_coordinates', 'additional_cards', 'koffset', 'kspacing']:
            if key in template.keys(): ase_dict[key] = template.pop(key)

        if return_atoms: return ase_dict, template, atoms

        return ase_dict, template

