import tkinter as tk
from tkinter import ttk, messagebox

class SettingsInterface(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("Settings")
        self.geometry("400x300")
        self.minsize(300, 200)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")
        self.create_general_settings()
        
        # Appearance tab
        self.appearance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.appearance_tab, text="Appearance")
        self.create_appearance_settings()
        
        # Hotkeys tab
        self.hotkeys_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.hotkeys_tab, text="Hotkeys")
        self.create_hotkey_settings()
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_button = tk.Button(button_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def create_general_settings(self):
        # Example settings
        frame = ttk.LabelFrame(self.general_tab, text="Default Languages")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(frame, text="Default Source Language:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.source_language = tk.StringVar(value=self.parent.native_language_var.get())
        source_combo = ttk.Combobox(frame, textvariable=self.source_language)
        source_combo['values'] = ["English", "Spanish", "French", "German"]
        source_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Default Target Language:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_language = tk.StringVar(value=self.parent.translated_language_var.get())
        target_combo = ttk.Combobox(frame, textvariable=self.target_language)
        target_combo['values'] = ["English", "Spanish", "French", "German"]
        target_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
    def create_appearance_settings(self):
        # Example theme settings
        frame = ttk.LabelFrame(self.appearance_tab, text="Theme")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        self.theme_var = tk.StringVar(value="Light")
        ttk.Radiobutton(frame, text="Light Theme", variable=self.theme_var, value="Light").pack(anchor=tk.W, padx=10, pady=5)
        ttk.Radiobutton(frame, text="Dark Theme", variable=self.theme_var, value="Dark").pack(anchor=tk.W, padx=10, pady=5)
        
        # Font settings
        font_frame = ttk.LabelFrame(self.appearance_tab, text="Font Settings")
        font_frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT, padx=5, pady=5)
        self.font_size = tk.StringVar(value="12")
        size_combo = ttk.Combobox(font_frame, textvariable=self.font_size, width=5)
        size_combo['values'] = ["10", "12", "14", "16", "18"]
        size_combo.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_hotkey_settings(self):
        frame = ttk.LabelFrame(self.hotkeys_tab, text="Keyboard Shortcuts")
        frame.pack(fill=tk.X, padx=10, pady=10, anchor=tk.N)
        
        ttk.Label(frame, text="Screen Selection:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.selection_hotkey = tk.StringVar(value="Ctrl+E")
        selection_entry = ttk.Entry(frame, textvariable=self.selection_hotkey, width=10)
        selection_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame, text="Save Word:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.save_hotkey = tk.StringVar(value="Ctrl+S")
        save_entry = ttk.Entry(frame, textvariable=self.save_hotkey, width=10)
        save_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Note: Actual hotkey handling would need more work
    
    def save_settings(self):
        # Update parent's language settings
        self.parent.native_language_var.set(self.source_language.get())
        self.parent.translated_language_var.set(self.target_language.get())
        
        # Other settings would be saved here
        # For now, just show a confirmation
        messagebox.showinfo("Settings Saved", "Your settings have been saved.")
        self.destroy()