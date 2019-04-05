import operator
from collections import OrderedDict
from shingle_utils import matching_vectors

# input: a set of html files
# output: a clusters-pages dictionary
def vertex_clusterer(pruning, shingle):
        # NEEDED PARAMETERS
        page_shingle_dict = {}
        clusters = {}
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
        # Put every masked vector in a new dictionary
        shingle_masked_dict = {key:val for key, val in shingle_dict.items() if '*' in key}
        # Initialite the clusters to an empty set
        for masked_vector in shingle_masked_dict:
                clusters[masked_vector] = set()

        # For every shingle in the pages dictionary, find the matching masked shingle vector with the best score
        for shingle in page_shingle_dict:
                matching_dict = matching_vectors(shingle, shingle_masked_dict)
                best_shingle = max(matching_dict.items(), key = operator.itemgetter(1))[0]
                # Add the page to the set of its cluster 
                clusters[best_shingle].add(page_shingle_dict[shingle])
        # Return the dictionary
        return clusters
        

