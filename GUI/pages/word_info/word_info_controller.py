import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import urllib.parse
from GUI.pages.word_info.word_info_model import WordInfoModel, DatabaseHandler
from GUI.pages.word_info.word_info_view import WordInfoView

class WordInfoController:
    def __init__(self, parent, word, source_lang="English"):
        self.model = WordInfoModel(word, source_lang)
        self.view = WordInfoView(parent)
        self.db_handler = DatabaseHandler()
        
        self.view.title(f"Word Info: {word}")
        self.view.geometry("400x300")
        self.view.create_ui()
        
        self.add_buttons()
        self.load_word_info()
    
    def add_buttons(self):
        button_frame = self.view.create_button_frame()
        
        save_btn = ttk.Button(button_frame, text="Save Word", command=self.save_word)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(button_frame, text="Open in Browser", command=self.open_in_browser)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(button_frame, text="Close", command=self.view.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def load_word_info(self):
        self.view.def_text.insert(tk.END, f"Loading definition for '{self.model.word}'...\n\n")
        self.view.etym_text.insert(tk.END, f"Loading etymology for '{self.model.word}'...\n\n")
        self.view.examples_text.insert(tk.END, f"Loading examples for '{self.model.word}'...\n\n")
        
        self.view.after(500, self.update_view)
    
    def update_view(self):
        """Update UI with word data"""
        # TODO - Make async call to fetch data
        self.model.fetch_data()
        
        for text_widget in [self.view.def_text, self.view.etym_text, self.view.examples_text]:
            text_widget.delete(1.0, tk.END)

        self.view.def_text.insert(tk.END, f"Definition of '{self.model.word}':\n\n", "heading")
        for i, definition in enumerate(self.model.definitions, 1):
            self.view.def_text.insert(tk.END, f"{i}. {definition}\n\n", "normal")
        
        self.view.etym_text.insert(tk.END, f"Etymology of '{self.model.word}':\n\n", "heading")
        self.view.etym_text.insert(tk.END, self.model.etymology + "\n\n", "normal")
        
        self.view.examples_text.insert(tk.END, f"Examples of '{self.model.word}':\n\n", "heading")
        for i, example in enumerate(self.model.examples, 1):
            self.view.examples_text.insert(tk.END, f"{i}. {example}\n\n", "normal")
    
    def save_word(self):
        parent = self.view.parent
        if hasattr(parent, "word_db"):
            source_lang = self.model.source_lang
            
            result = self.db_handler.save_word(parent.word_db, self.model.word, source_lang)
            
            if result is None:
                messagebox.showinfo("Word Already Saved", f"The word '{self.model.word}' is already saved.")
            elif result:
                messagebox.showinfo("Success", f"Word '{self.model.word}' saved successfully!")
            else:
                messagebox.showinfo("Error", "Could not save the word.")
    
    def open_in_browser(self):
        encoded_word = urllib.parse.quote(self.model.word)
        url = f"https://en.wiktionary.org/wiki/{encoded_word}"
        webbrowser.open(url)
