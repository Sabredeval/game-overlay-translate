from tkinter import messagebox
from view.saved_words_interface import SavedWordsInterface
from view.settings_interface import SettingsInterface
from view.browser_interface import BrowserInterface
from view.main_interface import MainView    
from model.database_manager import WordDatabase
from model.config_model import ConfigModel
from controller.word_database_controller import WordDatabaseController
from controller.word_info_controller import WordInfoController
from util.selection_tool import GlobalSelectionApp
from util.shortcut_handler import ShortcutsHandler
from util.tray_icon_handler import TrayIconHandler
from util.word_selection_handler import WordSelectionHandler
from util.clipboard_handler import ClipboardHandler
from util.translation_service import LibreTranslateService

class MainController:
    def __init__(self):
        # Initialize models
        self.config_model = ConfigModel()
        
        # Initialize view
        self.view = MainView()
        
        # Initialize database
        self.db = WordDatabase()
        self.db_controller = WordDatabaseController(self.db)
        
        # Initialize controllers
        self.shortcuts_controller = ShortcutsHandler()
        self.clipboard_controller = ClipboardHandler(self.view)
        self.word_selection_controller = WordSelectionHandler(self.view.native_text_widget)
        
        # Initialize translation service
        self.translation_service = LibreTranslateService()
        self.translation_service.start()  # Start service in background
        
        # Initialize tray icon
        self.tray_icon_handler = TrayIconHandler(
            "Pymage",
            "resources/icon.png",
            self.restore_window,
            self.exit_application
        )
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        
        self.view.on_close = self.minimize_to_tray
        
        # Add translation button
        self.view.add_translate_button(self.translate_text)
    
    # Add this new method
    def translate_text(self):
        """Translate the text in the native text widget"""
        text = self.view.native_text_widget.get("1.0", "end-1c").strip()
        if not text:
            return
            
        # Get selected languages
        source_lang = self.get_language_code(self.view.native_language_var.get())
        target_lang = self.get_language_code(self.view.translated_language_var.get())
        
        # Ensure translation service is ready
        if not self.translation_service.ready:
            self.view.show_status("Translation service is starting, please wait...")
            if not self.translation_service.wait_until_ready(10):
                messagebox.showinfo("Translation Service", "The translation service is still starting up. Please try again in a moment.")
                return
        
        # Show translating status
        self.view.show_status("Translating...")
            
        # Perform translation in a separate thread to avoid freezing UI
        def do_translation():
            translated = self.translation_service.translate(text, source_lang, target_lang)
            if translated:
                # Update the UI in the main thread
                self.view.after(0, lambda: self.update_translation_result(translated))
            else:
                self.view.after(0, lambda: self.view.show_status("Translation failed"))
        
        import threading
        threading.Thread(target=do_translation, daemon=True).start()
    
    def update_translation_result(self, translated_text):
        """Update the translation result in the UI"""
        self.view.translated_text_widget.config(state="normal")
        self.view.translated_text_widget.delete("1.0", "end")
        self.view.translated_text_widget.insert("1.0", translated_text)
        self.view.translated_text_widget.config(state="disabled")
        self.view.show_status("Translation completed")
    
    def get_language_code(self, language_name):
        """Convert language name to ISO code"""
        language_map = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de"
        }
        return language_map.get(language_name, "en")
    
    def setup_ui(self):
        # Set language options
        self.view.set_language_options(
            self.config_model.get_languages(),
            self.config_model.default_native,
            self.config_model.default_translated
        )
        
        # Create buttons with commands
        self.view.create_buttons({
            "saved_words": self.on_saved_words,
            "browse_words": self.on_browse_words,
            "settings": self.on_settings,
            "start_selection": self.start_selection,
            "save_word": self.save_word
        })
    
    def setup_shortcuts(self):
        self.shortcuts_controller.register_shortcut("ctrl+q", self.show_word_info)
        self.shortcuts_controller.register_shortcut("ctrl+e", self.start_selection)
    
    def setup_tray(self):
        self.tray_icon_handler.create_icon()
    
    def show_word_info(self, event=None):
        self.clipboard_controller.copy_selection_to_clipboard()
        clipboard_content = self.clipboard_controller.get_clipboard_text()
        if clipboard_content:
            WordInfoController(self.view, clipboard_content)
    
    def save_current_word(self, event=None):
        word = self.word_selection_controller.get_selected_text()
        if not word:
            messagebox.showinfo("No Word Selected", "Please select a word or position the cursor on a word.")
            return
        
        self.save_word_to_db(word)
    
    def save_word_to_db(self, word):
        source_lang = self.view.native_language_var.get()
        result = self.db_controller.save_word(word, source_lang)
        
        if result is None:
            messagebox.showinfo("Word Already Saved", f"The word '{word}' is already saved.")
        elif result:
            messagebox.showinfo("Success", f"Word '{word}' saved successfully!")
        else:
            messagebox.showinfo("Error", "Could not save the word.")
    
    def minimize_to_tray(self):
        self.view.withdraw()
    
    def restore_window(self):
        self.view.deiconify()
        self.tray_icon_handler.stop()
        self.tray_icon_handler.create_icon()
    
    def exit_application(self):
        self.shortcuts_controller.unregister_all()
        
        # Stop translation service
        self.translation_service.stop()
        
        if self.db:
            self.db.close()
        
        self.tray_icon_handler.stop()
        self.view.destroy()
    
    def on_saved_words(self):
        SavedWordsInterface(self.view, self.db)
    
    def on_browse_words(self):
        initial_word = self.word_selection_controller.get_selected_text()
        BrowserInterface(self.view, initial_word)
    
    def on_settings(self):
        SettingsInterface(self.view)
    
    def start_selection(self):
        if not hasattr(self, "selection_app") or self.selection_app is None:
            self.selection_app = GlobalSelectionApp(self.view)
        self.selection_app.on_ctrl_e()
    
    def save_word(self):
        word = self.word_selection_controller.get_selected_text()
        if not word:
            word = self.word_selection_controller.get_first_word_from_current_line()
        
        if not word:
            messagebox.showinfo("No word selected", "Please select a word to save.")
            return
        
        self.save_word_to_db(word)
    
    def run(self):
        self.view.mainloop()