from plotters import bands
#import plotters
import matplotlib.pyplot as plt

# subprocess.run('python plotters.py', shell = True)

plt.figure()    
a = [1,2,3]
b = [1,2,4]

bands(a, b, 'test1')
plt.show()

a = [1,2,3]
b = [4,3,2]
bands(a,b, 'test2')
plt.show()
