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
        modify: Calc object (or list thereof) for which an update dictionary is generated?
    """

    def __init__(self, link = None, source = None, modify = None, func = None):
        self.link = link
        self.source = source
        self.func = func

        if not isinstance(list, modify):
            self.modify = [modify]
        #Case I:
            #Extract linker from parser (which is passed)
            #link_val = source.parser.data.loc[link, :][0]
            #update = {link: link_val}
            #[eachcalc.update_template(update) for eachcalc in self.modify]
            
            

        return

    def link(self):
        #use parser to extract value to link. 
            #the value may come from the df associated with the parser
        update = self._retrieve_link_val(link)

#        link_val = self.source.parser.data.loc[link, :][0]
            #or it may come through a special function (less likely)
        #update = {link: link_val}
        [eachcalc.update_template(update, savefile = True) for eachcalc in self.modify]
    
        return

    def _retrieve_link_val(self, link):
        """
        Retrieve the value that is to be updated. 
        """
        #Parser should have retrieving functions for three (possible) cases:
        #Case I: Dataframe already has the value
        #Case II: Link value is the convergence output
        #Case III:  
        retriever = getattr(self.source.parser, self.func)
        link_val = retriever()
        
        return link_val        




class QELinker(Linker):

    def __init__(self):
        pass

    def link(self):
        return


