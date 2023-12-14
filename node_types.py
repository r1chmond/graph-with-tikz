class Terminator:
   pass

class AOrEnd:
    pass

class Decision:
    pass 


import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
from collections import OrderedDict

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

# import networkx as nx
# import matplotlib.pyplot as plt

# # Generate a random tree with its node positions
# G = nx.random_tree(14, seed=100, create_using=nx.DiGraph)
# pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

# # Compute lowest-common ancestors for certain node pairs
# ancestors = list(nx.all_pairs_lowest_common_ancestor(G, ((1, 3), (4, 9), (13, 10))))

# # Create node color and edge color lists
# node_color_map = []
# edge_color_map = []
# for i in range(14):
#     node_color_map.append("#D5D7D8")
#     edge_color_map.append("None")
# template = ["#FFE799", "#FFD23F", "#CEB6E2", "#A77CCB", "#88DFE7", "#45CDD9"]
# x = 0
# for i in ancestors:
#     for j in i[0]:
#         node_color_map[j] = template[x]
#     x += 1
#     node_color_map[i[1]] = template[x]
#     edge_color_map[i[1]] = "black"
#     x += 1

# # Plot tree
# plt.figure(figsize=(15, 15))
# plt.title("Visualize Lowest Common Ancestors of node pairs")
# nx.draw_networkx_nodes(
#     G, pos, node_color=node_color_map, node_size=2000, edgecolors=edge_color_map
# )
# nx.draw_networkx_edges(G, pos)
# nx.draw_networkx_labels(G, pos, font_size=15)
# plt.show()