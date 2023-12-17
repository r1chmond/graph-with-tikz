import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
from collections import OrderedDict

class DirectedGraph():
    pass



# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_node("A",node_color="yellow", node_shape="<", label="start")
G.add_nodes_from([("B",{"node_color": "red","node_shape":"v", "label": "process"}),("C",{"node_color": "green", "node_shape":"8", "label": "end"})])

# Add edges
G.add_edge("A", "B")
G.add_edge("B", "C")
G.add_edge("C", "A")

node_color_map=["red", "yellow", "green"]
node_shapes=["s","o","D"]

# G.nodes[0]["style"] = "blue"
# Display the graph
# custom_pos = {"A": (0, 0), "B": (1, 1), "C": (2, 0)} # Define the layout for better visualization
custom_colors = {"A": "red", "B": "green"}
pos = nx.spring_layout(G)
# pos = nx.spring_layout(G)
nodes_attr = {n: G.nodes[n] for n in G.nodes}
print(f"{nodes_attr=}")

num_of_nodes = len(G.nodes)
nodes = OrderedDict()
for n in G.nodes:
    nodes[n] = G.nodes[n]

bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3)
for node in nodes:
    nx.draw_networkx_nodes(node,pos,node_color=nodes[node]["node_color"],bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3))

labels = {}
for n in nodes:
    labels[n] = nodes[n]["label"]
    
# nx.draw_networkx(G,pos,labels=labels,bbox=dict(facecolor="skyblue", boxstyle="round", pad=0.3))
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G, pos, labels=labels)



# Show the plot
plt.show()