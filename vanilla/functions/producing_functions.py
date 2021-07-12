from operator import add, sub
from sympy import sqrt
from sympy import*
from vanilla.util.util import*
from vanilla.classes.base import*
from vanilla.classes.state import*
from vanilla.classes.object import*
from main import N

def add_basic_to_object(object , n = N):
    new_state = State( None  )
    for base in object.top_state.bases:
        new_base = list(base.base)
        new_base.append(up)
        new_state.add_dimension(base.coefficient , new_base)


    new_label = list(object.label)
    new_label[0] +=1
    state_index = 0
    new_state.normalize()  #might be redundant
    new_obj = Object([new_state] , new_label)
    new_obj.fill()
    final = {'Objects': []}
    final['Objects'].append(new_obj)
    if n == state_index:
        return final['Objects'][n]

    for index, label  in enumerate(object.label):  # index = 0 means it adds one to 2nd row
        new_label = list(object.label)
        if index != N-2:
            new_label[index]-=1
            new_label[index+1]+=1
        else:
            new_label[index]-=1
        if label > 0:
            temp_base=[]
            starting_content = []

            loop_state = Ladder(new_state, 0 , index + 1)
            content_of_new = list(loop_state.content)

            for i in range(index+2):
                starting_content.append(list(content_of_new))
                starting_content[i][i] -= 1
            temp_state = []
            for  j , content  in enumerate(starting_content): #FIND states of object that have starting_content[i] as content
                for state in object.contents[tuple(content)]:
                    temp_base=[]
                    for base in state.bases:
                        debug_base = list(base.base)

                        debug_base.append(vectors[j].copy())

                        temp_base.append(Base(base.coefficient , debug_base))
                    temp_state.append(State(temp_base))
            prev_states = []
            for obj in final['Objects']:
                for state in obj.contents[tuple(content_of_new)]: #  take states that have the needed content
                    prev_states.append(state)

            newer_state = Orthogonal2(temp_state , prev_states)

            newer_state.normalize()

            newest_obj = Object([newer_state] , new_label)
            newest_obj.fill()

            final['Objects'].append(newest_obj)

            state_index +=1
            if n == state_index:
                return final['Objects'][n]


    return final

def add_basic_to_total(total):
    final = {'Objects': []}
    for obj in total['Objects']:
        temp = add_basic_to_object(obj)
        for object in temp['Objects']:
            final['Objects'].append(object)

    return final

def produce_all_objects(number):
    for i in range(number):
        if i == 0:
            continue
        elif i == 1:
            final = add_basic_to_object(basic)
        else:
            final = add_basic_to_total(final)

    return final

def add_object_to_object(obj1 , obj2 , n = None ):
    tot = {'Objects' : []}
    dict_of_contents = {}
    for content1 in obj1.contents:
        for content2 in obj2.contents:
            new_content = tuple(map(add, content1, content2))
            pos_bases = []
            for state1 in obj1.contents[content1]:
                for state2 in obj2.contents[content2]:
                    produced_state  = tensor_product(state1, state2)
                    pos_bases.append(produced_state)

            if new_content in dict_of_contents:
                dict_of_contents[new_content]["mult"]+=len(obj1.contents[content1])*len(obj2.contents[content2])

                dict_of_contents[new_content]["bases"]+=pos_bases
            else:
                dict_of_contents[new_content] = {"mult": len(obj1.contents[content1])*len(obj2.contents[content2]) , "bases": pos_bases}
    key_list = []
    for key in dict_of_contents:
        key_list.append(key)
    new_state = dict_of_contents[key_list[0]]['bases'][0]
    new_label = content_to_label(new_state.content)
    new_obj = Object([new_state] , new_label)
    tot['Objects'].append(new_obj)
    true_key_list = new_obj.fill(True)
    for key in true_key_list:
        try:
            dict_of_contents[key]["mult"]-=1

        except:
            pass
    for key in true_key_list:
        try:
            if dict_of_contents[key]["mult"] == 1:
                base_states = dict_of_contents[key]['bases']
                prev_states = []
                for obj in tot['Objects']:
                    try:
                        for state in obj.contents[key]:
                            prev_states.append(state)
                    except:
                        pass
                newer_state = Orthogonal2(base_states , prev_states)
                newer_state.normalize()
                newer_label = content_to_label(newer_state.content)
                newest_obj = Object([newer_state] , newer_label)
                new_key_list = newest_obj.fill(True)
                tot['Objects'].append(newest_obj)
                for key2 in new_key_list:
                    try:
                        dict_of_contents[key2]["mult"]-=1

                    except:
                        pass
            elif dict_of_contents[key]["mult"] > 1:
                mult = dict_of_contents[key]["mult"]
                base_states = dict_of_contents[key]['bases']
                prev_states = []
                for obj in tot['Objects']:
                    for state in obj.contents[key]:
                        prev_states.append(state)
                orthnorm_states  = gramschmidt(prev_states + base_states)
                new_states = orthnorm_states[-mult:]
                for newer_state in new_states:
                    newer_state.normalize()
                    newer_label = content_to_label(newer_state.content)
                    newest_obj = Object([newer_state] , newer_label)
                    new_key_list = newest_obj.fill(True)
                    tot['Objects'].append(newest_obj)
                    for key2 in new_key_list:
                        try:
                            dict_of_contents[key2]["mult"]-=1

                        except:
                            pass


        except:
            print("could be error")
            traceback.print_exc()

    return tot




    return tot

def build_object(label):
    label.reverse()
    final = basic
    for index, length in enumerate(label):  #each index creates a 2 dimensional structure hence 2 more indices
        for i in range(length):
            for j in range(N-index-1):
                if j==0 and i==0 and index==0:
                    pass
                else:
                    if j==0:
                        final = add_basic_to_object(final , j)
                    else:
                        final = add_basic_to_object(final , 1)

    label.reverse()
    return final
