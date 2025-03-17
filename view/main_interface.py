import tkinter as tk
from tkinter import Label, Text, Scrollbar, Button, OptionMenu, StringVar


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pymage - Main Interface")
        self.geometry("800x600")
        
        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize widgets
        self.native_language_var = StringVar(self)
        self.translated_language_var = StringVar(self)
        self.native_text_widget = None
        self.translated_text_widget = None
        
        # Create components
        self._create_language_dropdowns()
        self._create_buttons()
        self._create_text_areas()
    
    def _create_language_dropdowns(self):
        dropdown_frame = tk.Frame(self)
        dropdown_frame.grid(row=0, column=0, pady=10, sticky="ew")
        
        return dropdown_frame
    
    def _create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")
        
        return button_frame
    
    def _create_text_areas(self):
        # Native language text
        native_text_frame = tk.Frame(self)
        native_text_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        native_label = Label(native_text_frame, text="Native Text:")
        native_label.pack(anchor=tk.W)
        
        native_scrollbar = Scrollbar(native_text_frame)
        native_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.native_text_widget = Text(native_text_frame, wrap=tk.WORD, yscrollcommand=native_scrollbar.set)
        self.native_text_widget.pack(fill=tk.BOTH, expand=True)
        
        native_scrollbar.config(command=self.native_text_widget.yview)
        
        # Translated language text
        translated_text_frame = tk.Frame(self)
        translated_text_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        translated_label = Label(translated_text_frame, text="Translated Text:")
        translated_label.pack(anchor=tk.W)
        
        translated_scrollbar = Scrollbar(translated_text_frame)
        translated_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.translated_text_widget = Text(translated_text_frame, wrap=tk.WORD, yscrollcommand=translated_scrollbar.set)
        self.translated_text_widget.config(state=tk.DISABLED)
        self.translated_text_widget.pack(fill=tk.BOTH, expand=True)
        
        translated_scrollbar.config(command=self.translated_text_widget.yview)
    
    def set_language_options(self, languages, native_default, translated_default):
        self.native_language_var.set(native_default)
        self.translated_language_var.set(translated_default)
        
        dropdown_frame = self.winfo_children()[0]
        
        native_language_dropdown = OptionMenu(dropdown_frame, self.native_language_var, *languages)
        native_language_dropdown.pack(side=tk.LEFT, padx=10)
        
        translated_language_dropdown = OptionMenu(dropdown_frame, self.translated_language_var, *languages)
        translated_language_dropdown.pack(side=tk.LEFT, padx=10)
    
    def create_buttons(self, commands):
        button_frame = self.winfo_children()[1]
        
        saved_words_button = Button(button_frame, text="Saved Words", command=commands["saved_words"])
        saved_words_button.pack(side=tk.LEFT, padx=10)
        
        browse_words_button = Button(button_frame, text="Browse Words", command=commands["browse_words"])
        browse_words_button.pack(side=tk.LEFT, padx=10)
        
        settings_button = Button(button_frame, text="Settings", command=commands["settings"])
        settings_button.pack(side=tk.LEFT, padx=10)
        
        start_selection_button = Button(button_frame, text="Start Selection", command=commands["start_selection"])
        start_selection_button.pack(side=tk.LEFT, padx=10)
        
        save_word_button = Button(button_frame, text="Save Word", command=commands["save_word"])
        save_word_button.pack(side=tk.LEFT, padx=10)
