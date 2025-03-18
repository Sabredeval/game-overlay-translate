import tkinter as tk
from tkinter import messagebox, Scrollbar, Label, Entry, Button, Listbox

class SavedWordsInterface(tk.Toplevel):
    def __init__(self, parent, word_db):
        super().__init__(parent)
        self.parent = parent
        self.word_db = word_db
        
        self.title("Saved Words")
        self.geometry("500x400")
        self.minsize(400, 300)
        
        # Search frame
        self.create_search_frame()
        
        # Words list
        self.create_list_frame()
        
        # Buttons
        self.create_button_frame()
        
        # Load initial data
        self.word_items = self.word_db.get_saved_words()
        self.update_word_list(self.word_items)
    
    def create_search_frame(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        search_button = Button(search_frame, text="Search", command=self.search_words)
        search_button.pack(side=tk.LEFT, padx=5)
    
    def create_list_frame(self):
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.word_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
        self.word_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.word_listbox.yview)
    
    def create_button_frame(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        delete_button = Button(button_frame, text="Delete", command=self.delete_selected_word)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        favorite_button = Button(button_frame, text="Toggle Favorite", command=self.toggle_favorite)
        favorite_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = Button(button_frame, text="Refresh", command=self.refresh_list)
        refresh_button.pack(side=tk.LEFT, padx=5)
    
    def search_words(self):
        query = self.search_entry.get().strip()
        if query:
            words = self.word_db.search_words(query)
        else:
            words = self.word_db.get_saved_words()
        
        self.update_word_list(words)
    
    def delete_selected_word(self):
        selection = self.word_listbox.curselection()
        if selection:
            index = selection[0]
            word_id = self.word_items[index][0]
            
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this word?"):
                self.word_db.delete_word(word_id)
                self.refresh_list()
    
    def toggle_favorite(self):
        selection = self.word_listbox.curselection()
        if selection:
            index = selection[0]
            word_id = self.word_items[index][0]
            
            self.word_db.toggle_favorite(word_id)
            self.refresh_list()
    
    def refresh_list(self):
        self.word_items = self.word_db.get_saved_words()
        self.update_word_list(self.word_items)
    
    def update_word_list(self, words):
        self.word_listbox.delete(0, tk.END)
        self.word_items = words
        
        for word_item in self.word_items:
            word_id, word_text, lang, date, favorite = word_item
            star = "★" if favorite else "☆"
            display_text = f"{star} {word_text} ({lang})"
            self.word_listbox.insert(tk.END, display_text)