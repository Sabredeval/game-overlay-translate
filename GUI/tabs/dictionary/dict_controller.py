import threading
import webbrowser
import urllib.parse
from util.services.word_data_service import WordDataService

class DictionaryController:
    def __init__(self, view, wiktionary_service, db_manager):
        """Initialize the dictionary controller
        
        Args:
            view: The dictionary tab view
            wiktionary_service: Service for dictionary lookups
            db_manager: Database manager for saving words
        """
        self.view = view
        self.view.set_controller(self)
        self.wiktionary_service = wiktionary_service
        self.db_manager = db_manager
        self.current_word_data = None
        
        # Create word data service
        self.word_data_service = WordDataService()
    
    def lookup_word(self):
        """Look up the current word in the dictionary"""
        word = self.view.get_current_word()
        if not word:
            return
        
        self.view.show_loading()
        
        self.word_data_service.fetch_word_data_async(
            word,
            "English",  # Default language
            self._on_word_data_loaded
        )
    
    def _on_word_data_loaded(self, word_data):
        """Handle word data loaded callback"""
        if word_data.get("needs_variant_selection"):
            self.word_data_service.show_variant_selector(
                self.view, 
                word_data["variants"],
                self._on_word_data_loaded 
            )
            return
            
        self.current_word_data = word_data
        
        self.view.after(0, lambda: self.view.display_word_info(word_data))
    
    def on_search_text_changed(self, text):
        """Handle changes to the search text for suggestions"""
        if len(text) >= 2 and self.wiktionary_service:
            threading.Thread(
                target=self._fetch_suggestions,
                args=(text,),
                daemon=True
            ).start()
    
    def _fetch_suggestions(self, prefix):
        """Fetch word suggestions in background thread"""
        try:
            suggestions = self.wiktionary_service.search_similar_words(prefix)
            self.view.after(0, lambda: self.view.update_suggestions(suggestions))
        except Exception:
            # Silently fail for suggestions
            pass
    
    def on_suggestion_selected(self, word):
        """Handle selection of a suggestion"""
        self.view.dict_search_var.set(word)
        self.lookup_word()
    
    def on_related_word_selected(self, word):
        """Handle selection of a related word"""
        self.view.dict_search_var.set(word)
        self.lookup_word()
    
    def save_current_word(self, language="English"):
        """Save the current word to the database"""
        word = self.view.get_current_word()
        if not word or not self.db_manager:
            return
        
        result = self.db_manager.save_word(word, language)
        
        print(f"Saved word '{word}' with result: {result}")
    
    def play_pronunciation(self):
        """Play pronunciation of current word"""
        if self.word_data_service.speak(self.view.get_current_word()) != None:
            from tkinter import messagebox
            messagebox.showinfo("Pronunciation", "Pronunciation not available right now.")
        
    
    def open_in_browser(self):
        """Open the current word in a web browser"""
        word = self.view.get_current_word()
        if word:
            encoded_word = urllib.parse.quote(word)
            url = f"https://en.wiktionary.org/wiki/{encoded_word}"
            webbrowser.open(url)