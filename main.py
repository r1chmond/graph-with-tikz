
from app import main_app
from app.data import ParsedData
from app.tikz_generator import TikzCodeGenerator
from app.visualisation import Graph, Edge, Vertex
import app.visualisation
import os
import tkinter as tk

# code = main_app.MainApp(os.path.join('tester.json'))

# code.print_tikz_code()


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


"""Start GUI"""
# root = tk.Tk() 
# app = main_app.TikzCodeGeneratorApp(root)
# # app.list_box.bind("<<ListboxSelect>>", app.on_select)
# root.minsize(500,600)
# root.maxsize(800, 620)
# root.mainloop()



    
# data = ParsedData("tester.json")
# it_data = data.get_parsed_data()
# gen = TikzCodeGenerator(it_data)
# code = gen.generate_tikz_code()

# with open("tikz.tex","w") as f:
#     f.write(code)

# print(code)

# di = DirectedGraph()
# di.visualise()
a = Vertex("a")
b = Vertex("b")
c = Vertex("c")
d = Vertex("d")

e1 = Edge(a, b, 1)
e2 = Edge(a, c, 1)
e3 = Edge(b, a, 0)
e4 = Edge(b, d, 1)
e5 = Edge(d, b, 0)
e6 = Edge(d, c, 1)
e7 = Edge(c, c, 1)

edges = {e1,e3,e6,e7,e2,e5,e4}

G = Graph(edges)

G.print_graph()

print("====================================\n")

G_no_cycle = app.visualisation.dfs_cycle_removal(G)

G_no_cycle.print_graph()
print("====================================\n")

layered_G = app.visualisation.longest_path_layer_assigment(G_no_cycle)

layered_G.print_graph()

# v_promo = app.visualisation.vertex_promotion_heuristic(layered_G)
# print("====================================\n")
# for v in v_promo.vertices:
#     print(f"{v} layer: {v.layer}")
    
