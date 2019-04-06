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
    if not 0 <= treshold <= 50: sys.exit("The number is too big, small or is not a number")
except:
    treshold = 20
    print("The number is too big, small or is not a number. The value was set to default.")

try:
    shingle_size = input("\nShingle size [blank for default] -> ")
    shingle_size = int(shingle_size)
    if not 5 <= shingle_size <= 50: sys.exit("The number is too big, small or is not a number")
except:
    shingle_size = 10
    print("The number is too big, small or is not a number. The value was set to default.")

print("\n...computing...\n")
try:
    clusters = vertex_clusterer(treshold, shingle_size)
except:
    print("Something went wrong: malformed or small pages, internal error.")

if not clusters: 
    sys.exit("\nNo cluster found or failure.")

# Preparing the coordinates and the colorscale
json_ready_dict = {}
pages_in_cluster = []
shingle_of_cluster = []
colors = []
for cluster in clusters:
    pages_in_cluster.append(len(clusters[cluster]))
    json_ready_dict[str(cluster)] = list(clusters[cluster])
    shingle_of_cluster.append(str(cluster))

for i in range(0,len(shingle_of_cluster)): 
    colors.append(i)

# Preparing the chart
data = [go.Bar(
    x = shingle_of_cluster,
    y = pages_in_cluster,
    name = 'Vertex Clustering',
       marker = {
        'color': colors,
        # Colorscale type. Other possible options below
        # Blackbody Bluered Blues Earth Electric Greens Greys Hot Jet Picnic Portland Rainbow RdBu Reds Viridis YlGnBu YlOrRd
        'colorscale': 'Viridis' 
    }
)]

config = {
    'scrollZoom': True,
    'displaylogo': False,
    'watermark': False
    }

layout = go.Layout(
    title = 'Vertex Clustering',
    xaxis = dict(
        title = 'CLUSTERS - TOTAL: ' + str(len(colors)),
            titlefont = dict(
            family = 'Arial, sans-serif',
            size = 18,
            color = '#777777'
        ),
        showticklabels = False,
        rangemode = 'nonnegative',
        autorange = True
    ),
    yaxis = dict(
        title = 'NUMBER OF PAGES',
            titlefont = dict(
            family = 'Arial, sans-serif',
            size = 18,
            color = '#777777'
        ),
        rangemode = 'nonnegative',
        autorange = True
    ), 
)

# Printing and saving the chart
fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig, filename = 'clusters.html', config = config)

# Write the clusters in a json file
json_ready_dict = {'Clusters': json_ready_dict}
with open('clusters.json', 'w') as file:
     file.write(json.dumps(json_ready_dict))

# All done, confirmation message
print("\nDone. The plot is in the current folder, as well as a json containing every cluster and its set of pages.\n")