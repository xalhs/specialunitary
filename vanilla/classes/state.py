from operator import add, sub
from sympy import sqrt
from sympy import*
from vanilla.util.util import*
from vanilla.classes.base import*
from main import N

class State:

    def __init__(self, bases=None):

        self.bases = bases


        if bases != None:
            self.content = self.get_content()
            self.normalize()
        else:
            self.content = []
            self.bases = []

    def get_content(self):
        content = empty.copy()
        for component in self.bases[0].base:
            try:
                content = list(map(add , content , component))
            except:
                content = list(map(add , content , component.content))

        return content

    def get_spin_proj(self):
        return sum(self.bases[0].base)

    def __eq__(self, state):
        if not isinstance(state , State):
            return False
        prod = InnerProduct(self , state)
        if prod == 1:
            return True
        elif prod == 0:
            return False
        else:
            raise TypeError("I don't know why this would ever occur " + str(type(self)) + " " + str(type(state)))

    def __mul__(self, constant):
        new_state = State(None)
        for base in self.bases:
            new_state.add_dimension(constant*base.coefficient , base.base)
        return new_state

    def __rmul__(self,constant):
        return self.__mul__(constant)

    def __add__(self , state):
        new_state = State(None)
        for base in self.bases:
            new_state.add_dimension(base.coefficient , base.base)

        for base in state.bases:
            new_state.add_dimension(base.coefficient , base.base)

        return new_state

    def remove_dimension (self, remove_base):
        for i , base in enumerate(self.bases):
            if base.base== remove_base:
                self.bases.pop(i)
                return

    def add_dimension(self, new_coef, new_base):
        try:

            if sum(new_base) != self.spin:
                return
        except:
            pass

        try:
            for base in self.bases:
                if base.base == new_base:
                    base.coefficient += new_coef
                    if base.coefficient == 0:
                        self.remove_dimension(base.base)
                    return
        except:
            pass

        if new_base == [] or new_coef == 0:
            return

        if self.content == []:
            content = empty.copy()
            for component in new_base:
                try:
                    content = list(map(add , content , component))
                except:
                    content = list(map(add , content , component.content))

            self.content = content

        self.bases.append(Base(new_coef , new_base))

    def normalize(self):
        global_coef = 0
        for base in self.bases:
            coef = base.coefficient
            global_coef += coef*coef

        for base in self.bases:
            base.coefficient *= sqrt(global_coef)/global_coef

        return sqrt(global_coef)

    def latexify(self):
        a = ""
        for i , base in enumerate(self.bases):
            try:
                if self.bases[i+1].coefficient > 0:
                    a+= base.latexify() + "+"
                else:
                    a+= base.latexify() + "-"
            except:
                a+= base.latexify()

        return a

    def __repr__(self):
        if N <= 6:
            for i in range(6-N):
                try:
                    vectors[5-i] = [0,0,0,0,0,0]
                except:
                    vectors.append([0,0,0,0,0,0])
            s0 = str([ (' Coefficient: ' + repr(base.coefficient) + ' Bases: ' + repr(base.base).replace(str(vectors[0]) , "u").replace(str(vectors[1]) , "d").replace(str(vectors[2]) , "s").replace(str(vectors[3]) , "c").replace(str(vectors[4]) , "b").replace(str(vectors[0]), "t")) for base in self.bases])
        else:
            for i in range(vectors):
                s0 = str([ (' Coefficient: ' + repr(base.coefficient) + ' Bases: ' + repr(base.base).replace(str(vectors[i]) , "e" + str(i))) for base in self.bases])
        return s0

def Orthogonal2(base_states , States):
    if len(States) != (len(base_states)-1):
        Raise("DimensionError")
        return
    A = [[0 for x in range(len(base_states) -1 )] for y in range(len(base_states) -1)]
    new_state = State(None)
    for k, base_state in enumerate(base_states):
        for i  , state in enumerate(States):
            for j , base_state_2 in enumerate(base_states):
                if j != k:
                    if j< k:
                        A[i][j] = InnerProduct(base_state_2 , state)
                    else:
                        A[i][j-1] = InnerProduct(base_state_2 , state)


        new_state +=  ((-1)**k)*(Matrix(A).det())*base_state


    return new_state

def gramschmidt(states):
    M =[[0 for x in range(len(states))] for y in range(len(states))]
    for i , state in enumerate(states):
        for j in range(i):
            numer = -1*InnerProduct(states[i] , states[j])
            denom = InnerProduct(states[j] , states[j])
            for base in states[j].bases:
                states[i].add_dimension(base.coefficient*numer/denom , base.base)

    del_list = []
    for  k ,state in enumerate(states):
        if state.bases == []:
            del_list.append(k)

    for delet in reversed(del_list):
        del states[delet]

    return states

def InnerProduct(state1 , state2):
    prod = 0
    if state1 == None or state2 == None:
        return 0
    for base in state1.bases:
        for same_base in state2.bases:
            if base.base == same_base.base:
                prod += base.coefficient*same_base.coefficient
                #break

    return prod

def Ladder(state ,  from_base , to_base ):
    if state == None:
        return

    new_state = State( None  )

    for base in state.bases:
        for index  in range(len(base.base)):
            new_base = []
            for second_index , spin_0 in enumerate(base.base):
                temp_base = [0  for x in range(N)]
                spin = spin_0
                new_coeff = base.coefficient
                if second_index == index:
                    if spin[from_base] == 1:
                        temp_base[from_base] = 0
                        temp_base[to_base] = 1
                        new_coeff = base.coefficient
                        new_base.append(temp_base)
                    else:
                        new_base = []
                        new_coeff = 0
                        break

                else:
                    new_base.append(spin)

            new_state.add_dimension( new_coeff, new_base)

    if new_state.bases == []:
        return

    return new_state

def tensor_product(state1, state2):
    new_state = State(None)
    for base1 in state1.bases:
        for base2 in state2.bases:
            new_base = []
            new_coef = []
            new_base = base1.base + base2.base
            new_coef = base1.coefficient * base2.coefficient
            new_state.add_dimension(new_coef , new_base)

    return new_state
