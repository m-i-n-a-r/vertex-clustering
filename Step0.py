import os
import requests
import urllib3
from bs4 import BeautifulSoup
import random
from crccheck.crc import Crc8
import glob

#Input: an URL
#Output: a list of tags in HTML Page
def getTagFromUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    tagList = []

    try:
        # Retrying for failed requests
        for i in range(1):
            # Generating random delays
            #sleep(randint(1, 3))
            # Adding verify=False to avold ssl related issues
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in soup.find_all():
                    tagList.append(tag.name)
                return tagList

            elif response.status_code == 404:
                break

    except Exception as e:
        print (e)

#Input: an HTML Page
#Output: a list of tags in HTML Page
def getTag(html):
    tagList = []
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all():
        tagList.append(tag.name)
    return tagList

#Input: list of tags in the html page, l window space
#Output: a set of CRC 8 hashed string. String are made from each l consecutive tags in the html page.
def getSet(tagList, l):
    n = l-1
    tagSet = set()
    for i in range(len(tagList)-n):
        # Hash the shingle to a 8-bit
        str = ' '.join(tagList[i:i+l])
        #CRC 8 Hash
        crc = Crc8.calc(str.encode('utf-8'))
        tagSet.add(crc)
    return tagSet


maxShingleID = 2 ** 8 - 1
nextPrime = 257

# Generate a list of 'k' random coefficients for the random hash functions,
# while ensuring that the same value does not appear multiple times in the
# list.
def pickRandomCoeffs(k):
    # Create a list of 'k' random values.
    randList = []

    while k > 0:
        # Get a random shingle ID.
        randIndex = random.randint(0, maxShingleID)

        # Ensure that each random number is unique.
        while randIndex in randList:
            randIndex = random.randint(0, maxShingleID)

            # Add the random number to the list.
        randList.append(randIndex)
        k = k - 1

    return randList

#Coefficients for hash function
coeffA = pickRandomCoeffs(8)
coeffB = pickRandomCoeffs(8)

# START List of independent hash function H(x) = (aX+b)%c
# Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is
# a prime number just greater than maxShingleID.
def hashTuple1(x):
    return ((coeffA[0]*x)+coeffB[0])%maxShingleID

def hashTuple2(x):
    return ((coeffA[1]*x)+coeffB[1])%maxShingleID

def hashTuple3(x):
    return ((coeffA[2]*x)+coeffB[2])%maxShingleID

def hashTuple4(x):
    return ((coeffA[3]*x)+coeffB[3])%maxShingleID

def hashTuple5(x):
    return ((coeffA[4]*x)+coeffB[4])%maxShingleID

def hashTuple6(x):
    return ((coeffA[5]*x)+coeffB[5])%maxShingleID

def hashTuple7(x):
    return ((coeffA[6]*x)+coeffB[6])%maxShingleID

def hashTuple8(x):
    return ((coeffA[7]*x)+coeffB[7])%maxShingleID
# END Hash Function

#Apply 8 independet hash function to the set of CRC 8 hash string of l tag
def getVector(tagSet):
    return  min(map(hashTuple1, tagSet)),min(map(hashTuple2, tagSet)),min(map(hashTuple3, tagSet)),min(map(hashTuple4, tagSet)),min(map(hashTuple5, tagSet)),min(map(hashTuple6, tagSet)),min(map(hashTuple7, tagSet)),min(map(hashTuple8, tagSet))


def readFile():
    page_shingle_dict = {}

    # Path containing http pages
    path = '/Users/regini/untitled/*.html'
    files = glob.glob(path)

    for file in files:
        with open(file) as fp:
            #Take tags from the HTML page
            tagList = getTag(fp)
        #Get shingle vector from the set of l consecutive tags
        vector = getVector(getSet(tagList, 10))

        path, filename = os.path.split(file)
        #Add filename in a dictionary where key is the shingle vector
        page_shingle_dict[vector] = filename

    print (page_shingle_dict)

if __name__ == "__main__":
    #Worning for https requests
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    readFile()



