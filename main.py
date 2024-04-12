from app import tikz_generator_app
from app.data import ParsedData
from app.tikz_generator import TikzCodeGenerator
from app.graph import Graph, Edge, Vertex
from app import sugiyama
from app import graph
import os
import tkinter as tk

"""Start GUI"""
root = tk.Tk()
app = tikz_generator_app.TikzCodeGeneratorApp(root)

root.minsize(500, 600)
root.maxsize(800, 620)
root.mainloop()
