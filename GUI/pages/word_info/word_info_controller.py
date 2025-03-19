import webbrowser
import urllib.parse
from tkinter import ttk, messagebox
from GUI.common.word_display import WordDisplay
from util.services.word_data_service import WordDataService

class WordInfoController:
    def __init__(self, parent, word, source_lang="English"):
        self.parent = parent
        self.word = word
        self.source_lang = source_lang
        self.word_data = None
        
        self.view = self._create_view()
        self._setup_components()
        
        self.word_service = WordDataService()
        self.load_word_data()
    
    def _create_view(self):
        """Create the word info view"""
        from GUI.pages.word_info.word_info_view import WordInfoView
        
        view = WordInfoView(self.parent)
        view.title(f"Word Info: {self.word}")
        view.create_ui()
        return view
    
    def _setup_components(self):
        """Set up components after view is created"""
        self.word_display = WordDisplay(self.view.content_frame)
        
        self.pronunciation_label = ttk.Label(self.view.header_frame, text="", font=("Segoe UI", 9))
        self.pronunciation_label.pack(side="left", padx=(10, 0))
        
        self._add_buttons(self.view.button_frame)
    
    def _add_buttons(self, button_frame):
        """Add action buttons to the view"""
        save_btn = ttk.Button(button_frame, text="Save Word", command=self.save_word)
        save_btn.pack(side="left", padx=5)
        
        speak_btn = ttk.Button(button_frame, text="Pronounce", command=self.pronounce_word)
        speak_btn.pack(side="left", padx=5)
        
        browser_btn = ttk.Button(button_frame, text="Open in Browser", command=self.open_in_browser)
        browser_btn.pack(side="left", padx=5)
        
        close_btn = ttk.Button(button_frame, text="Close", command=self.view.destroy)
        close_btn.pack(side="right", padx=5)
    
    def load_word_data(self):
        """Load word information asynchronously"""
        self.word_display.show_loading(f"Looking up information for '{self.word}'...")
        self.word_service.fetch_word_data_async(
            self.word, 
            self.source_lang,
            self._on_word_data_loaded
        )
        
    def _on_word_data_loaded(self, word_data):
        """Handle word data loaded callback"""
        # Check if we need to select a variant first
        if word_data.get("needs_variant_selection"):
            # Show variant selector dialog
            self.word_service.show_variant_selector(
                self.view, 
                word_data["variants"],
                self._on_word_data_loaded  # Pass the same callback for the retry
            )
            return
            
        # Normal processing
        self.word_data = word_data
        
        # Update view in main thread
        self.view.after(0, self._update_view)
    
    def _update_view(self):
        """Update the view with loaded data"""
        if not self.word_data:
            return
            
        self.word_display.display_word_data(
            self.word_data,
            self.on_related_word_click
        )
        
        if self.word_data.get("pronunciation"):
            self.pronunciation_label.config(text=f"/{self.word_data['pronunciation']}/")
    
    def on_related_word_click(self, word):
        """Handle click on a related word"""
        WordInfoController(self.parent, word, self.source_lang)
    
    def save_word(self):
        """Save the word to the vocabulary database"""
        if not self.word:
            return
            
        parent = self.view.parent
        if hasattr(parent, "db") and parent.db:
            result = parent.db.save_word(self.word, self.source_lang)
            
            if result is None:
                messagebox.showinfo("Word Already Saved", 
                                   f"The word '{self.word}' is already saved.")
            elif result:
                messagebox.showinfo("Success", 
                                   f"Word '{self.word}' saved successfully!")
            else:
                messagebox.showinfo("Error", "Could not save the word.")
        else:
            messagebox.showinfo("Database Error", 
                              "Cannot save word - database not available.")
    
    def pronounce_word(self):
        """Pronounce the word using the speech service"""
        if self.word:
            if self.word_service.speak(self.word) is not None:
                messagebox.showinfo("Error", "Could not play pronunciation.")
        
    def open_in_browser(self):
        """Open the word in Wiktionary"""
        encoded_word = urllib.parse.quote(self.word)
        url = f"https://en.wiktionary.org/wiki/{encoded_word}"
        webbrowser.open(url)