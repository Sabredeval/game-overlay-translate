import json
import os

class ConfigModel:
    """Stores configuration settings for the application"""
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        
        self.config = {
            "languages": ["English", "Spanish", "French", "German"],
            "default_native": "English",
            "default_translated": "Spanish",
            "theme": "Light",
            "font_size": "12",
            "hotkeys": {
                "selection": "ctrl+e",
                "save": "ctrl+s"
            }
        }
        
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception:
                pass
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def get_languages(self):
        return self.config["languages"]
    
    @property
    def default_native(self):
        return self.config["default_native"]
    
    @property
    def default_translated(self):
        return self.config["default_translated"]
    
    def get_theme(self):
        return self.config.get("theme", "Light")
    
    def set_theme(self, theme):
        self.config["theme"] = theme
    
    def get_font_size(self):
        return self.config.get("font_size", "12")
    
    def set_font_size(self, size):
        self.config["font_size"] = size
    
    def get_hotkey(self, action):
        return self.config.get("hotkeys", {}).get(action, "")
    
    def set_hotkey(self, action, key_combo):
        if "hotkeys" not in self.config:
            self.config["hotkeys"] = {}
        self.config["hotkeys"][action] = key_combo