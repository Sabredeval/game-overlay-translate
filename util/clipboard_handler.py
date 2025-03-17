import keyboard
import time

class ClipboardHandler:
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