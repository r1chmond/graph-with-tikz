from app import tikz_generator_app
from app.data import ParsedData
from app.tikz_generator import TikzCodeGenerator
from app.graph import Graph, Edge, Vertex
from app import sugiyama
from app import graph
import os
import tkinter as tk



d = ParsedData("json_examples/tester.json")
data = d.get_parsed_data()

g = Graph(data)
print(f"-=-=-=-=--=-=-=-=--=-=-=--topological sort-=-=-=--=-=-=-=--=-=-=-=-=--=-=")
topo_v = sugiyama.topological_ordering(g)
print(topo_v)



"""Start GUI"""
# root = tk.Tk()
# app = tikz_generator_app.TikzCodeGeneratorApp(root)

# root.minsize(500, 600)
# root.maxsize(800, 620)
# root.mainloop()
