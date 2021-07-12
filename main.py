global N
N = 4

if __name__ == '__main__':
    import vanilla.functions.producing_functions as v_func
    irreps = v_func.produce_all_objects(3)
    print(irreps)
