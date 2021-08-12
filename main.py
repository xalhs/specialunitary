global N
N = 5

if __name__ == '__main__':
    #import vanilla.functions.producing_functions as v_func
    #irreps = v_func.produce_all_objects(3)
    #print(irreps)
    import functions.irrep_producing_functions as func
    irrep = func.build_object2([1,1,1,1])
    print(irrep)
