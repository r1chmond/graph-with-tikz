from app.tikz_generator import TikzCodeGenerator
from app.data import ParsedData
import tkinter as tk
from tkinter import filedialog as fd
import os


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

class TikzCodeGeneratorApp:
    def __init__(self, root: tk.Tk)-> None:
        self.root = root
        self.root.geometry("700x580")
        self.root.title("Tikz Code Generator App")
        icon_img = tk.PhotoImage(file=os.path.join("icons/tex.png"))
        self.root.iconphoto(False, icon_img)
        self.left_mainframe = tk.Frame(self.root, padx=5, pady=5)
        self.list_box = tk.Listbox(self.left_mainframe,selectmode=tk.SINGLE, width= 30)
        
        self.radio_count = 0
        self.filepath_list=[]
        self.current_filepath = "/"
        
        self.create_menubar()
        self.create_left_section()
        self.create_right_section()
        
    
    def create_menubar(self)-> None:
        self.root.tk.call("tk","windowingsystem")
        self.root.option_add("*tearOff", False) #remove dotted lines before menu options

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="New", command=self.file_new_action)
        file_menu.add_command(label="Open", command=self.file_open_action)
        file_menu.add_command(label="Save/Export", command=self.file_save_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar)
        help_menu.add_command(label="Documentation")
        help_menu.add_command(label="About", command=self.about_menu_action)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_left_section(self) -> None:
        
        self.left_mainframe.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.create_toolbar(self.left_mainframe)
        # self.create_listbox(self.left_mainframe)
        self.create_status_bar(self.left_mainframe)
    
    def create_toolbar(self, parent_frame: tk.Frame) -> None:
        l_tools_frame = tk.Frame(parent_frame, bg="skyblue")
        l_tools_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        add_image = tk.PhotoImage(file=os.path.join("icons/add-file.png"))
        addfile_btn = tk.Button(l_tools_frame, text="Add", image=add_image)
        addfile_btn.image = add_image #add reference to image ..ref garbage collection
        addfile_btn.configure(image=add_image)
        addfile_btn.pack(side=tk.RIGHT, padx=(0, 10))  

    def create_listbox(self, parent_frame: tk.Frame) -> None:
        l_list_frame = tk.Frame(parent_frame, bg="green")
        l_list_frame.pack(fill=tk.X, pady=10)
        self.list_box.pack()
    
        
    def create_status_bar(self, parent_frame: tk.Frame) -> None:
        l_status_frame = tk.Frame(parent_frame, bg="purple")
        l_status_frame.pack(side=tk.BOTTOM)

        status_label = tk.Label(l_status_frame, text="status")
        status_label.pack(side=tk.LEFT)
        
    def create_right_section(self) -> None:
        right_mainframe = tk.Frame(self.root, padx=5, pady=5)
        right_mainframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_right_top_frame(right_mainframe)
        self.create_right_middle_frame(right_mainframe)
        self.create_right_bottom_frame(right_mainframe)
    
    def create_right_top_frame(self, parent_frame: tk.Frame) -> None:
        r_top_frame = tk.Frame(parent_frame, bg="purple")
        r_top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        image = tk.PhotoImage(file=os.path.join("icons/export.png"))
        export_btn = tk.Button(r_top_frame, image=image)
        export_btn.image = image
        export_btn.pack(side=tk.RIGHT, padx=(0, 15))
        
    def create_right_middle_frame(self, parent_frame: tk.Frame) -> None:
        r_middle_frame = tk.Frame(parent_frame, bg="green")
        r_middle_frame.pack(fill=tk.X, pady=10)

        textbox = tk.Text(r_middle_frame)
        textbox.pack(padx=5, pady=5)
    
    def create_right_bottom_frame(self, parent_frame: tk.Frame) -> None:
        r_bottom_frame = tk.Frame(parent_frame, bg="purple")
        r_bottom_frame.pack(side=tk.BOTTOM)

        visualise_btn = tk.Button(parent_frame, text="Visualise")
        generate_btn = tk.Button(parent_frame, text="Generate Tikz Code")

        visualise_btn.pack(side=tk.RIGHT, padx=(10, 30))
        generate_btn.pack(side=tk.RIGHT)
        
    def file_new_action(self):
        print("New")
    
    def file_open_action(self) -> None:
        filetypes = (("json files", "*.json"),("All files", "*,*"))
        filepath = fd.askopenfilename(title="Open file",
                                        initialdir=os.path.join("/"),
                                        filetypes=filetypes
        )
        var = tk.IntVar() 
        var.set(1)
        def on_select():
            selection = var.get()
            print(f"{selection=}")
        
        pathexist = filepath in [path for path,count in self.filepath_list]
        if filepath and not pathexist: 
            self.radio_count += 1 
            self.filepath_list.append((filepath,self.radio_count))
           
            for widget in self.left_mainframe.winfo_children():
                if widget.winfo_name() == "!radiobutton":
                    widget.destroy()

                
            for path, value in self.filepath_list:
                radio_btn = tk.Radiobutton(self.left_mainframe,text=self.get_filename(path), variable=var, value=value, width=30, command=on_select)
                radio_btn.pack(pady=5)
            
        
    def file_save_action(self):
        print("Save")
        
    def about_menu_action(self):
        print("About clicked !!!")

    def exit_application(self):
        self.root.destroy()
    
    def get_filename(self, path: str):
        i = len(path) - 1
        while i >= 0 and path[i] != "/" and path[i] != "\\":
            i -= 1
        return path[i+1:]
    

   