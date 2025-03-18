from tkinter import messagebox
import threading
from pages.saved_words.saved_words_view import SavedWordsInterface
from pages.word_browser.browser_view import BrowserInterface
from pages.settings.settings_controller import SettingsController
from pages.word_info.word_info_controller import WordInfoController
from core.main_view import MainView    
from data.config_model import ConfigModel
from data.database_manager import WordDatabase
from util.selection_tool import GlobalSelectionApp
from util.utils import TrayIconHandler
from util.utils import ShortcutsHandler
from util.utils import WordSelectionHandler
from util.utils import ClipboardHandler

class MainController:
    def __init__(self):
        # Initialize models
        self.config_model = ConfigModel()
        
        # Initialize view
        self.view = MainView()
        
        # Initialize database
        self.db = WordDatabase()
        
        # Initialize controllers
        self.shortcuts_controller = ShortcutsHandler()
        self.clipboard_controller = ClipboardHandler(self.view)
        self.word_selection_controller = WordSelectionHandler(self.view.reading_text)
        
        # Initialize tray icon
        self.tray_icon_handler = TrayIconHandler(
            "Pymage",
            "resources/icons/icon.png",
            self.restore_window,
            self.exit_application
        )
        
        self.setup_tab_controllers()
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        
        self.view.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.view.on_close = self.minimize_to_tray

    def setup_tab_controllers(self):
        """Set up controllers for each tab"""
        # Dictionary tab controller - implement for dictionary lookups
        # self.dictionary_controller = self._create_dictionary_controller()
        
        # Reading assistant tab controller - implement for text analysis
        # self.reading_controller = self._create_reading_controller()
        
        # Vocabulary builder tab controller - implement for vocabulary management
        # self.vocab_controller = self._create_vocabulary_controller()
        
        # Word explorer tab controller - implement for word relationship exploration
        # self.explorer_controller = self._create_explorer_controller()
        
        # Dashboard tab controller - implement for stats and progress tracking
        # self.dashboard_controller = self._create_dashboard_controller()
        pass
    
    def on_tab_changed(self, event):
        """Handle tab change events"""
        tab_id = self.view.notebook.index("current")
        tab_name = self.view.notebook.tab(tab_id, "text")
        self.view.show_status(f"Switched to {tab_name} tab")
        
        # Refresh the active tab if needed
        # This is where you'll implement tab-specific refresh logic
        if tab_id == 0:  # Dictionary tab
            self._refresh_dictionary_tab()
        elif tab_id == 1:  # Reading Assistant tab
            self._refresh_reading_tab()
        elif tab_id == 2:  # Vocabulary Builder tab
            self._refresh_vocabulary_tab()
        elif tab_id == 3:  # Word Explorer tab
            self._refresh_explorer_tab()
        elif tab_id == 4:  # Study Dashboard tab
            self._refresh_dashboard_tab()
    
    def _refresh_dictionary_tab(self):
        """Refresh dictionary tab content"""
        # You'll implement this to update dictionary content
        pass
    
    def _refresh_reading_tab(self):
        """Refresh reading assistant tab content"""
        # You'll implement this to update reading assistant content
        pass
    
    def _refresh_vocabulary_tab(self):
        """Refresh vocabulary builder tab content"""
        # You'll implement this to update vocabulary builder content
        pass
    
    def _refresh_explorer_tab(self):
        """Refresh word explorer tab content"""
        # You'll implement this to update word explorer content
        pass
    
    def _refresh_dashboard_tab(self):
        """Refresh study dashboard tab content"""
        # You'll implement this to update dashboard stats and graphs
        pass
    
    def perform_dictionary_lookup(self, word=None):
        """Look up a word in the dictionary"""
        if word is None:
            # Get the word from the dictionary search field
            word = self.view.dict_search_var.get().strip()
        
        if not word:
            return
            
        self.view.show_status(f"Looking up: {word}")
        
        # Show basic loading indicator
        self.view.dictionary_tabs_dict["definition"].config(state="normal")
        self.view.dictionary_tabs_dict["definition"].delete("1.0", "end")
        self.view.dictionary_tabs_dict["definition"].insert("1.0", "Looking up definition...")
        self.view.dictionary_tabs_dict["definition"].config(state="disabled")
        
        # Perform lookup in background thread
        def background_lookup():
            try:
                # This is where you'll implement the actual dictionary lookup
                # For now, we'll just simulate a delay
                import time
                time.sleep(1)
                
                # Example word data structure - replace with your actual lookup
                word_data = {
                    'word': word,
                    'definitions': [f'Definition for {word}'],
                    'examples': [f'Example sentence using {word}.'],
                    'related_words': {'synonyms': ['similar1', 'similar2']}
                }
                
                # Update UI in the main thread
                self.view.after(0, lambda: self._update_dictionary_results(word_data))
            except Exception as e:
                self.view.after(0, lambda: self.view.show_status(f"Lookup error: {e}"))
        
        threading.Thread(target=background_lookup, daemon=True).start()
    
    def _update_dictionary_results(self, word_data):
        """Update dictionary tab with word lookup results"""
        if not word_data:
            self.view.show_status("No definition found")
            return
            
        # Update definition tab
        def_text = self.view.dictionary_tabs_dict["definition"]
        def_text.config(state="normal")
        def_text.delete("1.0", "end")
        def_text.insert("1.0", f"{word_data['word']}\n\n", "heading")
        
        for i, definition in enumerate(word_data.get('definitions', [])):
            def_text.insert("end", f"{i+1}. {definition}\n\n", "normal")
        def_text.config(state="disabled")
        
        # Update examples tab
        examples_text = self.view.dictionary_tabs_dict["examples"]
        examples_text.config(state="normal")
        examples_text.delete("1.0", "end")
        
        for example in word_data.get('examples', []):
            examples_text.insert("end", f"• {example}\n\n", "example")
        examples_text.config(state="disabled")
        
        # Update related words
        self.view.update_related_words(word_data.get('related_words', {}))
        
        # Show success status
        self.view.show_status(f"Found definition for '{word_data['word']}'")
    
    def analyze_reading_text(self):
        """Analyze text in reading assistant tab"""
        text = self.view.reading_text.get("1.0", "end-1c")
        if not text.strip():
            self.view.show_status("No text to analyze")
            return
            
        self.view.show_status("Analyzing text...")
        
        # This is where you'll implement text analysis
        # For now, we'll just count words and show a basic result
        word_count = len(text.split())
        self.view.reading_stats_var.set(f"Word count: {word_count}")
        
        # Highlight some words as an example (you'll implement actual highlighting)
        self.view.reading_text.tag_remove("highlight", "1.0", "end")
        
        # Show simple results
        self.view.show_status(f"Analysis complete. {word_count} words found.")
    
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
        
        # Connect dictionary search button
        if hasattr(self.view, "search_button"):
            self.view.search_button.config(command=self.perform_dictionary_lookup)
        
        # Connect reading assistant analyze button
        if hasattr(self.view, "analyze_button"):
            self.view.analyze_button.config(command=self.analyze_reading_text)
    
    def setup_shortcuts(self):
        self.shortcuts_controller.register_shortcut("ctrl+q", self.show_word_info)
        self.shortcuts_controller.register_shortcut("ctrl+e", self.start_selection)
        self.shortcuts_controller.register_shortcut("ctrl+d", self.perform_dictionary_lookup)
    
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
        result = self.db.save_word(word, source_lang)
        
        if result is None:
            messagebox.showinfo("Word Already Saved", f"The word '{word}' is already saved.")
        elif result:
            messagebox.showinfo("Success", f"Word '{word}' saved successfully!")
            self._refresh_vocabulary_tab()
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
        SettingsController(self.view, self.config_model)
    
    def start_selection(self):
        if not hasattr(self, "selection_app") or self.selection_app is None:
            self.selection_app = GlobalSelectionApp(self.view)
        self.selection_app.on_ctrl_e()
    
    def save_word(self):
        word = self.word_selection_controller.get_selected_text()
        if not word:
            word = self.word_selection_controller.get_first_word()
        
        if not word:
            messagebox.showinfo("No word selected", "Please select a word to save.")
            return
        
        self.save_word_to_db(word)
    
    def run(self):
        self.view.mainloop()