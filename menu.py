import tkinter as tk

def create_menus(root, text_editor):
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
    format_menu.add_checkbutton(label="Word Wrap", variable=text_editor.word_wrap, command=text_editor.toggle_word_wrap)
    format_menu.add_command(label="Font...", command=text_editor.choose_font, accelerator="Ctrl+T")
    menu_bar.add_cascade(label="Format", menu=format_menu)

    # Insert menu
    insert_menu = tk.Menu(menu_bar, tearoff=0)
    insert_menu.add_command(label="Time/Date", command=text_editor.insert_time_date, accelerator="Ctrl+D")
    menu_bar.add_cascade(label="Insert", menu=insert_menu)

    # Modules menu
    modules_menu = tk.Menu(menu_bar, tearoff=0)
    modules_menu.add_command(label="Load Module", command=text_editor.load_module)
    modules_menu.add_command(label="Manage Modules", command=text_editor.manage_modules)
    modules_menu.add_command(label="Apply Last Module", command=text_editor.apply_last_module)
    menu_bar.add_cascade(label="Modules", menu=modules_menu)