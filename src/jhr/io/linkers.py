# For modifiying input files
#
#class Modifier():
#    """
#    Modifiers is a helping class for cleaning up files after (say) ase has created the file. This 
#    Convenience class for removing unnecessary stuff.
#    """
#    @staticmethod
#    def modify_file(func, file, verbose = True, *args, **kwargs):
#        """
#        A wrapper which opens and closes a `file` and passes the arguments to 'func'
#        """
#        with open(file, 'r') as f:
#            lines = f.readlines()
#
#        new_lines = func(lines, *args, **kwargs)
#
#        if verbose: print(f"Called {func.__name__} on {file} with args {args} and kwargs {kwargs}")
#
#        with open(file, 'w') as f:
#            f.writelines(new_lines)
#        return 
#
#

class Linker:
    """
    Class for creating linkers. A linker takes a value from one output file (or parser) and writes it to another output file or parser.
    Args:
        source: Parser or file
        target: Calc object (or list thereof) for which an update dictionary is generated?
        func: source argument's method which is to be called.
    """

    def __init__(self, source = None, target = None, func = None):
        self.source = source
        self.func = func

        if not isinstance(target, list):
            self.target = [target]


        return

    def link(self):

        retriever = getattr(self.source.parser.outparser, self.func)
        update = retriever()
        #update = self._retrieve_link_val(link)

        [eachcalc.update_template(update, savefile = True) for eachcalc in self.target]
    
        return

    def _retrieve_link_val(self, link):
        """
        Retrieve the value that is to be updated. 
        """
        #Parser should have retrieving functions for three (possible) cases:
        #Case I: Dataframe already has the value
        #Case II: Link value is the convergence output
        #Case III:  
        retriever = getattr(self.source.parse.outparser, self.func)
        link_val = retriever()
        
        return link_val        




class QELinker(Linker):
    """
    QE class for linking values across calculations.
    """

    def __init__(self, link = None, source = None, target = None):
        #Determine function needed to extract data.
        if link in ['atomic positions', 'atomic_positions']:
            func = 'atomic_positions'

        super().__init__(source = source, target = target, func = func)
        return

#    def link(self):
#        return


