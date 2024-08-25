import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.font as tkfont
from datetime import datetime
import os
import importlib.util

class TextEditor:
    def __init__(self, root):
        self.text_area = tk.Text(root, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both')
        self.word_wrap = tk.BooleanVar(value=True)
        self.loaded_modules = {}

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def print_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            os.startfile(file_path, "print")

    def undo_action(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo_action(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        search_query = simpledialog.askstring("Find", "Enter text to find:")
        if search_query:
            start_pos = self.text_area.search(search_query, 1.0, stopindex=tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(search_query)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                self.text_area.tag_config("highlight", background="yellow")
                self.text_area.mark_set(tk.INSERT, end_pos)
                self.text_area.see(tk.INSERT)
            else:
                messagebox.showinfo("Find", "Text not found")

    def replace_text(self):
        find_query = simpledialog.askstring("Find", "Enter text to find:")
        replace_query = simpledialog.askstring("Replace", "Enter text to replace with:")
        if find_query and replace_query:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_query, replace_query)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)

    def toggle_word_wrap(self):
        if self.word_wrap.get():
            self.text_area.config(wrap='word')
        else:
            self.text_area.config(wrap='none')

    def choose_font(self):
        current_font = tkfont.Font(font=self.text_area['font'])
        
        font_window = tk.Toplevel(self.text_area)
        font_window.title("Choose Font")
        
        tk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
        family_var = tk.StringVar(value=current_font.actual()['family'])
        family_combo = ttk.Combobox(font_window, textvariable=family_var, values=list(tkfont.families()))
        family_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
        size_var = tk.IntVar(value=current_font.actual()['size'])
        size_spin = tk.Spinbox(font_window, from_=1, to=100, textvariable=size_var)
        size_spin.grid(row=1, column=1, padx=5, pady=5)
        
        def apply_font():
            new_font = tkfont.Font(family=family_var.get(), size=size_var.get())
            self.text_area.configure(font=new_font)
            font_window.destroy()
        
        tk.Button(font_window, text="Apply", command=apply_font).grid(row=2, column=0, columnspan=2, pady=10)

    def insert_time_date(self):
        current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, current_time_date)

    def load_module(self):
        module_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if module_path:
            try:
                spec = importlib.util.spec_from_file_location("module", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for any class that has the required methods
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and hasattr(obj, 'process') and hasattr(obj, 'get_name') and hasattr(obj, 'get_description'):
                        processor = obj()
                        self.loaded_modules[processor.get_name()] = processor
                        messagebox.showinfo("Module Loaded", f"Module '{processor.get_name()}' loaded successfully!")
                        return
                
                raise AttributeError("Module does not contain a valid processor class")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load module: {str(e)}")

    def manage_modules(self):
        manage_window = tk.Toplevel(self.text_area)
        manage_window.title("Manage Modules")
        manage_window.geometry("300x200")

        listbox = tk.Listbox(manage_window)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for module_name in self.loaded_modules.keys():
            listbox.insert(tk.END, module_name)

        def apply_module():
            selection = listbox.curselection()
            if selection:
                module_name = listbox.get(selection[0])
                module = self.loaded_modules[module_name]
                text = self.text_area.get(1.0, tk.END)
                processed_text = module.process(text)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, processed_text)
                manage_window.destroy()

        apply_button = tk.Button(manage_window, text="Apply", command=apply_module)
        apply_button.pack(pady=10)

    def apply_last_module(self):
        if not self.loaded_modules:
            messagebox.showinfo("No Modules", "No modules have been loaded. Please load a module first.")
            return
        
        last_module_name = list(self.loaded_modules.keys())[-1]
        module = self.loaded_modules[last_module_name]
        text = self.text_area.get(1.0, tk.END)
        processed_text = module.process(text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, processed_text)
        messagebox.showinfo("Module Applied", f"Applied module: {last_module_name}")