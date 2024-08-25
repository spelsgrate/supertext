import tkinter as tk

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
        self.text_editor.text_area.edit_modified(False)