import tkinter as tk
from tkinter import ttk
from GUI.common.app_theme import AppTheme

class WordInfoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("Word Information")
        self.geometry("550x400")
        self.minsize(400, 300)
        self.configure(bg=AppTheme.BG_LIGHT)
        
        self.attributes('-topmost', True)
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Clean up on window close"""
        self.grab_release()
        self.destroy()
    
    def create_ui(self):
        """Create the main UI components"""
        # Create header with word
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Content area for the WordDisplay component
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Button frame at bottom
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=15, pady=15)