# Import necessary modules
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.font as tkfont
from datetime import datetime
import os

class TextEditor:
    def __init__(self, root):
        # Initialize the main text area
        self.text_area = tk.Text(root, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both')
        self.word_wrap = tk.BooleanVar(value=True)

    def new_file(self):
        # Clear the text area
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        # Open a file and insert its contents into the text area
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        # Save the current content to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def print_file(self):
        # Save the file and open it with the default print dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            os.startfile(file_path, "print")

    def undo_action(self):
        # Undo the last action
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo_action(self):
        # Redo the last undone action
        try:
            self.text_area.edit_redo()
        except:
            pass

    def cut_text(self):
        # Cut the selected text
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        # Copy the selected text
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        # Paste text from the clipboard
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        # Find and highlight specified text
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
        # Find and replace specified text
        find_query = simpledialog.askstring("Find", "Enter text to find:")
        replace_query = simpledialog.askstring("Replace", "Enter text to replace with:")
        if find_query and replace_query:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_query, replace_query)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)

    def toggle_word_wrap(self):
        # Toggle word wrap on/off
        if self.word_wrap.get():
            self.text_area.config(wrap='word')
        else:
            self.text_area.config(wrap='none')

    def choose_font(self):
        # Open a dialog to choose font family and size
        current_font = tkfont.Font(font=self.text_area['font'])
        
        font_window = tk.Toplevel(self.text_area)
        font_window.title("Choose Font")
        
        # Font family selection
        tk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
        family_var = tk.StringVar(value=current_font.actual()['family'])
        family_combo = ttk.Combobox(font_window, textvariable=family_var, values=list(tkfont.families()))
        family_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Font size selection
        tk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
        size_var = tk.IntVar(value=current_font.actual()['size'])
        size_spin = tk.Spinbox(font_window, from_=1, to=100, textvariable=size_var)
        size_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Apply the selected font
        def apply_font():
            new_font = tkfont.Font(family=family_var.get(), size=size_var.get())
            self.text_area.configure(font=new_font)
            font_window.destroy()
        
        tk.Button(font_window, text="Apply", command=apply_font).grid(row=2, column=0, columnspan=2, pady=10)

    def insert_time_date(self):
        # Insert current date and time at cursor position
        current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, current_time_date)

class StatusBar:
    def __init__(self, root, text_editor):
        # Initialize the status bar
        self.status_bar = tk.Frame(root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Left side of status bar (line and column numbers)
        self.status_bar_left = tk.Label(self.status_bar, text="Line: 1, Column: 1", anchor='w')
        self.status_bar_left.pack(side=tk.LEFT)

        # Right side of status bar (window size)
        self.status_bar_right = tk.Label(self.status_bar, text="Window Size: ", anchor='e')
        self.status_bar_right.pack(side=tk.RIGHT)

        self.root = root
        self.text_editor = text_editor

    def update(self, event=None):
        # Update status bar information
        line, column = self.text_editor.text_area.index(tk.INSERT).split('.')
        self.status_bar_left.config(text=f"Line: {line}, Column: {int(column) + 1}")
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        self.status_bar_right.config(text=f"Window Size: {window_width}x{window_height}")
        self.text_editor.text_area.edit_modified(False)

def create_menus(root, text_editor):
    # Create the main menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=text_editor.new_file, accelerator="Ctrl+N")
    file_menu.add_command(label="Open", command=text_editor.open_file, accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=text_editor.save_file, accelerator="Ctrl+S")
    file_menu.add_command(label="Print", command=text_editor.print_file, accelerator="Ctrl+P")
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Undo", command=text_editor.undo_action, accelerator="Ctrl+Z")
    edit_menu.add_command(label="Redo", command=text_editor.redo_action, accelerator="Ctrl+Y")
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", command=text_editor.cut_text, accelerator="Ctrl+X")
    edit_menu.add_command(label="Copy", command=text_editor.copy_text, accelerator="Ctrl+C")
    edit_menu.add_command(label="Paste", command=text_editor.paste_text, accelerator="Ctrl+V")
    edit_menu.add_separator()
    edit_menu.add_command(label="Find", command=text_editor.find_text, accelerator="Ctrl+F")
    edit_menu.add_command(label="Replace", command=text_editor.replace_text, accelerator="Ctrl+H")
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # Format menu
    format_menu = tk.Menu(menu_bar, tearoff=0)
    format_menu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=text_editor.word_wrap, command=text_editor.toggle_word_wrap)
    format_menu.add_command(label="Font...", command=text_editor.choose_font, accelerator="Ctrl+T")
    menu_bar.add_cascade(label="Format", menu=format_menu)

    # Insert menu
    insert_menu = tk.Menu(menu_bar, tearoff=0)
    insert_menu.add_command(label="Time/Date", command=text_editor.insert_time_date, accelerator="Ctrl+D")
    menu_bar.add_cascade(label="Insert", menu=insert_menu)

def bind_events(root, text_editor, status_bar):
    # Bind events to update status bar
    text_editor.text_area.bind('<KeyRelease>', status_bar.update)
    text_editor.text_area.bind('<ButtonRelease>', status_bar.update)
    root.bind('<Configure>', status_bar.update)

    # Bind keyboard shortcuts
    root.bind("<Control-n>", lambda event: text_editor.new_file())
    root.bind("<Control-o>", lambda event: text_editor.open_file())
    root.bind("<Control-s>", lambda event: text_editor.save_file())
    root.bind("<Control-p>", lambda event: text_editor.print_file())
    root.bind("<Control-z>", lambda event: text_editor.undo_action())
    root.bind("<Control-y>", lambda event: text_editor.redo_action())
    root.bind("<Control-x>", lambda event: text_editor.cut_text())
    root.bind("<Control-c>", lambda event: text_editor.copy_text())
    root.bind("<Control-v>", lambda event: text_editor.paste_text())
    root.bind("<Control-f>", lambda event: text_editor.find_text())
    root.bind("<Control-h>", lambda event: text_editor.replace_text())
    root.bind("<Control-t>", lambda event: text_editor.choose_font())
    root.bind("<Control-d>", lambda event: text_editor.insert_time_date())

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("My Text Editor")
    root.minsize(340, 340)

    # Initialize the text editor, status bar, menus, and event bindings
    text_editor = TextEditor(root)
    status_bar = StatusBar(root, text_editor)
    create_menus(root, text_editor)
    bind_events(root, text_editor, status_bar)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
