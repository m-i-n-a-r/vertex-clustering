import sys
import csv
import json
import plotly as py
import plotly.graph_objs as go
from vertex_clusterer import vertex_clusterer

version = "0.2"
clusters = {}

# Set the values to avoid null arguments
name = ""
file_number = 300

print("\nVertex Clusterer V " + version + "\n")

# Ask for the source
source_type = input("\nSource: c for csv, f for pages folder [blank for default] -> ")
if source_type == 'c' or source_type == 'C':
    try:
        name = input("\nFile name, with extension -> ")
        file_number = input("\nNumber of links to scan in the file [blank for default] -> ")
        file_number = int(file_number)
    except:
        print("Incorrect or empty value. Default set (20 percent of the site or 2000)")
        try:
            csv = open(name)
        except:
            sys.exit("File not found!")    
        
        # Calculate the default value (20% of the site, and 2000 if 20% < 2000)
        row_count = sum(1 for row in csv)
        file_number = row_count // 5
        if file_number < 2000:
            file_number = 2000

elif source_type == 'f' or source_type == 'F':
    pass
else:
    source_type = 'f'
    print("Wrong values. Default set (/pages folder).")

# Ask for the treshold and shingle size
try:
    treshold = input("\nPruning treshold [blank for default] -> ")
    treshold = int(treshold)
    if not 1 <= treshold <= 50:
        sys.exit()
except:
    treshold = 20
    print("The number is too big, small or is not a number. Default set (20).")

try:
    shingle_size = input("\nShingle size [blank for default] -> ")
    shingle_size = int(shingle_size)
    if not 5 <= shingle_size <= 50:
        sys.exit()
except:
    shingle_size = 10
    print("The number is too big, small or is not a number. Default set (10).")

print("\n...COMPUTING...\n")

# Execute the algorithm
try:
    clusters = vertex_clusterer(treshold, shingle_size, source_type, name, file_number)
except Exception as e:
    print(e)

if not clusters:
    sys.exit("\nNo cluster found or failure.\n")

# Preparing the coordinates and the colorscale
json_ready_dict = {}
pages_in_cluster = []
shingle_of_cluster = []
colors = []
for cluster in clusters:
    pages_in_cluster.append(len(clusters[cluster]))
    json_ready_dict[str(cluster)] = list(clusters[cluster])
    shingle_of_cluster.append(str(cluster))

for i in range(0, len(shingle_of_cluster)):
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
    )
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
