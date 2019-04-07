import os
import requests
import urllib3
from bs4 import BeautifulSoup
import random
from crccheck.crc import Crc8
import glob
import csv
import sys
from random import randint
from time import sleep

# Input: an URL
# Output: a list of tags in HTML Page
def get_tag_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    tagList = []

    try:
        # Retrying for failed requests
        for i in range(10):
            # Generating random delays
            #sleep(randint(1, 3))
            # Adding verify = False to avold ssl related issues
            response = requests.get(url, headers = headers, verify = False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in soup.find_all():
                    tagList.append(tag.name)
                return tagList

            elif response.status_code == 404:
                break

    except Exception as e:
        print(e)

# Input: an HTML Page
# Output: a list of tags in HTML Page
def get_tag(html):
    tag_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all():
        tag_list.append(tag.name)
    return tag_list

# Input: list of tags in the html page, l window space
# Output: a set of CRC 8 hashed string. String are made from each l consecutive tags in the html page.
def get_set(tag_list, l):
    if tag_list is not None:
        list_size = len(tag_list)
        n = l - 1
        tag_set = set()
        if (list_size - n)>0 and tag_list is not None:
            for i in range(len(tag_list) - n):
                # Hash the shingle to a 8-bit
                str = ' '.join(tag_list[i:i + l])
                # CRC 8 Hash
                crc = Crc8.calc(str.encode('utf-8'))
                tag_set.add(crc)
            return tag_set
        else:
            return tag_set

max_shingle_ID = 2 ** 8 - 1
next_prime = 257

# Generate a list of 'k' random coefficients for the random hash functions,
# while ensuring that the same value does not appear multiple times in the list
def pick_random_coeffs(k):
    # Create a list of 'k' random values.
    rand_list = []

    while k > 0:
        # Get a random shingle ID.
        rand_index = random.randint(0, max_shingle_ID)

        # Ensure that each random number is unique.
        while rand_index in rand_list:
            rand_index = random.randint(0, max_shingle_ID)

            # Add the random number to the list.
        rand_list.append(rand_index)
        k -= 1

    return rand_list


# Coefficients for hash function
coeffA = pick_random_coeffs(8)
coeffB = pick_random_coeffs(8)

# START List of independent hash function H(x) = (aX+b)%c
# Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is
# a prime number just greater than maxShingleID.
def hash_tuple1(x):
    return ((coeffA[0] * x) + coeffB[0]) % max_shingle_ID

def hash_tuple2(x):
    return ((coeffA[1] * x) + coeffB[1]) % max_shingle_ID

def hash_tuple3(x):
    return ((coeffA[2] * x) + coeffB[2]) % max_shingle_ID

def hash_tuple4(x):
    return ((coeffA[3] * x) + coeffB[3]) % max_shingle_ID

def hash_tuple5(x):
    return ((coeffA[4] * x) + coeffB[4]) % max_shingle_ID

def hash_tuple6(x):
    return ((coeffA[5] * x) + coeffB[5]) % max_shingle_ID

def hash_tuple7(x):
    return ((coeffA[6] * x) + coeffB[6]) % max_shingle_ID

def hash_tuple8(x):
    return ((coeffA[7] * x) + coeffB[7]) % max_shingle_ID
# END Hash Function

# Apply 8 independet hash function to the set of CRC 8 hash string of l tag
def get_vector(tag_set):
    return min(map(hash_tuple1, tag_set)), min(map(hash_tuple2, tag_set)), min(map(hash_tuple3, tag_set)), min(map(hash_tuple4, tag_set)), min(map(hash_tuple5, tag_set)), min(map(hash_tuple6, tag_set)), min(map(hash_tuple7, tag_set)), min(map(hash_tuple8, tag_set))

# Main method to generate the shingle:page dictionary starting from a directory
def read_file(shingle_size):
    page_shingle_dict = {}

    # Path containing http pages
    script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
    rel_path = "pages/*.html"
    abs_file_path = os.path.join(script_dir, rel_path)
    files = glob.glob(abs_file_path)

    for file in files:
        with open(file) as fp:
            # Take tags from the HTML page
            tag_list = get_tag(fp)
        # Get shingle vector from the set of l consecutive tags
        if tag_list:
            tag_set = get_set(tag_list, shingle_size)
            if tag_set:
                vector = get_vector(tag_set)

                abs_file_path, filename = os.path.split(file)
                # Add filename in a dictionary where key is the shingle vector
                page_shingle_dict[filename] = vector

    return page_shingle_dict

# Main method to generate the shingle:page dictionary starting from a csv
def read_csv(shingle_size, csvname, linknumber):
    page_shingle_dict = {}
    rownumber = 0  
    try:
        open(csvname)
    except:
        sys.exit("File not found!")    
    # Path containing http pages
    with open(csvname) as csvfile:
        reader = csv.DictReader(csvfile)
        # For each row, read the second link
        for row in reader:
            url = list(row.values())[1]
            tag_list = get_tag_from_url(url)
            if tag_list is not None:
                # Get shingle vector from the set of l consecutive tags
                tag_set = get_set(tag_list, shingle_size)
                if tag_set:
                    vector = get_vector(tag_set)
                    # Add filename in a dictionary where key is the shingle vector
                    page_shingle_dict[url] = vector
                    rownumber = rownumber + 1
                    print(rownumber) # TODO probably useless
                if rownumber == linknumber:
                    break

    print (page_shingle_dict)
    return page_shingle_dict

# Input: a shingle vector and a dictionary containing every shingle and its count
# Output: a dictionary containing the vectors which cover the input vector and their count
def matching_vectors(vector, shingle_dict):
    matching_dict = {}

    # Scan the keys in the dictionary, find every matching vector and add it to another dictionary
    for candidate_vector in shingle_dict:
        if match(candidate_vector, vector):
            matching_dict[candidate_vector] = shingle_dict[candidate_vector]

    return matching_dict

# Input: two shingle vectors (tuple)
# Output: 1 if the vectors match, else 0
def match(s1, s2):
    for i in range(8):
        if (s1[i] != s2[i] and s1[i] != '*' and s2[i] != '*'):
            return 0
    return 1

# Input: a shingle vector
# Output: dictionary containing every masked shingle vector with a count of 0
def generate_6_7_from_8_shingle_vec(shingle_vec):
    # Initialize the final dictionary and a temporary dictionary
    H = {}
    H_temp = {}

    shingle_dict = {shingle_vec: 0}

    # For each 8/8 shingle, replace an element with a wildcard for each element and add the result to the temporary dictionary
    for key in shingle_dict:
        for m in range(8):
            a = ()
            for n in range(8):
                if m != n:
                    a = a + (key[n],)
                else:
                    a = a + ("*",)
            H_temp[a] = 0

    # For each 7/8 shingle, replace an element with a wildcard for each element and add the result to the final dictionary
    for key in H_temp.keys():
        for m in range(8):
            a = ()
            for n in range(8):
                if m != n:
                    a = a + (key[n],)
                else:
                    a = a + ("*",)
            H[a] = 0

    # Add the 8/8 shingle to the final dictionary
    H[shingle_vec] = 0
    return H

# Input: the final dictionary (shingle:count), another shingle dictionary
# Output: a shingle:count dictionary with the right counts
def dict_shingle_occurencies(H, a):

    for key in a:
        x = H.get(key)
        if x == None:
            H[key] = 1
        else:
            y = H.get(key)
            y = y+1
            H[key] = y
    return H
