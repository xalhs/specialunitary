
from operator import add, sub
from sympy import sqrt
from sympy import*
from util.util import*
from classes.state import State,InnerProduct,vectors
from main import N


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
            M[i][j]= -1*numer
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

def gramschmidt2(states):
    number_of_states = len(states)
    M =[[0 for x in range(len(states))] for y in range(len(states))]
    for i , state in enumerate(states):
        for j in range(i):
            numer = -1*InnerProduct(states[i] , states[j])
            M[i][j]= -1*numer
            denom = InnerProduct(states[j] , states[j])
            for base in states[j].bases:
                states[i].add_dimension(base.coefficient*numer/denom , base.base)
        M[i][i]= InnerProduct(states[i] , states[i])

    del_list = []
    for  k ,state in enumerate(states):
        if state.bases == []:
            del_list.append(k)

    for delet in reversed(del_list):
        for i in range(len(M)):
            del M[i][delet]
        del states[delet]

    if len(states) != number_of_states:
        raise("DimensionError: expected linearly independent states")
    return [states,M]

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

def Ladder2(state , from_base, to_base , obj_lst):
    new_state = State(None)
    for base in state.bases:
        for i in range(2):
            if base.base[i].ladder[from_base][to_base] == []:
                new_base = base.base.copy()
                laddered_base = Ladder(base.base[i] ,  from_base, to_base)
                if laddered_base == None:
                    coef = 0
                    #break
                else:
                    content = laddered_base.content
                    for obj_state in obj_lst[i].contents[tuple(content)]:
                        coef = InnerProduct(laddered_base , obj_state)
                        new_coef = coef*base.coefficient
                        new_base[i] = obj_state
                        new_state.add_dimension( new_coef, new_base.copy())
            elif base.base[i].ladder[from_base][to_base] == None:
                coef = 0
                #break
            else:
                for  j, coef in enumerate(base.base[i].ladder[from_base][to_base]):
                    if coef != 0:
                        new_coef = coef*base.coefficient
                        new_base = base.base.copy()
                        new_base[i] = obj_lst[i].contents[tuple(map(add , base.base[i].content , list(map(sub, vectors[to_base],vectors[from_base]))))][j]
                        new_state.add_dimension( new_coef, new_base)

    if new_state.bases == []:
        return

    return new_state
