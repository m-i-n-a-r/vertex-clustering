import operator
from collections import OrderedDict
from shingle_utils import matching_vectors

# NEEDED PARAMETERS

shingle_dict = {}
pruning_treshold = 20 # default: 20

# STEP ONE

# Testing purpose
tuple_shingle1 = (198,202,163,100,56,7,180,98)
tuple_shingle2 = (102,3,4,5,96,'*',98,240)
tuple_shingle3 = (198,202,163,100,56,'*',180,'*')
tuple_shingle4 = (12,36,42,5,77,90,98,240)
shingle_dict[tuple_shingle1] = 24
shingle_dict[tuple_shingle2] = 1
shingle_dict[tuple_shingle3] = 30
shingle_dict[tuple_shingle4] = 2
# STEP TWO

# Order the dictionary by value
shingle_dict = OrderedDict(sorted(shingle_dict.items(), key = operator.itemgetter(1)))

# Process every shingle vector without wildcards
for vector in shingle_dict:
    if '*' not in vector:
        # Given the dictionary with every matching vector, delete the vector with the highest count
        matching_vectors_dict = matching_vectors(vector, shingle_dict)
        del matching_vectors_dict[max(matching_vectors_dict.items(), key = operator.itemgetter(1))[0]]
        # Decrease the count for every other matching vector
        for key in matching_vectors_dict:
            shingle_dict[key] -= shingle_dict[vector]
                
# Delete every masked shingle vector with a count less than a given treshold
shingle_dict = {key:val for key, val in shingle_dict.items() if val > pruning_treshold or '*' not in key}
        
# STEP THREE