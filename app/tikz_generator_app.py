from app.tikz_generator import TikzCodeGenerator
from app import sugiyama
import tkinter as tk
from tkinter import filedialog as fd, messagebox
import os
from app.file_handler import FileHandler
import subprocess
import sys
import pyperclip
from tktooltip import ToolTip
from app import helper

MAX_FILENAME_LENGTH = 20


class TikzCodeGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry("700x580")
        self.root.title("Tikz Code Generator App")
        icon_img = tk.PhotoImage(file=os.path.join("icons/tex.png"))
        self.root.iconphoto(False, icon_img)

        self.left_mainframe = tk.Frame(self.root, padx=5, pady=5)
        self.right_mainframe = tk.Frame(self.root, padx=5, pady=5)
        self.textbox = tk.Text(self.right_mainframe, font=('TkFixedFont', 9))

        self.filehandler = FileHandler()
        self.radio_count = 0
        self.filepath_list = []
        self.current_filepath = os.path.join("/")
        self.status_label = None
        self.current_status = "status"
        self.tikz_code = ""
        self.var = tk.IntVar()

        self.create_menubar()
        self.create_left_section()
        self.create_right_section()

    def create_menubar(self) -> None:
        self.root.tk.call("tk", "windowingsystem")
        self.root.option_add("*tearOff", False)  # remove dotted lines before menu options

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Open", command=self.file_open_action)
        file_menu.add_command(label="Save/Export", command=self.file_save_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar)
        help_menu.add_command(label="Documentation", command=self.documentation_menu_action)
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
        addfile_btn.image = add_image  # add reference to image ..ref garbage collection
        addfile_btn.config(width=25, height=25)
        addfile_btn.pack(side=tk.RIGHT, padx=(0, 15))
        ToolTip(addfile_btn, msg="Add JSON file")

        remove_image = tk.PhotoImage(file=os.path.join("icons/remove-file.png"))
        remove_file_btn = tk.Button(l_tools_frame, text="Remove", image=remove_image,
                                    command=lambda: self.remove_file_btn_action(self.current_filepath))
        remove_file_btn.image = remove_image
        remove_file_btn.config(width=25, height=25)
        remove_file_btn.pack(side=tk.RIGHT, padx=(0, 15))
        ToolTip(remove_file_btn, msg="Remove JSON file")

    def create_status_bar(self, parent_frame: tk.Frame) -> None:
        l_status_frame = tk.Frame(parent_frame)
        l_status_frame.pack(side=tk.BOTTOM)
        self.status_label = tk.Label(l_status_frame, text="status")
        self.status_label.pack(side=tk.LEFT)

    def create_right_section(self) -> None:
        self.right_mainframe.pack(side=tk.LEFT, fill=tk.Y, expand=True)

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
        copy_btn.pack(side=tk.RIGHT, padx=(0, 15))
        clear_btn.pack(side=tk.RIGHT, padx=(0, 15))
        ToolTip(copy_btn, msg="Copy")
        ToolTip(export_btn, msg="Export")
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

        preview_btn.pack(side=tk.RIGHT, padx=5)
        generate_btn.pack(side=tk.RIGHT)

    def radio_btn_on_select_action(self) -> None:
        selection = self.var.get()
        self.current_filepath = self.filepath_list[selection - 1][0]

    def file_open_action(self) -> None:
        filetypes = (("json files", "*.json"), ("All files", "*,*"))
        filepaths = fd.askopenfilenames(title="Open file",
                                        initialdir=self.current_filepath,
                                        filetypes=filetypes
                                        )

        paths = list(filepaths)
        paths_tuple_list = [(p, 0) for p in paths]

        if paths:
            self.filepath_list.extend(paths_tuple_list)
            helper.remove_duplicates(self.filepath_list)
            self.set_count_for_paths()
            self.refresh_radio_btns()

            self.textbox.delete("1.0", tk.END)
            self.status_label.config(text="File added")

    def set_count_for_paths(self, ) -> None:
        self.radio_count = 1
        for i in range(len(self.filepath_list)):
            self.filepath_list[i] = self.filepath_list[i][0], self.radio_count
            self.radio_count += 1

    def refresh_radio_btns(self, ) -> None:
        for widget in self.left_mainframe.winfo_children():
            if ("!radiobutton" in widget.winfo_name() or
                    "!canvas" in widget.winfo_name() or
                    "!scrollbar" in widget.winfo_name()):
                widget.destroy()
        self.set_count_for_paths()
        listspace = tk.Canvas(self.left_mainframe, width=150)
        listspace.pack(side=tk.LEFT, expand=True, fill=tk.Y, pady=(25, 110))

        scrollbar = tk.Scrollbar(self.left_mainframe, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, pady=(25, 110), fill=tk.Y)

        for i, (path, value) in enumerate(self.filepath_list):
            filename = self.get_filename(path)
            radio_txt = filename if len(filename) <= MAX_FILENAME_LENGTH else self.shorten_filename(filename)
            radio_btn = tk.Radiobutton(self.left_mainframe, text=radio_txt, variable=self.var, value=value,
                                       command=self.radio_btn_on_select_action)

            listspace.create_window((0, i * 30), window=radio_btn, anchor=tk.NW)

        scrollbar.config(command=listspace.yview)
        listspace.config(yscrollcommand=scrollbar.set, scrollregion=listspace.bbox("all"))

    def file_save_action(self) -> None:
        self.current_status = "Saving..."
        filetypes = (("LaTex files", "*.tex"),
                     ("Text files", "*.txt"),
                     ("All files", "*,*"))
        export_code = self.textbox.get("1.0", tk.END)

        if len(export_code) > 1:
            filepath = fd.asksaveasfilename(defaultextension=filetypes[0],
                                            title="Save/Export",
                                            initialdir=os.path.join("/"),
                                            filetypes=filetypes)

            self.filehandler.write(filepath, export_code)
            self.status_label.config(text="File saved")

        else:
            messagebox.showwarning(title="Unable To Export/Save",
                                   message="Unable to perform this action. Please add an appropriate JSON file, "
                                           "select it and click on generate. You will then be able to perform this "
                                           "action")

    def remove_file_btn_action(self, current_file: str) -> None:
        if current_file == "/" or len(self.filepath_list) == 0:
            messagebox.showerror("Nothing To Delete",
                                 "You have not selected a file. Please make sure a file is imported and selected to "
                                 "be able to delete")
        else:
            current_tuple = None
            for path, pos in self.filepath_list:
                if path == current_file:
                    current_tuple = (path, pos)
                    break

            self.filepath_list.remove(current_tuple)
            self.current_filepath = os.path.join("/")
            self.textbox.delete("1.0", tk.END)
            self.refresh_radio_btns()
            self.status_label.config(text="File removed")

    def about_menu_action(self) -> None:
        about = self.filehandler.read(os.path.join("about.txt"))
        messagebox.showinfo("About", about)

    def documentation_menu_action(self) -> None:
        documentation = self.filehandler.read(os.path.join("documentation.txt"))
        messagebox.showinfo("Documentation", documentation)

    def exit_application(self) -> None:
        self.root.destroy()

    def get_filename(self, path: str) -> str:
        '''
        Extract the filename from a given path.
        Args:
            path (str) -- The path containing the filename.
        Returns:
            str -- The extracted filename.
        '''
        return os.path.basename(path)

    def generate_code_btn_action(self) -> None:
        if self.current_filepath != "/":
            try:
                graph = sugiyama.draw_graph(self.current_filepath)
                generator = TikzCodeGenerator(graph)
                tikz_code = generator.generate_tikz_code()
                self.textbox.delete("1.0", tk.END)  # clear textbox before generation
                self.textbox.insert(tk.END, tikz_code)
            except AttributeError:
                messagebox.showerror("Error (Invalid JSON)", message="JSON does not match the specification. Please "
                                                                     "add a valid JSON file")
            except Exception as e:
                messagebox.showerror("Error (Oops!)", message="Something went wrong while generating the code. ")
                print(f"Error: unable to generate code -> {e}")

        else:
            messagebox.showinfo("JSON File Required", "Please add an appropriate JSON file and select.")

    def copy_btn_action(self) -> None:
        pyperclip.copy(self.textbox.get("1.0", tk.END))
        self.status_label.config(text="Copied to clipboard!")

    def clear_btn_action(self) -> None:
        if len(self.textbox.get("1.0", tk.END)) > 1:
            self.textbox.delete("1.0", tk.END)
            self.status_label.config(text="Textbox cleared!")
        else:
            messagebox.showinfo("Nothing To Clear", "Textbox is already empty")

    def preview_btn_action(self) -> None:
        tikz_code = self.textbox.get("1.0", tk.END)
        if self.current_filepath != "/" and len(tikz_code) > 1:
            self.filehandler.write("tikz.tex", tikz_code)
            subprocess.run("sh run_tex.sh", shell=True)
            #check if last output file exist
            path_exist = os.path.exists("lastln_output.txt")
            last_ln_output = self.filehandler.read(os.path.join("lastln_output.txt")) if path_exist else None
            if last_ln_output:
                messagebox.showerror("Compilation Error",
                                     "An error occurred while compiling the generated Tikz code. This may be due to "
                                     "an incorrect value mapped to key. Please check your JSON input and try again or "
                                     "correct the generated code in the text area.")
                os.remove(os.path.join("lastln_output.txt"))
        else:
            messagebox.showinfo("Nothing To Preview",
                                "Please add an appropriate JSON file, select and then click on generate. You will "
                                "then be able to preview the generated code.")

    def shorten_filename(self, filename: str) -> str:
        size = len(filename)
        if size > MAX_FILENAME_LENGTH:
            end_string = filename[size - 7:]
            start_string = filename[:10]
            return start_string + "..." + end_string
