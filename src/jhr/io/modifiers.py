# For modifiying input files

class Modifiers():
    """
    Modifiers is a helping class for cleaning up files after (say) ase has created the file. This 
    Convenience class for removing unnecessary stuff.
    """
    @staticmethod
    def modify_file(func, file, verbose = True, *args, **kwargs):
        """
        A wrapper which opens and closes a `file` and passes the arguments to 'func'
        """
        with open(file, 'r') as f:
            lines = f.readlines()

        new_lines = func(lines, *args, **kwargs)

        if verbose: print(f"Called {func.__name__} on {file} with args {args} and kwargs {kwargs}")

        with open(file, 'w') as f:
            f.writelines(new_lines)
        return 


