import re
import tkinter as tk
from tkinter import filedialog

class ReadingController:
    def __init__(self, view, dictionary_controller, db_manager):
        """Initialize the reading controller
            - view: The reading tab view
            - dictionary_controller: Dictionary controller for lookups
            - db_manager: Database manager for saving words
        """
        self.view = view
        self.view.set_controller(self)
        self.dictionary_controller = dictionary_controller
        self.db_manager = db_manager
        self.unknown_words = []
    
    def import_text(self):
        file_path = filedialog.askopenfilename(
            title="Import Text",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.view.set_text(text)
        except Exception as e:
            print(f"Error importing file: {e}")
    
    def clear_text(self):
        self.view.set_text("")
        self.view.update_statistics({"word_count": 0, "unique_words": 0, "reading_level": "N/A"})
        self.view.update_unknown_words([])
        self.unknown_words = []
    
    def analyze_text(self):
        """ Analyzes the reading text
            Provides statistics such as:
            - word count
            - unique words in the text
            - reading level based on frequency
        """
        text = self.view.get_text()
        if not text.strip():
            return
        
        words = re.findall(r'\b\w+\b', text.lower())
        
        word_count = len(words)
        unique_words = len(set(words))
        
        # TODO - implement algorithm for comparing frequency of words to determine reading level
        if word_count == 0:
            reading_level = "N/A"
        elif len([w for w in words if len(w) > 6]) / word_count > 0.2:
            reading_level = "Advanced"
        elif len([w for w in words if len(w) > 4]) / word_count > 0.3:
            reading_level = "Intermediate"
        else:
            reading_level = "Beginner"
        
        stats = {
            "word_count": word_count,
            "unique_words": unique_words,
            "reading_level": reading_level
        }
        self.view.update_statistics(stats)
        
        # TODO - find unknown words (words not in the database)
        unique_word_list = list(set(words))
        unique_word_list.sort()
        
        # TODO - add "show more" than 20 unknown words
        unknown_words = [word for word in unique_word_list if len(word) > 3][:20]
        self.unknown_words = unknown_words
        
        self.view.update_unknown_words(unknown_words)
    
    def add_all_unknown_words(self):
        """Add all unknown words to vocabulary"""
        if not self.unknown_words or not self.db_manager:
            return
        
        for word in self.unknown_words:
            self.db_manager.save_word(word, "English")
    
    def on_text_right_click(self, index, x, y):
        word = self._get_word_at_index(index)
        if not word:
            return
        
        commands = {
            "lookup": lambda: self._lookup_word(word),
            "add": lambda: self._add_word_to_vocabulary(word),
            "highlight": lambda: self.view.highlight_word(word)
        }
        
        self.view.show_context_menu(x, y, word, commands)
    
    def on_unknown_word_selected(self, word):
        self._lookup_word(word)
    
    def _lookup_word(self, word):
        if self.dictionary_controller:
            print(f"Looking up word:{word}")