# SpecialUnitary
An upgraded version of the spin-addition algorithm that can calculate states in irredudible representations (irr/rep) of any SU(N). Basic functions include tensor product between an arbitrary amount of fundamental representations, tensor product of any two representations (which can also be used to calculate Clebsch-Gordan coefficients), constructing any representation using the fundamental again and more.

## Quick Start
1. pip install sympy
2. in main.py change in line 2 ```N = 4``` to whatever SU(N) you want to work in 
3. And then just run main.py, as an example it should produce the representations occuring from the tensor product of 3 fundamental representations in your chosen SU(N).
4. In the vanilla version can also use the ```build_object(label)``` function for example as in ```irrep = v_func.build_object([1,1,1])``` to create an irr/rep of that label if you create two such irr/rreps for example ```irrep1```, ```irrep2```. You can find the resulting tensor product of the two with ```irrep3 = v_func.add_object_to_object(irrep1 , irrep2)```

## To be added
updated version of the algorithm

##to be added in README
theory
more info on how to use
