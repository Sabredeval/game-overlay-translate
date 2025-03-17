import keyboard

###
# This class is used to register and unregister global shortcuts.
###
class ShortcutsHandler:
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