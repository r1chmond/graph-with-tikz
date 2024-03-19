
from app import main_app
from app.data import ParsedData
from app.tikz_generator import TikzCodeGenerator
from app.graph import Graph, Edge, Vertex
from app import sugiyama
from app import graph
import os
import tkinter as tk

d = ParsedData("crossing_example.json")


print("================== Original Graph ==================\n")
G = Graph(d.get_parsed_data())
G.print_graph()

print("\n=============== Cycles removed =====================\n")
sugiyama.dfs_cycle_removal(G)

G.print_graph()
print("\n===============Top Sort =====================\n")

V = sugiyama.topological_ordering(G)
print(f"{V=}")

print("\n===============Layered =====================\n")
layered_G = sugiyama.longest_path_layer_assigment(G)

layered_G.print_graph()

print("\n===============Dummy vertices added =====================\n")
sugiyama.add_dummy_vertices(layered_G)
layered_G.print_graph()


sugiyama.init_ordering(layered_G)

print("\n=============== crossing reduction =====================\n")
for v in layered_G.get_ordering().values():
    print(v)
sugiyama.cross_reduction(layered_G)


print("\n=============== bfs shortest path =====================\n")
print("\n=============== x cord  =====================\n")
v = layered_G.get_vertex("idx1")
p,l, n = sugiyama.bfs_single_source_shortest_path(layered_G, v)


x_cor = sugiyama.x_coordinate_assignment(layered_G)
layered_G.print_graph()
print("\n=============== bfs tree  =====================\n")
print(l)
print("\n=============== predecessors  =====================\n")
for v,l in p.items():
    print(v,l)
print("\n=============== num of shortest paths  =====================\n")
for v, i in n.items():
    print(v, i)
    

# print("\n=============== paths  =====================\n")
# paths = sugiyama.find_paths(p)
# for a,b in paths:
#     print(f"({a[0]}, {a[1]}) -> {b}")


print("\n=============== centrality  =====================\n")
bc = sugiyama.vertex_centrality(layered_G)
for v, i in bc.items():
    print(f"{v} -=-=-=- {i}")

# print("\n=============== x cord assigment  =====================\n")
# d = sugiyama.x_coordinate_assignment(layered_G)
# for i,j in d.items():
#     print(i, j)
# #
# print("================== Vertex ordering ==================\n")
# sugiyama.vertex_ordering(layered_G)
 
# print("================== x cordinates ==================\n")
# ordered = sugiyama.vertex_positioning(layered_G)
# for k,v in ordered.ordering.items():
#     print(f"{k}: {v} \n")
# print("================== reverse layers ==================\n")
# sugiyama.reverse_layers(layered_G)
# layered_G.print_graph()

# print("================== init order ==================\n")
# v = layered_G.get_source_vertices()[0]
# pos = sugiyama.init_ordering(layered_G,v)

# for k,v in pos.items():
#     print(f"{k}: {v} \n")
    

# print("================== adj pos ==================\n")

# for i in range(5):
#     sugiyama.weighted_median_sweep(layered_G,pos,i,5)
#     print("================== adj pos ==================\n")
#     print(pos)
    
# # print("================== total crossings ==================\n")
# # print(f"{app.visualisation.overall_crossing(layered_G,pos)=}")
   
# print("================== transpose ==================\n")
# sugiyama.transpose(layered_G,pos)

# for k,v in pos.items():
#     print(f"{k}: {v} \n")
    

# print(f"{adj_pos=}")
# t = TikzCodeGenerator(layered_G)

# code = t.generate_tikz_code()
# print(code)

# print("\n===============vertex promoted =====================\n")

# c = t1.generate_tikz_code()
# print(c)




# """Start GUI"""
# root = tk.Tk() 
# app = main_app.TikzCodeGeneratorApp(root)
# root.minsize(500,600)
# root.maxsize(800, 620)
# root.mainloop()
