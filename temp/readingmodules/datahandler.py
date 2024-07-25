
def checker(a):
  check = [True if type(elem) == int or type(elem) == float else False for elem in a]

  return check 
