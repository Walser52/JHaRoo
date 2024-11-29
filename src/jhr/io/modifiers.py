# For modifiying input files

class Modifiers():
    """
    Modifiers is a helping class for cleaning up files after (say) ase has created the file. This 
    Convenience class for removing unnecessary stuff.
    """
    @staticmethod
    def modify_file(func, file, *args, **kwargs):
        """
        A wrapper which opens and closes a `file` and passes the arguments to 'func'
        """
        with open(file, 'r') as f:
            lines = f.readlines()

        new_lines = func(lines, *args, **kwargs)

        print(f"Called {func.__name__} on {file} with args {args} and kwargs {kwargs}")

        with open(file, 'w') as f:
            f.writelines(new_lines)
        return 

class QEModifier(Modifiers):
    @staticmethod
    def remove_ibrav(lines: list):
        """
        Removes ibrav from lines read from a file.
        """
        new_lines = []
        for line in lines:
            if 'ibrav' not in line.lower():
                new_lines.append(line)  # Keep the lines that don't contain 'ibrav'
        return new_lines


    @staticmethod
    def modify_atomic_positions(lines, atomic_positions: str = ''):
        """
        Modify the ATOMIC_POSITIONS line to 'ATOMIC POSITIONS crystal_sg' e.g.
        or to a user-specified atomic_positions string.
        """
        new_lines = []
        for line in lines:
            # Modify the ATOMIC_POSITIONS line if the atomic_positions string is provided
            if 'atomic_positions' in line.lower() and len(atomic_positions) > 0:
                new_lines.append(f'ATOMIC_POSITIONS {atomic_positions}\n')
            else:
                new_lines.append(line)

        return new_lines

    @staticmethod
    def remove_cell_parameters(lines):
        """
        Remove the line containing 'CELL_PARAMETERS' and the following 3 lines.
        """
        new_lines = []
        skip_next_lines = 0  # Flag to keep track of how many lines to skip
        for line in lines:
            # Check for 'CELL_PARAMETERS' line and set skip_next_lines
            if 'cell_parameters' in line.lower():
                skip_next_lines = 3  # Skip the next 3 lines after 'CELL_PARAMETERS'
                continue  # Skip the 'CELL_PARAMETERS' line itself
            # Skip the next lines if flagged
            if skip_next_lines > 0:
                skip_next_lines -= 1
            else:
                new_lines.append(line)  # Keep this line if we are not skipping it

        return new_lines
  
