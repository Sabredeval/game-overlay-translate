import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import urllib.parse
from GUI.common.word_display import WordDisplay
from util.services.word_data_service import WordDataService

class BrowserInterface(tk.Toplevel):
    def __init__(self, parent, initial_word=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Word Browser")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        self.word_service = WordDataService()
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Word:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        if initial_word:
            self.search_var.set(initial_word)
            
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", self.search_word)
        
        search_button = ttk.Button(search_frame, text="Look Up", command=self.search_word)
        search_button.pack(side=tk.LEFT, padx=5)
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.word_display = WordDisplay(content_frame)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Save to My Words", 
                                    command=self.save_to_my_words)
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        self.open_browser_button = ttk.Button(button_frame, text="Open in Browser", 
                                             command=self.open_in_browser)
        self.open_browser_button.pack(side=tk.RIGHT, padx=5)
        
        if initial_word:
            self.search_word()
    
    def search_word(self, event=None):
        word = self.search_var.get().strip()
        if not word:
            return
        
        self.word_display.show_loading(f"Looking up '{word}'...")
        self.word_service.fetch_word_data_async(word, callback=self._on_word_data_loaded)
    
    def _on_word_data_loaded(self, word_data):
        """Handle word data loaded"""
        # Check if we need to select a variant first
        if word_data.get("needs_variant_selection"):
            # Show variant selector dialog
            self.word_service.show_variant_selector(
                self, 
                word_data["variants"],
                self._on_word_data_loaded  # Pass the same callback for the retry
            )
            return
            
        # Normal processing
        self.after(0, lambda: self._update_display(word_data))
    
    def _update_display(self, word_data):
        """Update the word display with loaded data"""
        self.word_display.display_word_data(word_data, self._on_related_word_click)
    
    def _on_related_word_click(self, word):
        """Handle click on a related word"""
        self.search_var.set(word)
        self.search_word()
    
    def open_in_browser(self):
        word = self.search_var.get().strip()
        if word:
            encoded_word = urllib.parse.quote(word)
            url = f"https://en.wiktionary.org/wiki/{encoded_word}"
            webbrowser.open(url)
    
    def save_to_my_words(self):
        word = self.search_var.get().strip()
        if not word:
            return
            
        if hasattr(self.parent, "db"):
            source_lang = self.parent.native_language_var.get() if hasattr(self.parent, "native_language_var") else "English"
            
            if self.parent.db.word_exists(word):
                messagebox.showinfo("Word Already Saved", 
                                  f"The word '{word}' is already saved.")
                return
            
            word_id = self.parent.db.save_word(word, source_lang)
            
            if word_id:
                messagebox.showinfo("Success", f"Word '{word}' saved to your list!")
            else:
                messagebox.showinfo("Error", "Could not save the word.")
        else:
            messagebox.showinfo("Database Error", "Database not available.")