import operator
from collections import OrderedDict
from shingle_utils import matching_vectors

# NEEDED PARAMETERS

shingle_dict = {}
pruning_treshold = 20 # default: 20

# STEP ONE

# Testing purpose
shingle_dict['001 200 163 100 056 007 180 222'] = 2
shingle_dict['102 003 004 005 096 007 080 190'] = 1
shingle_dict['012 003 040 056 007 098 233 100'] = 3
shingle_dict['* 200 034 005 160 * 009 156'] = 2
shingle_dict['* 200 134 056 022 090 088 233'] = 4

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
shingle_dict = {key:val for key, val in shingle_dict.items() if val > pruning_treshold}
        
# STEP THREE