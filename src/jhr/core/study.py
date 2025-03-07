#study level classes.
from ase.io.espresso import write_espresso_ph, read_espresso_ph, read_espresso_in, write_espresso_in
from jhr.codes.espresso.io import QEio, QEModifier 
from jhr.io.base import Basher
import logging 
from itertools import product


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
      



class BaseConvergenceCalculation():
    """
    Base class for convergence calculations
    """
    def __init__(self,  template, parameters, code="", method="grid", update = {}, grepper = None):
        """
        Args:
          template (dict|str|path): Read template either from a dictionary or a json file path. 
          code (str): code to use
          criteria = convergence criteria (i.e. parameter e.g. 'Total Energy')
          update: Global updates that maybe needed for the template.
          grepper: Grepper class object for reading output files (to be provided by the code specific convergence class)
        """


        self.suite  = code.split('/')[0]
        self.code     = code.split('/')[1]
        self.template = self.read_template(template, update)
        self.parameters = parameters.keys()
        self.grepper = grepper

        # Create convergence value table
        def separate_params(parameters):
            """
            Separate parameters into convergence labels and values.
            """
            convs = []
            vals = []
            for each_conv in parameters.keys():
                convs.append(each_conv.split(","))
                vals.append(parameters[each_conv])
            convs = [x for xs in convs for x in xs]
            return convs, vals

        convs, vals = separate_params(parameters)

        def conv_method(convs, vals):
            # Whether to do nested convergence or grid?
            """
            Sorts values according to whether convergence is in grid or nested format.
            """
            if method == "nested":
                [print(f"performing convergence on {c}") for c in convs]
                print("NOT YET IMPLEMENTED")
                raise Exception("Sorry, no numbers below zero")
            elif method == "grid":
                combinations = self.convergence_combos(vals)
            return combinations

        self.params = convs
        self.vals = conv_method(convs, vals)

        #initialize self.calcs (for creating an iterator)
        self.calcs = [None]*len(vals)

        return 

    def read_template(self, template, update):
        """
        Read template from file depending on code. 
        """
        if not isinstance(template, dict):
            if self.code in ['pw.x', 'ph.x']:
                template = QEio.from_flat_JSON(template)
        template.update({k: update[k] for k in update.keys()})

        return template


    def convergence_combos(self, vals):
        """
        Create outer product for convergence
        """
        combinations = list(product(*vals))
        return combinations
    def run(self, command="", prepend="", check_conv = False, ):
        """
        Args:
            check_conv (bool): True. Check convergence in parallel 
        """
        for each_calc in self.calcs:
            each_calc.run(command, prepend)
            #grep deta
            #self.grepper.read(each_calc)
            #Read each_calc.
            if check_conv:
                check_convergence()

        return
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        """
        Returns next base calculation
        """
        if self.index >= len(self.calcs):
            raise StopIteration
        next_calc = self.calcs[self.index]
        self.index += 1
        return next_calc

    def __len__(self):
        return len(self.calcs)


    def __str__(self):
        return "Convergence calculation QE"



class BaseNormalCalculation():
    """
    Args:
    calc_type = 'normal', 'convergence'
    suite: 'QE', 'Yambo'
    code:   'pw.x'
    """
    def __init__(self,  template = None, code = '', update = {}, files = None):
        """
        Args:
          template (dict|str|path): Read template either from a dictionary or a json file path. 
          code (str): suite and code to use. 'qe/pw.x'
          files: Names to use for files. 
                  If None given: Read from template['prefix']
                  If str given: Use that (append '.in' and '.out' for input and output
                  If list given: Use the first two as file names.
        """

        self.suite  = code.split('/')[0]
        self.code     = code.split('/')[1]
        self.template = self.read_template(template, update)
        self.file_in, self.file_out    = self.figure_file_names(files, template)
        return 

    def read_template(self, template, update):
        """
        Read template from file depending on code. 
        """
        if not isinstance(template, dict):
            #if extension is .json
            if self.suite == 'qe':
                template = QEio.from_flat_JSON(template)
            #If extension is .in
        template.update({k: update[k] for k in update.keys()})

        return template

    def figure_file_names(self, files = None, template = None):
        """
        Figures out file names to use. 
        """

        # if files is None:
        #     if isinstance(template, str):
        #       try: 
        #         file_in = template + ".in"
        #         file_out = template + ".out"                
        #       except:
        #         raise Exception("Couldn't create file name from template name.")
        #     else: #if template is a dictionary
        #       try:
        #           file_in = self.template["prefix"] + ".in"
        #           file_out = self.template["prefix"] + ".out"
        #       except:
        #           raise Exception(
        #               "Couldn't read prefix from template. Consider adding 'prefix' to template or provide file name(s) for io files"
        #           )
        if isinstance(files, str):
            file_in = files + ".in"
            file_out = files + ".out"
        elif isinstance(files, list):
            file_in = files[0]
            file_out = files[1]
        return file_in, file_out

    def run(self, command="", prepend = ""):
        """
        Execute command
        """
        if command == "":
            command = f"{prepend} {self.code} < {self.file_in} > {self.file_out}"
        Basher.runcommand(command)

        return
      
