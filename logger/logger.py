# Input file path
# Pass to pwtk script
# Wait to calculation to finish
# If calculation has finished, update the JSON log file? 

Class Calculation:
  def __init__(self, type = 'scf', pp = 'pbe', **kwargs):
    Calculation.type = type
    Calculation.pp = pp
    # Calculation.kpoint = 


    Calculation.meta = {'type': type, 'pp': pp} 
    return


Class Log:
  def __init__(self, matname):
    Log.material = matname
    Log.state = {Log.material: ''}
    return
  def append(self, what, where):
    #Add 'what' to the right 'where'.
    return



fp = ''

# Calculation
for i in arange(1,1000):
  i+1

# 
# log = {'matname': 'scf'}

log = Log()


