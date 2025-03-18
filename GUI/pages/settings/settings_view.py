import tkinter as tk
from tkinter import ttk, messagebox

class SettingsInterface(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = None
        
        self.title("Settings")
        self.geometry("400x300")
        self.minsize(300, 200)
        
        self._create_notebook()
        self._create_buttons()
        
        self._initialize_variables()
        
    def _create_notebook(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")

        self.appearance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.appearance_tab, text="Appearance")
        
        self.hotkeys_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.hotkeys_tab, text="Hotkeys")
    
    def _create_buttons(self):
        """Create button area"""
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.save_button = tk.Button(button_frame, text="Save Settings")
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_button = tk.Button(button_frame, text="Cancel")
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _initialize_variables(self):
        """Initialize UI variables"""
        self.source_language = tk.StringVar()
        self.target_language = tk.StringVar()
        
        self.theme_var = tk.StringVar(value="Light")
        self.font_size = tk.StringVar(value="12")
        
        self.selection_hotkey = tk.StringVar(value="Ctrl+E")
        self.save_hotkey = tk.StringVar(value="Ctrl+S")
    
    def set_controller(self, controller):
        self.controller = controller
        
        self.create_general_settings()
        self.create_appearance_settings()
        self.create_hotkey_settings()
        
        self.save_button.config(command=self._on_save)
        self.cancel_button.config(command=self._on_cancel)
        
        self._load_settings()
    
    def _load_settings(self):
        """Load current settings from controller"""
        if self.controller:
            settings = self.controller.get_settings()
            
            self.source_language.set(settings.get('source_language', 'English'))
            self.target_language.set(settings.get('target_language', 'English'))
            self.theme_var.set(settings.get('theme', 'Light'))
            self.font_size.set(settings.get('font_size', '12'))
            self.selection_hotkey.set(settings.get('selection_hotkey', 'Ctrl+E'))
            self.save_hotkey.set(settings.get('save_hotkey', 'Ctrl+S'))
    
    def _on_save(self):
        if self.controller:
            settings = {
                'source_language': self.source_language.get(),
                'target_language': self.target_language.get(),
                'theme': self.theme_var.get(),
                'font_size': self.font_size.get(),
                'selection_hotkey': self.selection_hotkey.get(),
                'save_hotkey': self.save_hotkey.get()
            }
            
            self.controller.save_settings(settings)
    
    def _on_cancel(self):
        if self.controller:
            self.controller.cancel()
    
    def create_general_settings(self):
        frame = ttk.LabelFrame(self.general_tab, text="Default Languages")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(frame, text="Default Source Language:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        source_combo = ttk.Combobox(frame, textvariable=self.source_language)
        source_combo['values'] = ["English", "Spanish", "French", "German"]
        source_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Default Target Language:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        target_combo = ttk.Combobox(frame, textvariable=self.target_language)
        target_combo['values'] = ["English", "Spanish", "French", "German"]
        target_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
    def create_appearance_settings(self):
        frame = ttk.LabelFrame(self.appearance_tab, text="Theme")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Radiobutton(frame, text="Light Theme", variable=self.theme_var, value="Light").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Radiobutton(frame, text="Dark Theme", variable=self.theme_var, value="Dark").pack(anchor=tk.W, padx=10, pady=5)
        
        font_frame = ttk.LabelFrame(self.appearance_tab, text="Font Settings")
        font_frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT, padx=5, pady=5)
        size_combo = ttk.Combobox(font_frame, textvariable=self.font_size, width=5)
        size_combo['values'] = ["10", "12", "14", "16", "18"]
        size_combo.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_hotkey_settings(self):
        frame = ttk.LabelFrame(self.hotkeys_tab, text="Keyboard Shortcuts")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(frame, text="Screen Selection:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        selection_entry = ttk.Entry(frame, textvariable=self.selection_hotkey, width=10)
        selection_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Save Word:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        save_entry = ttk.Entry(frame, textvariable=self.save_hotkey, width=10)
        save_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
    def show_message(self, title, message):
        messagebox.showinfo(title, message)