# Error handlers. 

class Error:
  def __init__():
    pass

  @staticmethod
  def no_output_file(file):
    if file_out is None:
        raise ValueError("Provide output file name")
    return

  @staticmethod
  def missing_parameter(param, message = 'Missing parameter'):
#    message = f'param.__name__ missing.'
    if param is None:
        raise ValueError(message)
    return
