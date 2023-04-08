import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

print('*' * 30)
print("Note that rendering of a whole country might take a while and uses your PC memory as well as your network!")
print("Monaco and Vatican City are not included, the reason for that is that they don't have their own powerlines!")
fpath = input("Select location in which files will be saved in (example format: 'C:/EUROPEMAP/'): ")
print('*' * 30)

# All countries that are fully in Europe
countries = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
             "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
             "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein",
             "Lithuania", "Luxembourg", "Malta", "Moldova", "Montenegro", "Netherlands",
             "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino",
             "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
             "United Kingdom"]

country = []
while True:
    lowercase_countries = [i.lower() for i in countries]

    cty = input("Choose a European country that you want a graph and plot of: ")

    cty = cty.lower()
    if cty in lowercase_countries:
        country.append(cty)
    else:
        print("This country is either not in Europe or doesn't exist!")

    nxt = input("Do you want to add another country to graph and plot? y/n: ")
    if nxt != 'y' and nxt != 'Y':
        break

print("Countries you've chosen are:")
for i in country:
    print(i.capitalize())

print('*' * 30)
print("Creating a graph based on your preferences")
print('*' * 30)

# Filtering all the electricity data in the countries of choice
cf = '["power"~"line|cable"]'
electricity_lines = ox.graph_from_place(
        country,
    custom_filter=cf,
    retain_all=True,
    simplify=True,
    truncate_by_edge=True,
    buffer_dist=200,
    clean_periphery=True
)

# Creating a base graph and saving it to a file
prj_elec = ox.project_graph(electricity_lines)
ox.save_graph_shapefile(prj_elec, filepath=fpath) #Choose the location you desire

# Reading edges and nodes
edges = gpd.read_file(fpath+'edges.shp')
nodes = gpd.read_file(fpath+'nodes.shp')

# Checking the data of .shp files (edges, nodes)
print('*' * 30)
while True:
    ne_data = input("Do you want to see .shp files data? y/n: ")
    if ne_data != 'y' and ne_data != 'Y':
        break
    else:
        print(edges.head())
        print(edges.columns)
        print(nodes.head())
        print(nodes.columns)
        break

# Creating graph
G = nx.Graph()

# Adding nodes to a graph
for index, row in nodes.iterrows():
    G.add_node(row['osmid'], posx=float(row['x']), posy=float(row['y']))


# Adding edges to a graph
for index, row in edges.iterrows():
    G.add_edge(row['u'], row['v'], id=row['osmid'], length=row['length'])

# Creating tuple using node data
posy = nx.get_node_attributes(G, 'posy')
pos = {k:(x, posy[k]) for k, x in nx.get_node_attributes(G, 'posx').items()}

# Printing a tuple of coordinates
print('*' * 30)
while True:
    cord_data = input("Do you want to see the coordinates? y/n: ")
    if cord_data != 'y' and cord_data != 'Y':
        break
    else:
        print(pos)
        break

# Putting all the data into a G graph
nx.draw(G, pos, node_color='blue', node_size=50, with_labels=False)
plt.show()

# Saving the graph in a .graphml format
print('*' * 30)
while True:
    cord_data = input("Do you want to save the graph in a graphml format? y/n: ")
    if cord_data != 'y' and cord_data != 'Y':
        break
    else:
        nx.write_graphml(G, fpath+"GRAPH.graphml")
        break

# Creating a matplotlib plot
fig, ax = plt.subplots(figsize=(12, 8))
edges.plot(ax=ax)
nodes.plot(ax=ax, color='red', markersize=5)

# Saving the plot in .png format
print('*' * 30)
while True:
    cord_data = input("Do you want to save the plot in a .png format? y/n: ")
    if cord_data != 'y' and cord_data != 'Y':
        break
    else:
        plt.savefig(fpath+'Matplotlib_plot.png')
        break
plt.show()





















