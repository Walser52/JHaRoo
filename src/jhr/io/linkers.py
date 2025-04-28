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

class Linkers:
    """
    Class for creating linkers. A linker takes a value from one output file (or parser) and writes it to another output file or parser.
    Args:
        from: Parser or file
        modify: Calc object (or list thereof) for which an update dictionary is generated?
    """

    def __init__(self, link = None, from = None, modify = None):
        self.link = link
        self.from = from

        if not isinstance(list, modify):
            self.modify = [modify]
        #Case I:
            #Extract linker from parser (which is passed)
            link_val = from.parser.data.loc[link, :][0]
            update = {link: link_val}
            [eachcalc.update_template(update) for eachcalc in self.modify]
            
            

        return

