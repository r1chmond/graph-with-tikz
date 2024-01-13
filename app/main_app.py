from app.tikz_generator import TikzCodeGenerator
from app.data import ParsedData
import tkinter as tk

class MainApp:
    def __init__(self,path: str)-> None:
        self._parsed_data = ParsedData(path)
        self.gen = TikzCodeGenerator(self._parsed_data.get_parsed_data())
        
    def print_tikz_code(self):
        code = self.gen.generate_tikz_code()
        print(code)

# TODO:
# What if processes have the same?
#  Consider swapping "id" with "label"
# eg: "idx2": {"label":"walk", "type": "process"}

class App(tk.Frame):
    def __init__(self, master=None)-> None:
        super().__init__(master)
        self.pack()
        self.create_menubar()
        
    
    
    def create_menubar(self)-> None:
        self.menubar = tk.Menu(self)

        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label="New", command=self.file_new_action)
        file_menu.add_command(label="Open", command=lambda: self.file_open_action("Open!!!"))
        file_menu.add_command(label="Save/Export", command=self.file_save_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        self.menubar.add_cascade(label="File", menu=file_menu)

        # help_menu = tk.Menu(self.menubar)
        # help_menu.add_command(label="Documentation")
        # help_menu.add_command(label="About", command=about_menu_action)
        # self.menubar.add_cascade(label="Help", menu=help_menu)
    
    def file_new_action(self):
        print("New")
    
    def file_open_action(self,s):
        print(s)
        
    def file_save_action(self):
        print("Save")
        
    def about_menu_action(self):
        print("About clicked !!!")

    def exit_application(self):
        self.destroy()
    
# root = tk.Tk()
# root.geometry("700x580")
# root.title("Tikz Code Generator App")
# icon_img = tk.PhotoImage(file=os.path.join("icons/tex.png"))
# root.iconphoto(False,icon_img)

# root.tk.call("tk","windowingsystem")
# root.option_add("*tearOff", False) #remove dotted lines before menu options



# #left section
# left_mainframe = tk.Frame(root,padx=5,pady=5)
# left_mainframe.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# #toolbar
# l_tools_frame = tk.Frame(left_mainframe, bg="skyblue")
# l_tools_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
# add_image = tk.PhotoImage(file=os.path.join("icons/add-file.png"))
# addfile_btn = tk.Button(l_tools_frame,text="Add", image=add_image)
# addfile_btn.pack(side=tk.RIGHT, padx=(0,10))

# #listbox
# l_list_frame = tk.Frame(left_mainframe, bg="green")
# l_list_frame.pack(fill=tk.X, pady=10)

# items = ["tester.json", "chart.json"]
# list_items = tk.Variable(value=items)
# list_box = tk.Listbox(l_list_frame, listvariable=list_items)
# list_box.pack()

# #status
# l_status_frame = tk.Frame(left_mainframe, bg="purple")
# l_status_frame.pack(side=tk.BOTTOM)

# status_label = tk.Label(l_status_frame,text="status")
# status_label.pack(side=tk.LEFT)

# #right section
# right_mainframe = tk.Frame(root,padx=5,pady=5)
# right_mainframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# r_top_frame = tk.Frame(right_mainframe, bg="purple")
# r_top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
# image = tk.PhotoImage(file=os.path.join("icons/export.png"))
# export_btn = tk.Button(r_top_frame, image=image)
# export_btn.pack(side=tk.RIGHT, padx=(0,15))

# r_middle_frame = tk.Frame(right_mainframe, bg="green")
# r_middle_frame.pack(fill=tk.X, pady=10)
# textbox = tk.Text(r_middle_frame)
# textbox.pack(padx=5,pady=5)

# r_bottom_frame = tk.Frame(right_mainframe, bg="purple")
# r_bottom_frame.pack(side=tk.BOTTOM)


# visualise_btn = tk.Button(right_mainframe,text="Visualise",)
# generate_btn = tk.Button(right_mainframe,text="Generate Tikz Code",)

# visualise_btn.pack(side=tk.RIGHT, padx=(10, 30))
# generate_btn.pack(side=tk.RIGHT)

   