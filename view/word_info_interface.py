import tkinter as tk
from tkinter import ttk

class WordInfoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.minsize(200, 200)
        self.maxsize(400, 300)
        self.attributes('-topmost', True)
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()
        
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Button-1>", self.on_click)

    def on_focus_out(self, event=None):
        if not self.focus_get():
            self.destroy()

    def on_click(self, event):
        pass
    
    def create_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.def_tab, self.def_text = self.create_tab("Definition")
        self.etym_tab, self.etym_text = self.create_tab("Etymology")
        self.examples_tab, self.examples_text = self.create_tab("Examples")
        
        self.create_button_frame()
        
        # Text styling
        for text_widget in [self.def_text, self.etym_text, self.examples_text]:
            text_widget.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
            text_widget.tag_configure("normal", font=("TkDefaultFont", 9, "normal"))
    
    def create_tab(self, name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=name)
        
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        text.config(yscrollcommand=scrollbar.set)
        
        return tab, text
    
    def create_button_frame(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        return button_frame