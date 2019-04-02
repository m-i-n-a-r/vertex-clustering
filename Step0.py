import requests
from lxml import html
import urllib3
from bs4 import BeautifulSoup

def getTag(url):
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
        print e

def getSet(tagList, l):
    n = l-1
    tagSet = set()
    for i in range(len(tagList)-n):
        tagSet.add(tuple(tagList[i:i+l]))
    return tagSet

def getVector(tagSet):

    setHash1 = set()
    setHash2 = set()
    setHash3 = set()
    setHash4 = set()
    setHash5 = set()
    setHash6 = set()
    setHash7 = set()
    setHash8 = set()

    for tuple in tagSet:
        tmp1 = hashTuple1(tuple)
        setHash1.add(tmp1)

        tmp2 = hashTuple1(tuple)
        setHash2.add(tmp2)

        tmp3 = hashTuple1(tuple)
        setHash3.add(tmp3)

        tmp4 = hashTuple1(tuple)
        setHash4.add(tmp4)

        tmp5 = hashTuple1(tuple)
        setHash5.add(tmp5)

        tmp6 = hashTuple1(tuple)
        setHash6.add(tmp6)

        tmp7 = hashTuple1(tuple)
        setHash7.add(tmp7)

        tmp8 = hashTuple1(tuple)
        setHash8.add(tmp8)

    return min(setHash1), min(setHash2), min(setHash3), min(setHash4), min(setHash5), min(setHash6), min(setHash7), min(setHash8)


def hashTuple1(tuple):
    return hash(tuple)

# Se match tra due shingle vectors ritorno 1
def match(s1, s2):
    for i in range(8):
        if(s1[i]!=s2[i] and (s1[i]!="*" or s2[i]!="*")):
            return 0
    return 1


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    tagList = getTag("https://www.zalando.it/jcrew-scarf-sciarpa-graphite-jc452g006-c11.html")
    print getVector(getSet(tagList, 10))