from operator import add, sub
import sympy
from sympy import sqrt
from sympy import*
from vanilla.util.util import*
from vanilla.classes.base import*
from vanilla.classes.state import*
from main import N


class Object:

    def __init__(self, states, label=None , top_state = None):
        self.contents = {}
        self.states = states
        self.label = label
        self.top_state = self.states[0]
        for s in states:
            try:
                if s in self.contents[tuple(s.content)]:
                    pass
                else:
                    self.contents[tuple(s.content)].append(s)
            except:
                self.contents[tuple(s.content)] = [s]

    def __getitem__(self, key):
        return self.contents[key]

    def fill(self, tracking = False):

        new_state = self.top_state
        tuple_list = [tuple(new_state.content)]
        checkpoints = [new_state for  i in range(N-2)]
        checkpoints.append(None)
        end = False
        while end == False:       # 0 = u , 1 =d , 2 = s , 3= c
            for i in range(1 , N):
                loop_state = new_state
                for j in reversed(range(i)):
                    Degenerate = True
                    exists = False
                    new_state = Ladder(loop_state , j , i)
                    if new_state != None:
                        exists = True
                        for k in range(i-1):
                            checkpoints[k] = new_state

                    if loop_state.content == [0,1,2,3]:
                        Degenerate = True

                    if Degenerate and exists:
                        state_list = []
                        for h in range(j+1 , N):
                            try:
                                for available_state in self.contents[tuple(map(add, loop_state.content, list(map(sub, vectors[i],vectors[h])) ))]:
                                    temp = Ladder( available_state , j , h)
                                    temp.normalize()
                                    state_list.append(temp)
                            except:
                                pass

                        state_list = gramschmidt(state_list)
                        for ortho_state in state_list:
                            ortho_state.normalize()
                        self.contents[tuple(state_list[0].content)] = state_list
                        new_state = state_list[0]
                        for mult_state in state_list:
                            tuple_list.append(tuple(new_state.content))
                        break
                    else:
                        new_state = Ladder(loop_state , j , i)
                        if new_state != None:
                            new_state.normalize()

                            try:
                                if new_state in self.contents[tuple(new_state.content)]:
                                    pass
                                else:
                                    self.contents[tuple(new_state.content)].append(new_state)
                                    tuple_list.append(tuple(new_state.content))
                            except:
                                self.contents[tuple(new_state.content)] = [new_state]
                                tuple_list.append(tuple(new_state.content))
                            for k in range(i-1):
                                checkpoints[k] = new_state

                            break
                if new_state != None:
                    break
                else:
                    new_state = checkpoints[i-1]      #if "to s" fails, this  should go back to checkpoint after "to c"
            if new_state == None:
                end = True
        if tracking == True:
            return tuple_list

    def __repr__(self):
        dim = 0
        for content in self.contents:
            for state in self.contents[content]:
                dim +=1
        s0 = "label: " + str(self.label) + " dim: " + str(dim)
        return s0


basic = Object([State([Base(1 ,[up] )]) ], basic_label )
basic.fill()
