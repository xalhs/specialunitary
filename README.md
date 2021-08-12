# SpecialUnitary
An upgraded version of the spin-addition algorithm that can calculate states in irredudible representations (irr/rep) of any SU(N). Basic functions include tensor product between an arbitrary amount of fundamental representations, tensor product of any two representations (which can also be used to calculate Clebsch-Gordan coefficients), constructing any representation using the fundamental again and more.

## Quick Start
1. pip install sympy
2. in main.py change in line 2 ```N = 5``` to whatever SU(N) you want to work in 
3. And then just run main.py, as an example it should produce an irr/rep with Dynkin label [1,1,1,1] (dimension 1024).
4. In the optimized version currently the build_object2 function is supported so you can use build_object2(label) as in ```irrep = func.build_object([1,1,1])``` to create an irr/rep of that label
5. In the vanilla version can also use the ```build_object(label)``` function after importing ```import vanilla.functions.producing_functions as v_func``` for example as in ```irrep = v_func.build_object([1,1,1])``` for the same purpose as in the optimized version if you create two such irr/rreps for example ```irrep1```, ```irrep2```. You can find the resulting tensor product of the two with ```irrep3 = v_func.add_object_to_object(irrep1 , irrep2)```

## Differences between optimized and vanilla version
The vanilla version is the first realization of the algorithm, it works but on higher SU(N)s and larger irr/reps it proves too slow. That's why the optimized version was developed to reduce that time. It achieves that by noticing that in the vanilla version you have to make the same calculation multiple times over (mainly on ladder operators). Thus the optimized version was developed. Usually functions involving the optimized part are named as {function}2. This naming convention might change soon but for now it holds. Using optimized functions generally produces a different type of irreps that are in a condensed form, meaning that they are compacted into a sum of tensor products of multiple smaller states. Most vanilla functions will not work on optimized states/irreps and vice versa. Some optimized irreps (those that are composed of only one tensor product) can be converted to their vanilla counterparts by using the ```.expand_tensor_products()``` method.

## To be added
More functions for the optimized version  
Functions to plot the irr/reps
List of methods/functions and their use

## to be added in README
theory  
more info on how to use
