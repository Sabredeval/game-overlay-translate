from tkinter import ttk
import os
import tkinter as tk
from PIL import ImageTk, Image

class AppTheme:
    """Application theme colors constants and fonts"""
    PRIMARY = "#1976D2"        # Primary blue
    PRIMARY_DARK = "#0D47A1"   # Darker blue for hover states
    ACCENT = "#FF5722"         # Orange accent for highlights
    BG_DARK = "#263238"        # Dark background
    BG_LIGHT = "#ECEFF1"       # Light background
    TEXT_DARK = "#263238"      # Dark text
    TEXT_LIGHT = "#FFFFFF"     # White text
    BORDER = "#B0BEC5"         # Light gray border
    
    HEADING_FONT = ("Segoe UI", 12, "bold")
    BODY_FONT = ("Segoe UI", 10)
    SMALL_FONT = ("Segoe UI", 9)
    
    @classmethod
    def configure_styles(cls):
        style = ttk.Style()
        
        try:
            style.theme_use('alt') 
        except:
            pass 
        
        style.configure('TFrame', background=cls.BG_LIGHT)
        style.configure('TLabel', background=cls.BG_LIGHT, foreground=cls.TEXT_DARK, font=cls.BODY_FONT)
        style.configure('TButton', foreground=cls.TEXT_LIGHT, background=cls.PRIMARY, 
                        font=cls.BODY_FONT, padding=(10, 5))
        style.map('TButton',
                  background=[('active', cls.PRIMARY_DARK), ('pressed', cls.PRIMARY_DARK)],
                  foreground=[('active', cls.TEXT_LIGHT), ('pressed', cls.TEXT_LIGHT)])
        
        style.configure('Header.TLabel', font=cls.HEADING_FONT, background=cls.PRIMARY, foreground=cls.TEXT_LIGHT)
        style.configure('Accent.TButton', background=cls.ACCENT)
        style.map('Accent.TButton', 
                  background=[('active', '#E64A19'), ('pressed', '#BF360C')])
        
        style.configure('TCombobox', foreground=cls.TEXT_DARK, background=cls.BG_LIGHT)
        style.map('TCombobox', fieldbackground=[('readonly', cls.BG_LIGHT)])
        
        style.configure('TNotebook', background=cls.BG_LIGHT, borderwidth=0)
        style.configure('TNotebook.Tab', background=cls.BG_LIGHT, foreground=cls.TEXT_DARK,
                       padding=(10, 5), font=cls.BODY_FONT)
        style.map('TNotebook.Tab',
                 background=[('selected', cls.PRIMARY)],
                 foreground=[('selected', cls.TEXT_LIGHT)])
        
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)
    
    def show(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(tw, text=self.text, background=AppTheme.PRIMARY_DARK, 
                        foreground=AppTheme.TEXT_LIGHT, relief="solid", borderwidth=1,
                        font=AppTheme.SMALL_FONT, padding=(5, 3))
        label.pack()
    
    def hide(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class IconManager:
    def __init__(self):
        self.icons = {}
        self._load_icons()
    
    def _load_icons(self):
        icon_dir = os.path.join(os.path.dirname(__file__), "..", "resources", "icons")
        os.makedirs(icon_dir, exist_ok=True)
        
        # TODO - Load actual icons from files
        icon_definitions = {
            "saved_words": "\uf02d",  # Book icon
            "browse": "\uf002",       # Search icon
            "settings": "\uf013",     # Gear icon
            "selection": "\uf065",    # Expand icon
            "save": "\uf0c7",         # Save icon
            "language": "\uf1ab",     # Language icon
            "logo": None              # Custom logo
        }
        
        for name, symbol in icon_definitions.items():
            img = Image.new('RGBA', (24, 24), AppTheme.PRIMARY)
            self.icons[name] = ImageTk.PhotoImage(img)
    
    def get(self, name):
        return self.icons.get(name)