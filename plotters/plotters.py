import matplotlib.pyplot as plt

print("abc")

def bands(a, b, savefile = 'test.pdf'):

    plt.plot(a,b, color = 'pink')
    plt.savefig(savefile, format = 'pdf')
#    plt.show()

    return 

#if __name__ == '__main__':
#    plt.figure()    
#    a = [1,2,3]
#    b = [1,2,4]
#
#    bands(a, b, 'test1')
#    plt.show()
#
#    a = [1,2,3]
#    b = [4,3,2]
#    bands(a,b, 'test2')
#    plt.show()
