import tkinter as tk
from tkinter import StringVar, ttk
from GUI.common.app_theme import IconManager, AppTheme, ToolTip
from GUI.tabs.dictionary.dict_view import DictionaryView
from GUI.tabs.reading.reading_view import ReadingView
from GUI.tabs.vocabulary.vocabulary_view import VocabularyView
from GUI.tabs.explorer.explorer_view import ExplorerView
from GUI.tabs.dashboard.dashboard_view import DashboardView


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pymage - Language Learning Assistant")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        AppTheme.configure_styles()
        
        self.icon_manager = IconManager()
        
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Controls
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        self.native_language_var = StringVar(self)
        self.translated_language_var = StringVar(self)
        self.search_var = StringVar(self)
        self.search_var.trace("w", self._on_search_changed)
        
        self._create_header()
        self._create_language_dropdowns()
        self._create_buttons()
        self._create_notebook()
        
        self._create_status_bar()
        
    def _create_header(self):
        header = ttk.Frame(self, style='Header.TFrame')
        header.grid(row=0, column=0, sticky="ew")
        header.configure(height=50)
        
        logo_frame = ttk.Frame(header, style='Header.TFrame')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        app_name = ttk.Label(logo_frame, text="Pymage", style='Header.TLabel', font=("Segoe UI", 16, "bold"))
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
        
        native_frame = ttk.Frame(dropdown_frame)
        native_frame.pack(side=tk.LEFT, padx=20, pady=10)
        native_label = ttk.Label(native_frame, text="Native Language:")
        native_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.native_dropdown = ttk.Combobox(native_frame, textvariable=self.native_language_var, state="readonly", width=15)
        self.native_dropdown.pack(side=tk.TOP, pady=5)
        
        translated_frame = ttk.Frame(dropdown_frame)
        translated_frame.pack(side=tk.LEFT, padx=20, pady=10)
        translated_label = ttk.Label(translated_frame, text="Learning Language:")
        translated_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.translated_dropdown = ttk.Combobox(translated_frame, textvariable=self.translated_language_var, state="readonly", width=15)
        self.translated_dropdown.pack(side=tk.TOP, pady=5)
        
        search_frame = ttk.Frame(dropdown_frame)
        search_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.TOP, anchor=tk.W)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.TOP, pady=5, fill=tk.X)
        
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
        ToolTip(start_selection_button, "Capture text from screen (Ctrl+E)")
        
        separator = ttk.Separator(toolbar, orient="vertical")
        separator.pack(side=tk.LEFT, padx=10, fill="y")
        
        save_word_button = ttk.Button(toolbar, text="Save Word")
        save_word_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(save_word_button, "Save selected word (Ctrl+S)")
        
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
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # 1. Dictionary & Lookup Tab
        self.dictionary_tab = DictionaryView(self.notebook)
        self.notebook.add(self.dictionary_tab, text="Dictionary")
        
        # 2. Reading Assistant Tab
        self.reading_tab = ReadingView(self.notebook)
        self.notebook.add(self.reading_tab, text="Reading Assistant")
        
        # 3. Vocabulary Builder Tab
        self.vocabulary_tab = VocabularyView(self.notebook)
        self.notebook.add(self.vocabulary_tab, text="Vocabulary Builder")
        
        # 4. Word Explorer Tab
        self.explorer_tab = ExplorerView(self.notebook)
        self.notebook.add(self.explorer_tab, text="Word Explorer")
        
        # 5. Study Dashboard Tab
        self.dashboard_tab = DashboardView(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Study Dashboard")
    
    def _create_status_bar(self):
        """Create status bar at the bottom of the window"""
        status_frame = ttk.Frame(self, relief="sunken", style='TFrame')
        status_frame.grid(row=3, column=0, sticky="ew")
        
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W, padding=(5, 2))
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        version_label = ttk.Label(status_frame, text="v0.1.0", padding=(5, 2))
        version_label.pack(side=tk.RIGHT)
    
    def set_language_options(self, languages, native_default, translated_default):
        """Set language dropdown options"""
        self.native_language_var.set(native_default)
        self.translated_language_var.set(translated_default)
        
        self.native_dropdown['values'] = languages
        self.translated_dropdown['values'] = languages
    
    def create_buttons(self, commands):
        """Set button commands"""
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
    
    def _on_search_changed(self, *args):
        """Handle changes to the global search field"""
        search_text = self.search_var.get()
        if len(search_text) >= 3:
            self.show_status(f"Searching for: {search_text}")
    
    def show_status(self, message):
        """Updates message in the status bar"""
        self.status_label.config(text=message)