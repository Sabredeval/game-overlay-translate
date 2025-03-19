import webbrowser
import urllib.parse
from tkinter import ttk, messagebox

from GUI.pages.word_info.word_info_model import WordInfoModel
from GUI.pages.word_info.word_info_view import WordInfoView

class WordInfoController:
    def __init__(self, parent, word, source_lang="English"):
        self.parent = parent
        self.word = word
        self.source_lang = source_lang
        
        self.model = WordInfoModel(word, source_lang)
        self.view = WordInfoView(parent)
        self.view.title(f"Word Info: {word}")
        self.view.create_ui(word)
        self.add_buttons()
        self.load_word_info()
        self.view._on_related_word_click = self.on_related_word_click
    
    def add_buttons(self):
        """Add action buttons to the Word Info view"""
        button_frame = self.view.button_frame
        
        save_btn = ttk.Button(button_frame, text="Save Word", command=self.save_word)
        save_btn.pack(side="left", padx=5)
        
        speak_btn = ttk.Button(button_frame, text="Pronounce", command=self.pronounce_word)
        speak_btn.pack(side="left", padx=5)
        
        browser_btn = ttk.Button(button_frame, text="Open in Browser", command=self.open_in_browser)
        browser_btn.pack(side="left", padx=5)
        
        close_btn = ttk.Button(button_frame, text="Close", command=self.view.destroy)
        close_btn.pack(side="right", padx=5)
    
    def load_word_info(self):
        """Load word information asynchronously"""
        self.model.fetch_data(callback=self.update_view)
    
    def update_view(self):
        """Update the view with data from the model"""
        self.view.after(0, self._update_view_main_thread)
    
    def _update_view_main_thread(self):
        """Update view elements with model data (in main thread)"""
        self.view.hide_loading()
        
        if self.model.error:
            self.view.display_error(self.model.error)
            return
        
        self.view.update_pronunciation(self.model.pronunciation)
        self.view.update_definitions(self.model.definitions_by_pos)
        self.view.update_etymology(self.model.etymology)
        self.view.update_examples(self.model.examples)
        self.view.update_related_words(self.model.related_words)
    
    def save_word(self):
        """Save the current word to database"""
        parent = self.view.parent
        if hasattr(parent, "db") and parent.db:
            source_lang = self.model.source_lang
            
            result = self.model.save_word(parent.db, self.model.word, source_lang)
            
            if result is None:
                messagebox.showinfo("Word Already Saved", 
                                   f"The word '{self.model.word}' is already saved.")
            elif result:
                messagebox.showinfo("Success", 
                                   f"Word '{self.model.word}' saved successfully!")
            else:
                messagebox.showinfo("Error", 
                                   "Could not save the word.")
        else:
            messagebox.showinfo("Database Error", 
                              "Cannot save word - database not available.")
    
    def pronounce_word(self, language="en"):
        """Play pronunciation of the word with Google Text-to-Speech and playsound library. 
           Creates temporary mp3 file.
        """
        try:
            from gtts import gTTS
            import os
            import tempfile
            from playsound import playsound
            
            tts = gTTS(text=self.word, lang=language)

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            tts.save(temp_file.name)
            
            playsound(temp_file.name)
                
            os.unlink(temp_file.name)
        except Exception as e:
            try:
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(self.word)
            except Exception as e:
                messagebox.showinfo("Pronunciation Error", 
                                f"Could not pronounce word: {str(e)}")
    
    def open_in_browser(self):
        """Open the word in Wiktionary browser"""
        encoded_word = urllib.parse.quote(self.model.word)
        url = f"https://en.wiktionary.org/wiki/{encoded_word}"
        webbrowser.open(url)
    
    def on_related_word_click(self, word):
        """Handle click on related word"""
        # Create a new word info window for the related word
        WordInfoController(self.parent, word, self.source_lang)