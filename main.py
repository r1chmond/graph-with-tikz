
from app import main_app
from app.data import ParsedData
from app.tikz_generator import TikzCodeGenerator
from app.graph import Graph, Edge, Vertex
from app import sugiyama
from app import graph
import os
import tkinter as tk

d = ParsedData("example_2.json")


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

# print("================== Vertex ordering ==================\n")
# sugiyama.vertex_ordering(layered_G)
 
# print("================== x cordinates ==================\n")
# ordered = sugiyama.vertex_positioning(layered_G)
# for k,v in ordered.ordering.items():
#     print(f"{k}: {v} \n")
# print("================== reverse layers ==================\n")
# sugiyama.reverse_layers(layered_G)
# layered_G.print_graph()

print("================== init order ==================\n")
v = layered_G.get_source_vertices()[0]
pos = sugiyama.init_ordering(layered_G,v)

for k,v in pos.items():
    print(f"{k}: {v} \n")
    

print("================== adj pos ==================\n")

for i in range(5):
    sugiyama.weighted_median_sweep(layered_G,pos,i,5)
    print("================== adj pos ==================\n")
    print(pos)
    
# print("================== total crossings ==================\n")
# print(f"{app.visualisation.overall_crossing(layered_G,pos)=}")
   
print("================== transpose ==================\n")
sugiyama.transpose(layered_G,pos)

for k,v in pos.items():
    print(f"{k}: {v} \n")
    

# print(f"{adj_pos=}")
# t = TikzCodeGenerator(layered_G)

# code = t.generate_tikz_code()
# print(code)

# print("\n===============vertex promoted =====================\n")

# c = t1.generate_tikz_code()
# print(c)




"""Start GUI"""
root = tk.Tk() 
app = main_app.TikzCodeGeneratorApp(root)
root.minsize(500,600)
root.maxsize(800, 620)
root.mainloop()


# a = Vertex("id1","a")
# b = Vertex("id2","b")
# c = Vertex("id3","c")
# d = Vertex("id4","d")

# e1 = Edge(a, b, 1)
# e2 = Edge(a, c, 1)
# e3 = Edge(b, a, 0)
# e4 = Edge(b, d, 1)
# e5 = Edge(d, b, 0)
# e6 = Edge(d, c, 1)
# e7 = Edge(c, c, 1)

# edges = {e1,e3,e6,e7,e2,e5,e4}

# G = Graph(edges)
# print("================== Original Graph ==================\n")
# G.print_graph()

# print("\n=============== Cycles removed =====================\n")
# G_no_cycle = app.visualisation.dfs_cycle_removal(G)

# G_no_cycle.print_graph()

# print("\n===============Layered and Dummy vertices added =====================\n")
# layered_G = app.visualisation.longest_path_layer_assigment(G_no_cycle)

# layered_G.print_graph()

# v_promo = app.visualisation.vertex_promotion_heuristic(layered_G)
# print("\n=============== =====================\n")
# for v in v_promo.vertices:
#     print(f"{v} layer: {v.layer}")
    


# from schemdraw import flow
# import schemdraw

# with schemdraw.Drawing() as d:
#     flow.Terminal().label('START')
#     flow.Arrow().down(d.unit/3)
#     h = flow.Decision(w=5.5, h=4, S='YES').label('Hey, wait,\nthis flowchart\nis a trap!')
#     flow.Line().down(d.unit/4)
#     flow.Wire('c', k=3.5, arrow='->').to(h.E)
#     d.draw()