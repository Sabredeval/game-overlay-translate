from pystray import Icon, Menu, MenuItem
from PIL import Image
import tkinter as tk
import keyboard
import time
import threading

class TrayIconHandler:
    """This class allows to restore the application window after closing it by putting it in the windows tray."""
    def __init__(self, app_name, icon_path, on_restore, on_exit):
        self.app_name = app_name
        self.icon_path = icon_path
        self.on_restore = on_restore
        self.on_exit = on_exit
        self.icon = None
        
    def create_icon(self):
        icon_image = Image.open(self.icon_path)
        
        menu = Menu(
            MenuItem("Restore", self.on_restore),
            MenuItem("Exit", self.on_exit)
        )
        
        self.icon = Icon(self.app_name, icon_image, self.app_name, menu)
        
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def stop(self):
        if self.icon:
            self.icon.stop()
            self.icon = None

class ClipboardHandler:
    """This class is used to interact with the clipboard."""
    def __init__(self, root):
        self.root = root
    
    def get_clipboard_text(self):
        try:
            return self.root.clipboard_get().strip()
        except Exception as e:
            print(f"Error getting clipboard content: {e}")
            return ""
    
    def copy_selection_to_clipboard(self):
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.2)
        
class ShortcutsHandler:
    """This class is used to register and unregister global shortcuts."""
    def __init__(self):
        self.shortcuts = {}
    
    def register_shortcut(self, key_combo, callback):
        try:
            keyboard.add_hotkey(key_combo, callback)
            self.shortcuts[key_combo] = callback
        except Exception as e:
            print(f"Error registering shortcut {key_combo}: {e}")
            pass
    
    def unregister_all(self):
        try:
            keyboard.unhook_all()
            self.shortcuts.clear()
        except Exception as e:
            print(f"Error unregistering shortcuts: {e}")
            pass

class WordSelectionHandler:
    """This class is used to handle text selection in a text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def get_selected_text(self):
        """Return the selected text from the text widget."""
        if self.text_widget.tag_ranges(tk.SEL):
            return self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        return ""
    
    def get_first_word(self):
        """Selects first word from the text widget."""
        current_line = self.text_widget.get("insert linestart", "insert lineend").strip()
        if current_line:
            return current_line.split()[0]
        return ""