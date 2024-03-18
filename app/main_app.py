from app.tikz_generator import TikzCodeGenerator
from app.graph import Graph
from app import sugiyama
from app.data import ParsedData
import tkinter as tk
from tkinter import filedialog as fd, messagebox
import os
from app.file_handler import FileHandler
import subprocess
import pyperclip
from tktooltip import ToolTip
import time
from app import helper


MAX_FILENAME_LENGTH = 20

class TikzCodeGeneratorApp:
    def __init__(self, root: tk.Tk)-> None:
        self.root = root
        self.root.geometry("700x580")
        self.root.title("Tikz Code Generator App")
        icon_img = tk.PhotoImage(file=os.path.join("icons/tex.png"))
        self.root.iconphoto(False, icon_img)
        
        self.left_mainframe = tk.Frame(self.root, padx=5, pady=5)
        self.right_mainframe = tk.Frame(self.root, padx=5, pady=5)
        self.list_box = tk.Listbox(self.left_mainframe,selectmode=tk.SINGLE, width= 30)
        self.textbox = tk.Text(self.right_mainframe)
    
        self.filehandler = FileHandler()
        self.radio_count = 0
        self.filepath_list=[]
        self.current_filepath = os.path.join("/")
        self.status_label = None
        self.current_status = "status"
        self.tikz_code = ""
         
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
        self.create_status_bar(self.left_mainframe)
    
    def create_toolbar(self, parent_frame: tk.Frame) -> None:
        l_tools_frame = tk.Frame(parent_frame)
        l_tools_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        add_image = tk.PhotoImage(file=os.path.join("icons/add-file.png"))
        addfile_btn = tk.Button(l_tools_frame, text="Add", image=add_image, command=self.file_open_action)
        addfile_btn.image = add_image #add reference to image ..ref garbage collection
        addfile_btn.configure(image=add_image)
        addfile_btn.pack(side=tk.RIGHT, padx=(0, 10))  
        ToolTip(addfile_btn, msg= "Add JSON file")

    def create_listbox(self, parent_frame: tk.Frame) -> None:
        l_list_frame = tk.Frame(parent_frame)
        l_list_frame.pack(fill=tk.X, pady=10)
        self.list_box.pack()
    
        
    def create_status_bar(self, parent_frame: tk.Frame) -> None:
        l_status_frame = tk.Frame(parent_frame)
        l_status_frame.pack(side=tk.BOTTOM)
        self.status_label = tk.Label(l_status_frame, text= "status")
        self.status_label.pack(side=tk.LEFT)
        
    def create_right_section(self) -> None:
        self.right_mainframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_right_top_frame(self.right_mainframe)
        self.create_right_middle_frame(self.right_mainframe)
        self.create_right_bottom_frame(self.right_mainframe)
    
    def create_right_top_frame(self, parent_frame: tk.Frame) -> None:
        r_top_frame = tk.Frame(parent_frame)
        r_top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        image = tk.PhotoImage(file=os.path.join("icons/export.png"))
        export_btn = tk.Button(r_top_frame, image=image, command=self.file_save_action)
        export_btn.image = image
        export_btn.config(width=25, height=25)
        
        copy_image = tk.PhotoImage(file=os.path.join("icons/copy.png"))
        copy_btn = tk.Button(r_top_frame, image=copy_image, command=self.copy_btn_action)
        copy_btn.image = copy_image
        copy_btn.config(width=25, height=25)


        clear_image = tk.PhotoImage(file=os.path.join("icons/clear.png"))
        clear_btn = tk.Button(r_top_frame, image=clear_image, command=self.clear_btn_action)
        clear_btn.image = clear_image
        clear_btn.config(width=25, height=25)
        
        export_btn.pack(side=tk.RIGHT, padx=(0, 15))
        copy_btn.pack(side=tk.RIGHT, padx=(0,15))
        clear_btn.pack(side=tk.RIGHT,padx=(0,15))
        ToolTip(copy_btn, msg= "Copy")
        ToolTip(export_btn, msg= "Export")
        ToolTip(clear_btn, msg="Clear")
        
    def create_right_middle_frame(self, parent_frame: tk.Frame) -> None:
        r_middle_frame = tk.Frame(parent_frame)
        r_middle_frame.pack(fill=tk.X, pady=10)

        self.textbox.pack(padx=5, pady=5)
    
    def create_right_bottom_frame(self, parent_frame: tk.Frame) -> None:
        r_bottom_frame = tk.Frame(parent_frame)
        r_bottom_frame.pack(side=tk.BOTTOM)

        preview_btn = tk.Button(parent_frame, text="Preview PDF", command=self.preview_btn_action)
        generate_btn = tk.Button(parent_frame, text="Generate Tikz Code", command=self.generate_code_btn_action)

        preview_btn.pack(side=tk.RIGHT, padx=(10, 30))
        generate_btn.pack(side=tk.RIGHT)
        
    def file_new_action(self):
        print("New")
    
    def file_open_action(self) -> None:
        filetypes = (("json files", "*.json"),("All files", "*,*"))
        filepaths = fd.askopenfilenames(title="Open file",
                                        initialdir=self.current_filepath,
                                        filetypes=filetypes
        )
        var = tk.IntVar() 
        
        def on_select() -> None:
            selection = var.get()
            self.current_filepath = self.filepath_list[selection-1][0]
            print(f"-=-=-=-=-=-=--=--={selection=}")
        #TODO: error with radio count. add one file, then add more than one files including the one added earlier to get the error
        paths = list(filepaths)
        paths_tuple_list = []
        self.radio_count = len(self.filepath_list)
        for p in paths:
            self.radio_count += 1
            paths_tuple_list.append((p,self.radio_count))
        
        if paths:
            self.filepath_list.extend(paths_tuple_list)
            helper.remove_duplicates(self.filepath_list)
            
            for widget in self.left_mainframe.winfo_children():
                if "!radiobutton" in widget.winfo_name(): 
                    widget.destroy()
        
            for path, value in self.filepath_list:
                filename = self.get_filename(path)
                radio_txt = filename if len(filename) <= MAX_FILENAME_LENGTH else self.shorten_filename(filename)
                radio_btn = tk.Radiobutton(self.left_mainframe,text=radio_txt, variable=var, value=value, width=20, command=on_select)
                radio_btn.pack(pady=5)
            self.textbox.delete("1.0", tk.END) 
            self.status_label.config(text="File added")
        
        
    def file_save_action(self) -> None:
        self.current_status = "Saving..."
        filetypes = (("LaTex files", "*.tex"),
                     ("Text files", "*.txt"),
                     ("All files", "*,*"))
        export_code = self.textbox.get("1.0", tk.END)
        
        if len(export_code) > 1:
            filepath = fd.asksaveasfilename(defaultextension = filetypes[0],
                                            title="Save/Export",
                                            initialdir=os.path.join("/"),
                                            filetypes=filetypes)
            
            self.filehandler.write(filepath,export_code)
            self.status_label.config(text="File saved")
            
        else:
            messagebox.showwarning(title="Unable To Export/Save", message="Unable to perform this action. Please add an appropriate JSON file, select it and click on generate. You will then be able to perform this action")
        
    def about_menu_action(self) -> None:
        file = FileHandler()
        about = file.read(os.path.join("about.txt"))
        messagebox.showinfo("About", about)        

    def exit_application(self) -> None:
        self.root.destroy()
    
    def get_filename(self, path: str) -> str:
        i = len(path) - 1
        while i >= 0 and path[i] != "/" and path[i] != "\\":
            i -= 1
        return path[i+1:]
    
    def generate_code_btn_action(self) -> None:
        if self.current_filepath != "/":
            graph = sugiyama.draw_graph(self.current_filepath)
            generator = TikzCodeGenerator(graph)
            tikz_code = generator.generate_tikz_code()
            self.textbox.delete("1.0", tk.END) #clear textbox before generation
            self.textbox.insert(tk.END, tikz_code)

        else:
            messagebox.showinfo("JSON File Required", "Please add an appropriate JSON file and select.")
    
    def copy_btn_action(self) -> None:
        pyperclip.copy(self.textbox.get("1.0", tk.END))
        self.status_label.config(text="Copied to clipboard!")

    def clear_btn_action(self) -> None:
        if len(self.textbox.get("1.0",tk.END)) > 1:   
            self.textbox.delete("1.0", tk.END)
            self.status_label.config(text="Textbox cleared!")
        else:
            messagebox.showinfo("Nothing To Clear", "Textbox is already empty")
            
    def preview_btn_action(self) -> None:
        tikz_code = self.textbox.get("1.0", tk.END)
        if self.current_filepath != "/" and len(tikz_code) > 1:
            self.filehandler.write("tikz.tex",tikz_code)
            subprocess.run("sh run_tex.sh", shell=True)
        else:
            messagebox.showinfo("Nothing To Preview", "Please add an appropriate JSON file, select and then click on generate. You will then be able to preview the generated code.")
            
    def shorten_filename(self, filename: str) -> str:
        size = len(filename)
        if size > MAX_FILENAME_LENGTH:
            end_string = filename[size-7:]
            start_string = filename[:10]
            return start_string + "..." + end_string
        
    