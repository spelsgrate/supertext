import tkinter as tk
from text_editor import TextEditor
from status_bar import StatusBar
from menu import create_menus
from event_bindings import bind_events

def main():
    root = tk.Tk()
    root.title("My Text Editor")
    root.minsize(340, 340)

    text_editor = TextEditor(root)
    status_bar = StatusBar(root, text_editor)
    create_menus(root, text_editor)
    bind_events(root, text_editor, status_bar)

    root.mainloop()

if __name__ == "__main__":
    main()