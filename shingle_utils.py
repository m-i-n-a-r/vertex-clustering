# input: a shingle vector and a dictionary containing every shingle and its count
# output: a dictionary containing the vectors which cover the input vector and their count
def matching_vectors(vector, shingle_dict):
    # Testing purpose
    test_dict = {}
    test_dict['012 003 040 056 007 098 233 100'] = 3
    test_dict['102 003 004 005 096 007 080 190'] = 1
    return test_dict