from operator import add, sub
import sympy
from sympy import sqrt
from sympy import*
from util.util import*
from classes.state import*
from functions.state_producing_functions import*
from main import N


from copy import deepcopy

class Object:

    def __init__(self, states, label=None , top_state = None):
        self.contents = {}
        self.states = states
        self.label = label
        self.top_state = self.states[0]
        self.top_state.top_state_counter(N)
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

    def fill(self, tracking = False):           #SAFE TO ASSUME, label[n]=a means a steps from n to N  as nth step

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

    def fill_2(self , obj1 , obj2 , tracking = False , skip_ladderfill = False ):           #SAFE TO ASSUME, label[n]=a means a steps from n to N  as nth step
        self.top_state.label = [self.label , self.top_state.content , 0]
        new_state = self.top_state
        new_state_content = new_state.content
        for top1 in range(len(new_state.topness)):
            for top2 in range(len(new_state.topness[top1])):
                try:
                    if new_state.topness[top1][top2] > 0:
                        arriving_content = tuple(map(add, new_state.content, list(map(sub, vectors[top1], vectors[top2]))))
                        if arriving_content in self.contents:
                            self.contents[(arriving_content)].append([new_state.content, new_state.label[2], top2, top1])
                        else:
                            self.contents[(arriving_content)] = [[new_state.content, new_state.label[2], top2, top1]]
                except:
                    pass


        tuple_list = [tuple(new_state.content)]
        checkpoints = [new_state.content for  i in range(N-2)]
        checkpoints.append(None)
        end = False
        while end == False:       ##### 0 = u , 1 =d , 2 = s , 3= c
            for i in range(1 , N):
                loop_state_content = new_state_content
                for j in reversed(range(i)):
                    Degenerate = True
                    exists = False
                    new_state_content = tuple(map(add, loop_state_content , list(map(sub, vectors[i],vectors[j])) ))   #this takes the role of the ladder
                    if new_state_content in self.contents:
                        exists = True
                        for k in range(i-1):
                            checkpoints[k] = new_state_content
                    if Degenerate and exists:
                        state_list = []
                        index_list = []
                        for numbering_index , info in enumerate(reversed(self[(new_state_content)])):
                            temp = Ladder2(self[tuple(info[0])][info[1]] , info[2] , info[3] , [obj1 , obj2])
                            temp.top_state_counter(info[3])
                            for temp_topness_2_index , temp_topness_2  in enumerate(self[tuple(info[0])][info[1]].topness[info[3]]):
                                if temp_topness_2_index > info[2] :
                                    temp.topness[info[3]][temp_topness_2_index] = 0
                                else:
                                    temp.topness[info[3]][temp_topness_2_index] = temp_topness_2
                            temp.topness[info[3]][info[2]] -= 1

                            for top1 in range(len(temp.topness)):
                                for top2 in range(len(temp.topness[top1])):
                                    try:
                                        if temp.topness[top1][top2] > 0:
                                            arriving_content = tuple(map(add, temp.content, list(map(sub, vectors[top1],vectors[top2])) ))
                                            if arriving_content in self.contents:
                                                self.contents[(arriving_content)].append([temp.content , numbering_index , top2 , top1])
                                            else:
                                                self.contents[(arriving_content)] = [[temp.content , numbering_index , top2 , top1]]
                                    except:
                                        pass

                            g_coef = temp.normalize()
                            state_list.append(temp)
                            index_list.append([self[tuple(info[0])][info[1]] , info[2] , info[3]  , g_coef ])
                        print("working on content: " + str(loop_state_content))
                        state_list_2 = state_list
                        [state_list, matrix] = gramschmidt2(state_list)

                     #       return state_list_2

                        for steet in state_list:
                            pass
                        for index_of_state , ortho_state in enumerate(state_list):
                            g2_coef = ortho_state.normalize()
                            ortho_state.label = [self.label , ortho_state.content , index_of_state  ]
                            for entry_index , entry in enumerate(index_list):
                                for nom in range(index_of_state - len(entry[0].ladder[entry[1]][entry[2]]) + 1):
                                    entry[0].ladder[entry[1]][entry[2]].append([])

                                entry[0].ladder[entry[1]][entry[2]][index_of_state] = matrix[entry_index][index_of_state]*entry[3]/g2_coef
                        self.contents[tuple(state_list[0].content)] = state_list
                        content = state_list[0].content
                        new_state = state_list[0]
                        for mult_state in state_list:
                            tuple_list.append(tuple(new_state.content))
                        break
                if exists:
                    break
                else:
                    new_state_content = checkpoints[i-1]      #if "to s" fails, this  should go back to checkpoint after "to c"
            if not exists:
                end = True
        if skip_ladderfill != True:
            self.fill_ladder_for_states(obj1 , obj2)
        else:
            print("SKIPPING LADDER FILL ")

        self.labelize()
        if tracking == True:
            return tuple_list

    def labelize(self):
        print("labelize start")
        for key in self.contents:
            for i , state in enumerate(self.contents[key]):
                state.label = [self.label , list(key) , i]
        print("labelize end")
    def fill_ladder_for_states(self , obj1 , obj2):
        print(" ladder fill start")
        for key in self.contents:
            for state in self.contents[key]:
                for i in range(N):
                    for j in range(i+1,N):
                        if state.ladder[i][j] == []:
                            temp = Ladder2(state , i , j , [obj1 , obj2])
                            try:
                                if temp == None:
                                    state.ladder[i][j] = None
                                else:
                                    for k, other_state in  enumerate(self.contents[tuple(temp.content)]):
                                        state.ladder[i][j].append(InnerProduct(temp, other_state))
                            except:
                                pass
        print(" ladder fill end")
    def expand_tensor_products(self):
        for key in self.contents:
            for m , state in enumerate(self.contents[key]):
                new_state = State(None)
                new_state.label = state.label
                for base in state.bases:
                    new_base = deepcopy(base.base[0])
                    new_base *= base.coefficient
                    new_state += tensor_product(new_base , base.base[1])
             #   new_state *= base.coefficient
                for i in range(len(state.ladder)):
                    for j in range(len(state.ladder[i])):
                        if state.ladder[i][j] == None:
                            new_state.ladder[i][j] == None
                        else:
                            for k in range(len(state.ladder[i][j])):
                                new_state.ladder[i][j].append(state.ladder[i][j][k])
                self.contents[key][m] = new_state
        self.top_state = self.contents[tuple(list(self.contents.keys())[0])][0]




    def __repr__(self):
        dim = 0
        for content in self.contents:
            for state in self.contents[content]:
                dim +=1
        s0 = "label: " + str(self.label) + " dim: " + str(dim)
        return s0


basic = Object([State([Base(1 ,[up] )]) ], basic_label )
basic.fill()
for key in basic.contents:
    basic[key][0].label = [(vectors[0].copy()).pop(-1) , list(key) , 0]
