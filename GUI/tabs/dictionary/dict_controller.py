import threading
import webbrowser
import urllib.parse

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
    
    def lookup_word(self):
        """Look up the current word in the dictionary"""
        word = self.view.get_current_word()
        if not word:
            return
        
        # Show loading state
        self.view.show_loading()
        
        # Perform lookup in background thread
        threading.Thread(
            target=self._background_lookup,
            args=(word,),
            daemon=True
        ).start()
    
    def _background_lookup(self, word):
        """Perform dictionary lookup in background thread"""
        try:
            word_data = self.wiktionary_service.get_word_data(word)
            
            # Update UI in main thread
            self.view.after(0, lambda: self._update_ui_with_results(word_data))
        except Exception as e:
            self.view.after(0, lambda: self._handle_lookup_error(str(e)))
    
    def _update_ui_with_results(self, word_data):
        """Update UI with lookup results"""
        self.current_word_data = word_data
        self.view.display_word_info(word_data)
    
    def _handle_lookup_error(self, error_message):
        """Handle errors during lookup"""
        error_data = {
            "word": self.view.get_current_word(),
            "definitions_by_pos": {"error": [error_message]},
            "examples": [],
            "etymology": "Error retrieving etymology",
            "related_words": {}
        }
        self.view.display_word_info(error_data)
    
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
    
    def save_current_word(self):
        """Save the current word to the database"""
        word = self.view.get_current_word()
        if not word or not self.db_manager:
            return
        
        # We should have a proper method in the main controller for this
        # For now, we'll just call through to the database directly
        result = self.db_manager.save_word(word, "English")  # Default language
        
        # Ideally we would show feedback to the user
        # We could expose a method on the main controller to show a message
        print(f"Saved word '{word}' with result: {result}")
    
    def play_pronunciation(self):
        """Play pronunciation of current word"""
        # This would require audio capabilities
        # For now, just print a message
        print(f"Playing pronunciation for '{self.view.get_current_word()}'")
    
    def open_in_browser(self):
        """Open the current word in a web browser"""
        word = self.view.get_current_word()
        if word:
            encoded_word = urllib.parse.quote(word)
            url = f"https://en.wiktionary.org/wiki/{encoded_word}"
            webbrowser.open(url)