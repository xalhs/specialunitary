from operator import add, sub
import sympy
from sympy import sqrt
from sympy import*
from vanilla.util.util import*
#from vanilla.classes.state import*
from main import N

global vectors
vectors =[[0 for x in range(N)] for y in range(N)]
for i in range(0,N):
    vectors[i][i] = 1

class Base:
    def __init__(self, coefficient, base):
        if coefficient == 0:
            return
        self.base = base
        self.coefficient = coefficient

    def add_base(self, coefficient, base):
        self.base.append(base)
        self.coefficient.append(coefficient)
