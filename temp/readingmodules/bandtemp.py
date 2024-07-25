from datahandler import checker


a = [1,2,1.2,4,5]

def btfuna(a):
  check = checker(a)

  if False in check:
    return "type mismatch"
  else:
    a = a*2
 
  return a


def btfunb(a):
  check = checker(a)

  if len(a) > 4:
    return "too long"
  else:
    a = a*2
 
  return a

  


b = btfuna(a)
print("Final array is: ", b)



