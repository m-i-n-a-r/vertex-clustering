# input: a shingle vector and a dictionary containing every shingle and its count
# output: a dictionary containing the vectors which cover the input vector and their count
def matching_vectors(vector, shingle_dict):
    matching_dict = {}

    # Scan the keys in the dictionary, find every matching vector and add it to another dictionary
    for candidate_vector in shingle_dict:
        if match(candidate_vector, vector):
            matching_dict[candidate_vector] = shingle_dict[candidate_vector]

    return matching_dict

# input: two shingle vectors (tuple)
# output: 1 if the vectors match, else 0
def match(s1, s2):
    for i in range(8):
        if (s1[i] != s2[i] and s1[i] != '*' and s2[i] != '*'):
            return 0
    return 1
