import tkinter as tk
from tkinter import Text, StringVar, ttk
from view.app_theme import IconManager, AppTheme, ToolTip


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pymage - Main Interface")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Apply theme
        AppTheme.configure_styles()
        
        # Load icons
        self.icon_manager = IconManager()
        
        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Controls
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize widgets
        self.native_language_var = StringVar(self)
        self.translated_language_var = StringVar(self)
        self.native_text_widget = None
        self.translated_text_widget = None
        
        # Create components
        self._create_header()
        self._create_language_dropdowns()
        self._create_buttons()
        self._create_notebook()
        
        # Add status bar
        self._create_status_bar()
        
    def _create_header(self):
        """Create application header"""
        header = ttk.Frame(self, style='Header.TFrame')
        header.grid(row=0, column=0, sticky="ew")
        header.configure(height=50)
        
        # Logo/app name
        logo_frame = ttk.Frame(header, style='Header.TFrame')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        app_name = ttk.Label(logo_frame, text="Pylla", style='Header.TLabel', font=("Segoe UI", 16, "bold"))
        app_name.pack(side=tk.LEFT)
        
        app_subtitle = ttk.Label(logo_frame, text="Language Learning Assistant", 
                               style='Header.TLabel', font=("Segoe UI", 10))
        app_subtitle.pack(side=tk.LEFT, padx=10)
        
    def _create_language_dropdowns(self):
        """Create language selection area"""
        dropdown_container = ttk.Frame(self)
        dropdown_container.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        
        dropdown_frame = ttk.LabelFrame(dropdown_container, text="Language Selection")
        dropdown_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Native language selection
        native_frame = ttk.Frame(dropdown_frame)
        native_frame.pack(side=tk.LEFT, padx=20, pady=10)
        native_label = ttk.Label(native_frame, text="Native Language:")
        native_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.native_dropdown = ttk.Combobox(native_frame, textvariable=self.native_language_var, state="readonly", width=15)
        self.native_dropdown.pack(side=tk.TOP, pady=5)
        
        # Translated language selection
        translated_frame = ttk.Frame(dropdown_frame)
        translated_frame.pack(side=tk.LEFT, padx=20, pady=10)
        translated_label = ttk.Label(translated_frame, text="Translation Language:")
        translated_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.translated_dropdown = ttk.Combobox(translated_frame, textvariable=self.translated_language_var, state="readonly", width=15)
        self.translated_dropdown.pack(side=tk.TOP, pady=5)
        
        return dropdown_frame
        
    def _create_buttons(self):
        button_container = ttk.Frame(self)
        button_container.grid(row=1, column=0, pady=0, padx=10, sticky="ew")
        
        button_frame = ttk.LabelFrame(button_container, text="Tools")
        button_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        toolbar = ttk.Frame(button_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        start_selection_button = ttk.Button(toolbar, text="Select Text", style="Accent.TButton")
        start_selection_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(start_selection_button, "Start text selection tool (Ctrl+E)")
        
        save_word_button = ttk.Button(toolbar, text="Save Word")
        save_word_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(save_word_button, "Save selected word (Ctrl+S)")
        
        separator = ttk.Separator(toolbar, orient="vertical")
        separator.pack(side=tk.LEFT, padx=10, fill="y")
        
        saved_words_button = ttk.Button(toolbar, text="Saved Words")
        saved_words_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(saved_words_button, "View saved words")
        
        browse_words_button = ttk.Button(toolbar, text="Browse Words")
        browse_words_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(browse_words_button, "Browse dictionary")
        
        settings_button = ttk.Button(toolbar, text="Settings")
        settings_button.pack(side=tk.RIGHT, padx=5, pady=5)
        ToolTip(settings_button, "Application settings")
        
        return button_frame
    
    def _create_notebook(self):
        """Create tabbed interface for content"""
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        translation_tab = ttk.Frame(self.notebook)
        self.notebook.add(translation_tab, text="Translation")
        
        translation_tab.grid_rowconfigure(0, weight=1)
        translation_tab.grid_rowconfigure(1, weight=1)
        translation_tab.grid_columnconfigure(0, weight=1)
        
        self._create_text_areas(translation_tab)
        
        # To be expanded in future
        dictionary_tab = ttk.Frame(self.notebook)
        self.notebook.add(dictionary_tab, text="Dictionary")
        
        dict_placeholder = ttk.Label(dictionary_tab, text="Dictionary functionality coming soon!")
        dict_placeholder.pack(expand=True, pady=50)
    
    def _create_text_areas(self, parent):
        native_text_frame = ttk.LabelFrame(parent, text="Native Text")
        native_text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        native_container = ttk.Frame(native_text_frame)
        native_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.native_text_widget = Text(
            native_container, 
            wrap=tk.WORD, 
            font=AppTheme.BODY_FONT,
            background="white",
            foreground=AppTheme.TEXT_DARK,
            insertbackground=AppTheme.PRIMARY,
            relief="flat",
            borderwidth=0,
            padx=5,
            pady=5
        )
        self.native_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        native_scrollbar = ttk.Scrollbar(native_container, orient="vertical", command=self.native_text_widget.yview)
        native_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.native_text_widget.config(yscrollcommand=native_scrollbar.set)
        
        translated_text_frame = ttk.LabelFrame(parent, text="Translation")
        translated_text_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        translated_container = ttk.Frame(translated_text_frame)
        translated_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.translated_text_widget = Text(
            translated_container, 
            wrap=tk.WORD, 
            font=AppTheme.BODY_FONT,
            background=AppTheme.BG_LIGHT,
            foreground=AppTheme.TEXT_DARK,
            relief="flat",
            borderwidth=0,
            padx=5,
            pady=5,
            state=tk.DISABLED
        )
        self.translated_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        translated_scrollbar = ttk.Scrollbar(translated_container, orient="vertical", command=self.translated_text_widget.yview)
        translated_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.translated_text_widget.config(yscrollcommand=translated_scrollbar.set)
    
    def _create_status_bar(self):
        # To be extended in future
        status_frame = ttk.Frame(self, relief="sunken", style='TFrame')
        status_frame.grid(row=3, column=0, sticky="ew")
        
        status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W, padding=(5, 2))
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        version_label = ttk.Label(status_frame, text="v0.0.1", padding=(5, 2))
        version_label.pack(side=tk.RIGHT)
    
    def set_language_options(self, languages, native_default, translated_default):
        self.native_language_var.set(native_default)
        self.translated_language_var.set(translated_default)
        
        self.native_dropdown['values'] = languages
        self.translated_dropdown['values'] = languages
    
    def create_buttons(self, commands):
        button_container = self.grid_slaves(row=1, column=0)[0]
        button_frame = button_container.winfo_children()[0]
        toolbar = button_frame.winfo_children()[0]
        
        buttons = [b for b in toolbar.winfo_children() if isinstance(b, ttk.Button)]
        
        # Order: Select Text, Save Word, [separator], Saved Words, Browse Words, Settings
        buttons[0].config(command=commands["start_selection"])
        buttons[1].config(command=commands["save_word"])
        buttons[2].config(command=commands["saved_words"])
        buttons[3].config(command=commands["browse_words"])
        buttons[4].config(command=commands["settings"])


if __name__ == "__main__":
    app = MainView()
    app.set_language_options(["English", "Spanish", "French", "German"], "English", "Spanish")
    app.create_buttons({
        "saved_words": lambda: print("Saved Words"),
        "browse_words": lambda: print("Browse Words"),
        "settings": lambda: print("Settings"),
        "start_selection": lambda: print("Start Selection"),
        "save_word": lambda: print("Save Word")
    })
    app.mainloop()