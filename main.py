import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from datetime import datetime
import os

class TextEditor:
    def __init__(self, root):
        self.text_area = tk.Text(root, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both')
        self.word_wrap = tk.BooleanVar(value=True)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                               filetypes=[("Text Files", "*.txt"), 
                                                          ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text Files", "*.txt"), 
                                                            ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def print_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text Files", "*.txt"), 
                                                            ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END))
            os.startfile(file_path, "print")

    def undo_action(self):
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo_action(self):
        try:
            self.text_area.edit_redo()
        except:
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
        font_choice = font.askfont(self.text_area)
        if font_choice:
            selected_font = font.Font(family=font_choice['family'], 
                                      size=font_choice['size'], 
                                      weight=font_choice['weight'], 
                                      slant=font_choice['slant'])
            self.text_area.config(font=selected_font)

    def insert_time_date(self):
        current_time_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.INSERT, current_time_date)

class StatusBar:
    def __init__(self, root, text_editor):
        self.status_bar = tk.Frame(root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar_left = tk.Label(self.status_bar, text="Line: 1, Column: 1", anchor='w')
        self.status_bar_left.pack(side=tk.LEFT)

        self.status_bar_right = tk.Label(self.status_bar, text="Window Size: ", anchor='e')
        self.status_bar_right.pack(side=tk.RIGHT)

        self.root = root
        self.text_editor = text_editor

    def update(self, event=None):
        line, column = self.text_editor.text_area.index(tk.INSERT).split('.')
        self.status_bar_left.config(text=f"Line: {line}, Column: {int(column) + 1}")
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        self.status_bar_right.config(text=f"Window Size: {window_width}x{window_height}")
        self.text_editor.text_area.edit_modified(False)  # Reset the modified flag

def create_menus(root, text_editor):
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=text_editor.new_file, accelerator="Ctrl+N")
    file_menu.add_command(label="Open", command=text_editor.open_file, accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=text_editor.save_file, accelerator="Ctrl+S")
    file_menu.add_command(label="Print", command=text_editor.print_file, accelerator="Ctrl+P")
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit Menu
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

    # Format Menu
    format_menu = tk.Menu(menu_bar, tearoff=0)
    format_menu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, 
                                variable=text_editor.word_wrap, command=text_editor.toggle_word_wrap)
    format_menu.add_command(label="Font...", command=text_editor.choose_font, accelerator="Ctrl+T")
    menu_bar.add_cascade(label="Format", menu=format_menu)

    # Insert Menu
    insert_menu = tk.Menu(menu_bar, tearoff=0)
    insert_menu.add_command(label="Time/Date", command=text_editor.insert_time_date, accelerator="Ctrl+D")
    menu_bar.add_cascade(label="Insert", menu=insert_menu)

def bind_events(root, text_editor, status_bar):
    # Bind events to update the status bar
    text_editor.text_area.bind('<KeyRelease>', status_bar.update)
    text_editor.text_area.bind('<ButtonRelease>', status_bar.update)
    root.bind('<Configure>', status_bar.update)  # Update status bar on window resize

    # Keyboard Shortcuts
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
    root = tk.Tk()
    root.title("My Text Editor")

    # Set the minimum window size
    root.minsize(340, 340)

    # Create the Text Editor
    text_editor = TextEditor(root)

    # Create the Status Bar
    status_bar = StatusBar(root, text_editor)

    # Create Menus
    create_menus(root, text_editor)
    bind_events(root, text_editor, status_bar)
    root.mainloop()

if __name__ == "__main__":
    main()