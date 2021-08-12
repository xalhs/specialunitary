from operator import add, sub
from sympy import sqrt
from sympy import*
from util.util import*
from main import N




vectors =[[0 for x in range(N)] for y in range(N)]
for i in range(0,N):
    vectors[i][i] = 1
if N <= 6:
    for i in range(6-N):
        try:
            vectors[5-i] = [0,0,0,0,0,0]
        except:
            vectors.append([0,0,0,0,0,0])


class Base:
    def __init__(self, coefficient, base):
        if coefficient == 0:
            return
        self.base = base
        self.coefficient = coefficient


    def add_base(self, coefficient, base):
        self.base.append(base)
        self.coefficient.append(coefficient)

    def latexify(self):
        if self.coefficient == 1:
            a = ""
        elif "/" in str(self.coefficient):
            a= "\\frac{" +  (str(self.coefficient).replace("/" , "}{")) + "}"
        else:
            a = str(self.coefficient)
        a = a.replace("-" , "")
        a = a.replace("sqrt(" , "\sqrt{").replace(")" , "}")
        if isinstance(self.base[0] , State):
            for component in self.base:
                a+="(" + component.latexify() + ")\\tens{}"
            a = a[:-7]

        else:
            a+= str((self.base)).replace(str(vectors[0]) , "u").replace(str(vectors[1]) , "d").replace(str(vectors[2]) , "s").replace(str(vectors[3]) , "c").replace(str(vectors[4]) , "b").replace(str(vectors[0]), "t").replace(", " , "").replace("[","").replace("]","")

        return a

class State:

    def __init__(self, bases=None):

        self.bases = bases
        if bases != None:
            self.content = self.get_content()
            self.normalize()
        else:
            self.content = []
            self.bases = []
        self.ladder = []
        self.topness = []
        for i in range(N):
            self.topness.append([])
            self.ladder.append([])
            for j in range(N):#-i):
                self.ladder[i].append([])
                self.topness[i].append([])

        self.label = [ None , None  , None]

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
        prod = InnerProduct(self , state)
        if prod == 1:
            return True
        elif prod == 0:
            return False
        else:
            raise TypeError("like I know why this occured OMEGALUL " + str(type(self)) + " " + str(type(state)))

    def __mul__(self, constant):
        new_state = State(None)
        new_state.label = self.label
        for base in self.bases:
            new_state.add_dimension(constant*base.coefficient , base.base)

        for i in range(len(self.ladder)):
            for j in range(len(self.ladder[i])):
                for k in range(len(self.ladder[i][j])):
                    new_state.ladder[i][j].append(constant*self.ladder[i][j][k])
        return new_state

    def __rmul__(self,constant):
        return self.__mul__(constant)

    def __add__(self , state):
        new_state = State(None)
        new_state.label = self.label
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

    def top_state_counter(self, n):      #takes the state as if it were a top state of an irrep of SU(n) and asssings a topness to it
        label = content_to_label(self.content)
        for i in range(1,n):
            for j in range(i):#-i):
                self.topness[i][j] = label[j]

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


def InnerProduct(state1 , state2):
    prod = 0
    if isinstance(state1 , State):
        pass
    else:
        if state1 == None:
            return 0
        else:
            raise TypeError("idk InnerProduct")
    if isinstance(state2 , State):
        pass
    else:
        if state2 == None:
            return 0
        else:
            raise TypeError("idk InnerProduct")
    try:
        if (state1.label[2] != None) and  ( state2.label[2] != None):
            if state1.label == state2.label:
                return 1
            else:
                return 0
    except:
        pass
#    if state1 == None or state2 == None:
    #    return 0
    for base in state1.bases:
        for same_base in state2.bases:
            if isinstance(base.base[0] , State):
                temp_prod = base.coefficient*same_base.coefficient
                for i , stat in enumerate(base.base):
                    if base.base[i].label == same_base.base[i].label:
                        if (base.base[i].label[0] == None or base.base[i].label[1] == None):
                            print("ERROR"*10)
                        pass
                    else:
                        temp_prod = 0
                prod += temp_prod
            elif base.base == same_base.base:
                prod += base.coefficient*same_base.coefficient
                #break

    return prod
