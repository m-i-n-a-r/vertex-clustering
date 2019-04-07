import operator
from collections import OrderedDict
import shingle_utils as utils


# Input: a set of html files
# Output: a clusters-pages dictionary
def vertex_clusterer(pruning, shingle, source_type, name, link_number):
    # NEEDED PARAMETERS
    page_shingle_dict = {}  # Shingle vector of the page : url or filename of the page
    clusters = {}  # Masked shingle vector which represents the cluster : set of pages in the cluster
    shingle_dict = {}  # Shingle vector or masked shingle vector : count
    pruning_treshold = pruning  # Default: 20
    shingle_size = shingle  # Default: 10

    # STEP ZERO
    # Prepare the set of pages to be computed
    if source_type == 'f' or source_type == 'F':
        page_shingle_dict = utils.read_file(shingle_size)
    if source_type == 'c' or source_type == 'C':
        page_shingle_dict = utils.read_csv(shingle_size, name, link_number)

    # STEP ONE
    # For every shingle, generate every 6/8, 7/8 and 8/8 shingles and masked shingles
    # Given every shingle, build a shingle:count dictionary with the right counts
    for vector in page_shingle_dict:
        temporary_dict = utils.generate_6_7_from_8_shingle_vec(vector)
        shingle_dict = utils.dict_shingle_occurencies(shingle_dict, temporary_dict)

    # STEP TWO
    # Order the dictionary by value
    shingle_dict = OrderedDict(
        sorted(shingle_dict.items(), key=operator.itemgetter(1)))

    # Process every shingle vector without wildcards
    for vector in shingle_dict:
        matching_vectors_dict = {}
        if '*' not in vector:
            # Given the dictionary with every matching vector, delete the vector with the highest count
            matching_vectors_dict = utils.matching_vectors(
                vector, shingle_dict)
            del matching_vectors_dict[max(
                matching_vectors_dict.items(), key=operator.itemgetter(1))[0]]
        # Decrease the count for every other matching vector
            for key in matching_vectors_dict:
                shingle_dict[key] -= shingle_dict[vector]

    # Delete every masked shingle vector with a count less than a given treshold
    shingle_dict = {key: val for key, val in shingle_dict.items() if val > pruning_treshold or '*' not in key}

    # STEP THREE
    # Put every masked vector in a new dictionary
    shingle_masked_dict = {key: val for key, val in shingle_dict.items() if '*' in key}
    # Initialite the clusters to an empty set
    for masked_vector in shingle_masked_dict:
        clusters[masked_vector] = set()

    # For every shingle in the pages dictionary, find the matching masked shingle vector with the best score
    for shingle in page_shingle_dict:
        matching_dict = utils.matching_vectors(shingle, shingle_masked_dict)
        best_shingle = max(matching_dict.items(), key = operator.itemgetter(1))[0]
        # Add the page to the set of its cluster
        clusters[best_shingle].add(page_shingle_dict[shingle])
    # Return the dictionary
    return clusters
