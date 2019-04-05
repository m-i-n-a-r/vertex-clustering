import sys
import json
import plotly as py
import plotly.graph_objs as go
from vertex_clusterer import vertex_clusterer

version = "0.1"
clusters = {}

# Ask for the treshold and shingle size
print("\nVertex Clusterer V " + version + "\n")

try:
    treshold = input("Pruning treshold [blank for default] -> ")
    treshold = int(treshold)
    if not 5 <= treshold <= 50: sys.exit("The number is too big, small or is not a number")
except:
    treshold = 20
    print("The number is too big, small or is not a number. The value was set to default.")

try:
    shingle_size = input("\nShingle size [blank for defult] -> ")
    shingle_size = int(shingle_size)
    if not 5 <= shingle_size <= 50: sys.exit("The number is too big, small or is not a number")
except:
    shingle_size = 10
    print("The number is too big, small or is not a number. The value was set to default.")

print("\n...computing...\n")
try:
    clusters = vertex_clusterer(treshold, shingle_size)
except:
    #sys.exit("Something went wrong")
    print("\ttesting\n") # TODO remove

if not clusters: 
    #sys.exit("No cluster found.")
    print("\ttesting\n") # TODO remove

# Test purpose
cluster_dict = {}
tuple_shingle1 = (198,202,163,100,56,7,180,98)
tuple_shingle2 = (102,3,4,5,96,'*',98,240)
tuple_shingle3 = (198,202,163,100,56,'*',180,'*')
tuple_shingle4 = (12,36,42,5,77,90,98,240)
tuple_shingle5 = (198,22,163,100,56,7,180,98)
tuple_shingle6 = (12,3,4,5,96,'*',98,240)
tuple_shingle7 = (198,'*',163,100,56,'*',180,'*')
tuple_shingle8 = (12,36,2,5,77,90,98,240)

set1 = set(["a", "b", "c", "d", "e"])
set2 = set(["c", "b", "q", "e", "d", "t", "i"])
set3 = set(["a", "b", "o", "e", "d", "s"])
set4 = set(["a", "l", "d", "e"])
set5 = set(["a", "o", "q", "i", "t"])
set6 = set(["o", "l", "t", "e", "d", "t", "u","m","w"])
set7 = set(["c", "b", "q", "e", "d", "t"])
set8 = set(["c", "b", "d", "t"])

cluster_dict[tuple_shingle1] = set1
cluster_dict[tuple_shingle2] = set2
cluster_dict[tuple_shingle3] = set3
cluster_dict[tuple_shingle4] = set4
cluster_dict[tuple_shingle5] = set5
cluster_dict[tuple_shingle6] = set6
cluster_dict[tuple_shingle7] = set7
cluster_dict[tuple_shingle8] = set8


# Preparing the coordinates
json_ready_dict = {}
pages_in_cluster = []
shingle_of_cluster = []
for cluster in cluster_dict:
    pages_in_cluster.append(len(cluster_dict[cluster]))
    json_ready_dict[str(cluster)] = list(cluster_dict[cluster])
    shingle_of_cluster.append(str(cluster))


# Preparing the chart
data = [go.Bar(
    x = shingle_of_cluster,
    y = pages_in_cluster,
    name = 'Clusters'
)]

# Printing and saving the chart
py.offline.plot(data, filename='clusters.html')

# Write the clusters in a json file
json_ready_dict = {'Clusters': json_ready_dict}
with open('clusters.json', 'w') as file:
     file.write(json.dumps(json_ready_dict))

# All done, confirmation message
print("\nDone. The plot is in the current folder.")