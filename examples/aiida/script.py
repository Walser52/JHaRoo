from aiida import orm
from aiida.engine import calcfunction, workfunction

@calcfunction
def add(x, y):
    return x + y

@calcfunction
def multiply(x, y):
    return x * y

@workfunction
def add_multiply(x, y, z):
    """Add two numbers and multiply it with a third."""
    addition = add(x, y)
    product = multiply(addition, z)
    return product


node1 = orm.Int(2)
node2 = orm.Int(3)

node3 = add(node1, node2)

# print(node)

# @calcfunction
# def times2( number ):
#   return 2 * number

# @calcfunction
# def plus1( number ):
#   return 1 + number

# data0 = orm.Int( 10 )
# data1 = times2(number=data0)
# data2 = plus1(number=data1)