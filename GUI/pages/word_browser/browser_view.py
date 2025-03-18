import tkinter as tk
from tkinter import ttk
import webbrowser
import urllib.parse

class BrowserInterface(tk.Toplevel):
    def __init__(self, parent, initial_word=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Wiktionary Browser")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Create the main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create search frame at the top
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
        
        notebook_frame = ttk.Frame(main_frame)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Definition tab
        self.def_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.def_tab, text="Definition")
        
        # Set up scrollable text area for definitions
        def_scroll = ttk.Scrollbar(self.def_tab)
        def_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.definition_text = tk.Text(self.def_tab, wrap=tk.WORD)
        self.definition_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.definition_text.config(yscrollcommand=def_scroll.set)
        def_scroll.config(command=self.definition_text.yview)
        
        # Etymology tab
        self.etym_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.etym_tab, text="Etymology")
        
        etym_scroll = ttk.Scrollbar(self.etym_tab)
        etym_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.etymology_text = tk.Text(self.etym_tab, wrap=tk.WORD)
        self.etymology_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.etymology_text.config(yscrollcommand=etym_scroll.set)
        etym_scroll.config(command=self.etymology_text.yview)
        
        # Examples tab
        self.examples_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.examples_tab, text="Examples")
        
        examples_scroll = ttk.Scrollbar(self.examples_tab)
        examples_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.examples_text = tk.Text(self.examples_tab, wrap=tk.WORD)
        self.examples_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.examples_text.config(yscrollcommand=examples_scroll.set)
        examples_scroll.config(command=self.examples_text.yview)

        # Web view tab
        self.web_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.web_tab, text="Online Definition")
        
        web_info = ttk.Label(self.web_tab, 
                            text="Click the 'Open in Browser' button to see the full Wiktionary page.")
        web_info.pack(pady=20)
        
        open_browser_button = ttk.Button(self.web_tab, text="Open in Browser", 
                                        command=self.open_in_browser)
        open_browser_button.pack(pady=10)

        # Bottom button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        save_button = ttk.Button(button_frame, text="Save to My Words", 
                                command=self.save_to_my_words)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        if initial_word:
            self.search_word()
    
    def search_word(self, event=None):
        word = self.search_var.get().strip()
        if not word:
            return
            
        from util.services.wiktionary_service import WiktionaryService
        service = WiktionaryService()
        word_data = service.get_word_data(word)
        
        self.update_definition_tab(word_data)
        self.update_etymology_tab(word_data)
        self.update_examples_tab(word_data)
    
    def update_definition_tab(self, word_data):
        self.definition_text.config(state=tk.NORMAL)
        self.definition_text.delete(1.0, tk.END)
        
        if "error" in word_data:
            self.definition_text.insert(tk.END, f"Error: {word_data['error']}")
            self.definition_text.config(state=tk.DISABLED)
            return
            
        self.definition_text.insert(tk.END, "Definitions:\n\n", "heading")
        
        if not word_data["definitions"]:
            self.definition_text.insert(tk.END, "No definitions found.\n")
        else:
            for i, definition in enumerate(word_data["definitions"], 1):
                self.definition_text.insert(tk.END, f"{i}. {definition}\n\n")
                
        if word_data.get("pronunciation"):
            self.definition_text.insert(tk.END, "\nPronunciation:\n\n", "heading")
            self.definition_text.insert(tk.END, f"{word_data['pronunciation']}\n")
            
        self.definition_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        
        self.definition_text.config(state=tk.DISABLED)
    
    def update_etymology_tab(self, word_data):
        self.etymology_text.config(state=tk.NORMAL)
        self.etymology_text.delete(1.0, tk.END)
        
        if "error" in word_data:
            self.etymology_text.insert(tk.END, f"Error: {word_data['error']}")
            self.etymology_text.config(state=tk.DISABLED)
            return
            
        self.etymology_text.insert(tk.END, "Etymology:\n\n", "heading")
        
        if not word_data.get("etymology"):
            self.etymology_text.insert(tk.END, "No etymology information available.")
        else:
            self.etymology_text.insert(tk.END, word_data["etymology"])
            
        self.etymology_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        self.etymology_text.config(state=tk.DISABLED)
    
    def update_examples_tab(self, word_data):
        """Update the examples tab with word data"""
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete(1.0, tk.END)
        
        if "error" in word_data:
            self.examples_text.insert(tk.END, f"Error: {word_data['error']}")
            self.examples_text.config(state=tk.DISABLED)
            return
            
        self.examples_text.insert(tk.END, "Examples:\n\n", "heading")
        
        if not word_data["examples"]:
            self.examples_text.insert(tk.END, "No examples available.")
        else:
            for i, example in enumerate(word_data["examples"], 1):
                self.examples_text.insert(tk.END, f"{i}. {example}\n\n")
                
        self.examples_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        
        self.examples_text.config(state=tk.DISABLED)
    
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
            
        if hasattr(self.parent, "word_db"):
            source_lang = self.parent.native_language_var.get()
            
            if self.parent.word_db.word_exists(word):
                tk.messagebox.showinfo("Word Already Saved", 
                                      f"The word '{word}' is already saved.")
                return
            
            word_id = self.parent.word_db.save_word(word, source_lang)
            
            if word_id:
                tk.messagebox.showinfo("Success", f"Word '{word}' saved to your list!")
            else:
                tk.messagebox.showinfo("Already Saved", 
                                      f"The word '{word}' is already in your saved list.")