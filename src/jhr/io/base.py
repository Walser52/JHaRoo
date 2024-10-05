def modify_input_file(input_file, output_file, **kwargs):
    """Update the input file with various parameter values."""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            updated_line = line
            for param, value in kwargs.items():
                if param in line:
                    if isinstance(value, str):
                        # Add quotes around string values
                        updated_line = f"  {param} = '{value}',\n"
                    else:
                        # For non-string values
                        updated_line = f"  {param} = {value},\n"
                    break  # Break after updating the line for the specific parameter
            file.write(updated_line)
  return


