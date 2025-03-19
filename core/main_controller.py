import logging
from tkinter import messagebox

# View imports
from GUI.pages.saved_words.saved_words_view import SavedWordsInterface
from GUI.pages.word_browser.browser_view import BrowserInterface
from GUI.pages.settings.settings_controller import SettingsController
from GUI.pages.word_info.word_info_controller import WordInfoController
from core.main_view import MainView    

# Controller imports
from GUI.tabs.dashboard.dashboard_controller import DashboardController
from GUI.tabs.dictionary.dict_controller import DictionaryController
from GUI.tabs.reading.reading_controller import ReadingController
from GUI.tabs.vocabulary.vocabulary_controller import VocabularyController
from GUI.tabs.explorer.explorer_controller import ExplorerController

# Data imports
from data.config_model import ConfigModel
from data.database_manager import WordDatabase
from util.services.online_service import WiktionaryService

# Util imports
from util.selection_tool import GlobalSelectionApp
from util.utils import TrayIconHandler, ShortcutsHandler, ClipboardHandler


class MainController:
    """Main controller that communicates between the main view and the data model"""
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                           filename='pymage.log')
        self.logger = logging.getLogger('Pymage')
        
        self.config_model = ConfigModel()
        self.view = MainView()
        
        try:
            self.db = WordDatabase()
        except Exception as e:
            self.logger.error(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
            self.db = None
        
        self.shortcuts_controller = ShortcutsHandler()
        self.clipboard_controller = ClipboardHandler(self.view)
        self.tray_icon_handler = TrayIconHandler("Pymage", "resources/icons/icon.png", 
                                               self.restore_window, self.exit_application)
        
        self.setup_tab_controllers()
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        
        self.view.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.view.on_close = self.minimize_to_tray
        self.logger.info("Application initialized successfully")

    def setup_tab_controllers(self):
        dict_service = WiktionaryService()
        
        self.controllers = [
            DictionaryController(self.view.dictionary_tab, dict_service, self.db),
            ReadingController(self.view.reading_tab, None, self.db),  # We'll set this after
            VocabularyController(self.view.vocabulary_tab, self.db),
            ExplorerController(self.view.explorer_tab, self.db),
            DashboardController(self.view.dashboard_tab, self.db)
        ]
        
        self.dictionary_controller, self.reading_controller, self.vocabulary_controller, \
        self.explorer_controller, self.dashboard_controller = self.controllers
        
        # Now set the dictionary controller for the reading controller
        self.reading_controller.dictionary_controller = self.dictionary_controller
    
    def on_tab_changed(self, event):
        tab_id = self.view.notebook.index("current")
        tab_name = self.view.notebook.tab(tab_id, "text")
        self.view.show_status(f"Switched to {tab_name} tab")
        
        if 0 <= tab_id < len(self.controllers):
            try:
                if hasattr(self.controllers[tab_id], 'refresh'):
                    self.controllers[tab_id].refresh()
            except Exception as e:
                self.logger.error(f"Error refreshing tab {tab_name}: {e}")
    
    def setup_ui(self):
        self.view.set_language_options(
            self.config_model.get_languages(),
            self.config_model.default_native,
            self.config_model.default_translated
        )
        
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
        self.shortcuts_controller.register_shortcut("ctrl+d", lambda: self.dictionary_controller.perform_lookup())
    
    def setup_tray(self):
        self.tray_icon_handler.create_icon()
    
    def show_word_info(self, event=None):
        self.clipboard_controller.copy_selection_to_clipboard()
        clipboard_content = self.clipboard_controller.get_clipboard_text()
        if clipboard_content:
            WordInfoController(self.view, clipboard_content)
    
    def save_word_to_db(self, word):
        if not word or not self.db:
            return False
            
        source_lang = self.view.native_language_var.get()
        result = self.db.save_word(word, source_lang)
        
        if result is None:
            messagebox.showinfo("Word Already Saved", f"The word '{word}' is already saved.")
        elif result:
            messagebox.showinfo("Success", f"Word '{word}' saved successfully!")
            if hasattr(self.vocabulary_controller, 'refresh'):
                self.vocabulary_controller.refresh()
            return True
        else:
            messagebox.showinfo("Error", "Could not save the word.")
            return False
    
    def minimize_to_tray(self):
        self.view.withdraw()
    
    def restore_window(self):
        self.view.deiconify()
        self.tray_icon_handler.stop()
        self.tray_icon_handler.create_icon()
    
    def exit_application(self):
        self.logger.info("Application shutting down")
        self.shortcuts_controller.unregister_all()
        
        if self.db:
            self.db.close()
        
        self.tray_icon_handler.stop()
        self.view.destroy()
    
    def on_saved_words(self):
        if not self.db:
            messagebox.showinfo("Database Error", "Cannot access saved words - database not available.")
            return
            
        SavedWordsInterface(self.view, self.db)
    
    def on_browse_words(self):
        BrowserInterface(self.view, "")
    
    def on_settings(self):
        SettingsController(self.view, self.config_model)
    
    def start_selection(self):
        try:
            if not hasattr(self, "selection_app") or self.selection_app is None:
                self.selection_app = GlobalSelectionApp(self.view)
            self.selection_app.on_ctrl_e()
        except Exception as e:
            self.logger.error(f"Error in screen selection: {e}")
            messagebox.showerror("Selection Error", f"Could not start selection: {e}")
    
    def save_word(self):
        messagebox.showinfo("Not Implemented", 
                          "Word selection is not fully implemented yet.")
    
    def run(self):
        self.view.mainloop()