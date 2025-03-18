from pages.settings.settings_view import SettingsInterface

class SettingsController:
    def __init__(self, parent, config_model):
        self.parent = parent
        self.config_model = config_model
        
        self.view = SettingsInterface(parent)
        self.view.set_controller(self)
    
    def get_settings(self):
        """Get current application settings"""
        return {
            'source_language': self.parent.native_language_var.get(),
            'target_language': self.parent.translated_language_var.get(),
            'theme': self.config_model.get_theme(),
            'font_size': self.config_model.get_font_size(),
            'selection_hotkey': self.config_model.get_hotkey('selection'),
            'save_hotkey': self.config_model.get_hotkey('save')
        }
    
    def save_settings(self, settings):
        if 'source_language' in settings:
            self.parent.native_language_var.set(settings['source_language'])
        
        if 'target_language' in settings:
            self.parent.translated_language_var.set(settings['target_language'])
        
        if 'theme' in settings:
            self.config_model.set_theme(settings['theme'])
            
        if 'font_size' in settings:
            self.config_model.set_font_size(settings['font_size'])
            
        if 'selection_hotkey' in settings:
            self.config_model.set_hotkey('selection', settings['selection_hotkey'])
            
        if 'save_hotkey' in settings:
            self.config_model.set_hotkey('save', settings['save_hotkey'])
        
        self.config_model.save()
        
        self.view.show_message("Settings Saved", "Your settings have been saved.")
        self.view.destroy()
    
    def cancel(self):
        self.view.destroy()