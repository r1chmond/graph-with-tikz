
from app import main_app
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
def file_new_action():
    print("New")
def file_open_action(s):
    print(s)
def file_save_action():
    print("Save")
def about_menu_action():
    print("About clicked !!!")

def exit_application():
    root.destroy()
    
root = tk.Tk()
root.geometry("700x580")
root.title("Tikz Code Generator App")
icon_img = tk.PhotoImage(file=os.path.join("icons/tex.png"))
root.iconphoto(False,icon_img)

root.tk.call("tk","windowingsystem")
root.option_add("*tearOff", False) #remove dotted lines before menu options

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar)
file_menu.add_command(label="New", command=file_new_action)
file_menu.add_command(label="Open", command=lambda: file_open_action("Open!!!"))
file_menu.add_command(label="Save/Export", command=file_save_action)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_application)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar)
help_menu.add_command(label="Documentation")
help_menu.add_command(label="About", command=about_menu_action)
menubar.add_cascade(label="Help", menu=help_menu)

#left section
left_mainframe = tk.Frame(root,padx=5,pady=5)
left_mainframe.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

#toolbar
l_tools_frame = tk.Frame(left_mainframe, bg="skyblue")
l_tools_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
add_image = tk.PhotoImage(file=os.path.join("icons/add-file.png"))
addfile_btn = tk.Button(l_tools_frame,text="Add", image=add_image)
addfile_btn.pack(side=tk.RIGHT, padx=(0,10))

#listbox
l_list_frame = tk.Frame(left_mainframe, bg="green")
l_list_frame.pack(fill=tk.X, pady=10)

items = ["tester.json", "chart.json"]
list_items = tk.Variable(value=items)
list_box = tk.Listbox(l_list_frame, listvariable=list_items)
list_box.pack()

#status
l_status_frame = tk.Frame(left_mainframe, bg="purple")
l_status_frame.pack(side=tk.BOTTOM)

status_label = tk.Label(l_status_frame,text="status")
status_label.pack(side=tk.LEFT)

#right section
right_mainframe = tk.Frame(root,padx=5,pady=5)
right_mainframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

r_top_frame = tk.Frame(right_mainframe, bg="purple")
r_top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
image = tk.PhotoImage(file=os.path.join("icons/export.png"))
export_btn = tk.Button(r_top_frame, image=image)
export_btn.pack(side=tk.RIGHT, padx=(0,15))

r_middle_frame = tk.Frame(right_mainframe, bg="green")
r_middle_frame.pack(fill=tk.X, pady=10)
textbox = tk.Text(r_middle_frame)
textbox.pack(padx=5,pady=5)

r_bottom_frame = tk.Frame(right_mainframe, bg="purple")
r_bottom_frame.pack(side=tk.BOTTOM)


visualise_btn = tk.Button(right_mainframe,text="Visualise",)
generate_btn = tk.Button(right_mainframe,text="Generate Tikz Code",)

visualise_btn.pack(side=tk.RIGHT, padx=(10, 30))
generate_btn.pack(side=tk.RIGHT)

root.config(menu=menubar)
root.minsize(500, 600)
root.maxsize(800, 620)
root.mainloop()

