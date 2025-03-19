import tkinter as tk
from tkinter import ttk
from GUI.common.app_theme import AppTheme

class WordInfoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Word Information")
        self.geometry("550x400")
        self.minsize(400, 300)
        self.configure(bg=AppTheme.BG_LIGHT)
        
        self.attributes('-topmost', True)
        self.grab_set()
        self.focus_force()
        self.bind("<FocusOut>", self.on_focus_out)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.loading_indicator = None

    def on_focus_out(self, event=None):
        if self.winfo_exists() and not self.focus_get():
            self.destroy()
    
    def on_close(self):
        """Clean up on window close"""
        self.grab_release()
        self.destroy()
    
    def create_ui(self, word):
        """Create the main UI components"""
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        self.word_label = ttk.Label(self.header_frame, 
                                  text=word, 
                                  font=AppTheme.TITLE_FONT)
        self.word_label.pack(side=tk.LEFT)
        
        self.pronunciation_label = ttk.Label(self.header_frame, 
                                           text="",
                                           font=AppTheme.SMALL_FONT)
        self.pronunciation_label.pack(side=tk.LEFT, padx=(10, 0))
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.def_tab, self.def_text = self.create_tab("Definition")
        self.examples_tab, self.examples_text = self.create_tab("Examples")
        self.etym_tab, self.etym_text = self.create_tab("Etymology") 
        self.related_tab, self.related_frame = self.create_related_tab()
        
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        for text_widget in [self.def_text, self.etym_text, self.examples_text]:
            text_widget.tag_configure("heading", font=AppTheme.HEADING_FONT, foreground=AppTheme.PRIMARY)
            text_widget.tag_configure("pos", font=AppTheme.SUBHEADING_FONT, foreground=AppTheme.PRIMARY_DARK)
            text_widget.tag_configure("normal", font=AppTheme.BODY_FONT)
            text_widget.tag_configure("italic", font=AppTheme.BODY_FONT)
            text_widget.tag_configure("example", font=AppTheme.BODY_FONT, foreground=AppTheme.ACCENT)
            text_widget.tag_configure("error", foreground="red")
        
        self.show_loading()
    
    def create_tab(self, name):
        """Create a tab with a scrollable text widget"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=name)
        
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        text = tk.Text(frame, wrap=tk.WORD, padx=10, pady=10, 
                      background="white", highlightthickness=0,
                      relief="flat", font=AppTheme.BODY_FONT,
                      height=10)
        text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        text.config(yscrollcommand=scrollbar.set)
        
        return tab, text
    
    def create_related_tab(self):
        """Create tab for related words"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Related Words")
        
        content_frame = ttk.Frame(tab, padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return tab, content_frame
    
    def show_loading(self):
        """Show loading indicator"""
        self.loading_frame = ttk.Frame(self)
        self.loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        loading_label = ttk.Label(self.loading_frame, text="Loading word information...",
                                 font=AppTheme.BODY_FONT)
        loading_label.pack(pady=10)
        
        self.loading_progress = ttk.Progressbar(self.loading_frame, 
                                              mode="indeterminate", 
                                              length=200)
        self.loading_progress.pack(pady=10)
        self.loading_progress.start()
    
    def hide_loading(self):
        """Hide the loading indicator"""
        if hasattr(self, 'loading_frame'):
            self.loading_progress.stop()
            self.loading_frame.destroy()
    
    def display_error(self, error_message):
        """Display error in all tabs"""
        self.def_text.config(state=tk.NORMAL)
        self.def_text.delete("1.0", tk.END)
        self.def_text.insert(tk.END, f"Error: {error_message}\n\n", "error")
        self.def_text.insert(tk.END, "Try opening the word in browser for more information.", "normal")
        self.def_text.config(state=tk.DISABLED)
        
        self.etym_text.config(state=tk.NORMAL)
        self.etym_text.delete("1.0", tk.END)
        self.etym_text.insert(tk.END, "No information available due to error.", "normal")
        self.etym_text.config(state=tk.DISABLED)
        
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete("1.0", tk.END)
        self.examples_text.insert(tk.END, "No examples available due to error.", "normal")
        self.examples_text.config(state=tk.DISABLED)
    
    def update_pronunciation(self, pronunciation):
        """Update pronunciation display"""
        if pronunciation:
            self.pronunciation_label.config(text=f"/{pronunciation}/")
        else:
            self.pronunciation_label.config(text="")
    
    def update_definitions(self, definitions_by_pos):
        """Update definitions tab"""
        self.def_text.config(state=tk.NORMAL)
        self.def_text.delete("1.0", tk.END)
        
        if not definitions_by_pos:
            self.def_text.insert(tk.END, "No definitions found for this word.", "normal")
            self.def_text.config(state=tk.DISABLED)
            return
        
        for pos, definitions in definitions_by_pos.items():
            self.def_text.insert(tk.END, f"{pos.title()}\n", "pos")
            
            for i, definition in enumerate(definitions, 1):
                self.def_text.insert(tk.END, f"{i}. {definition}\n\n", "normal")
                
        self.def_text.config(state=tk.DISABLED)
    
    def update_etymology(self, etymology):
        """Update etymology tab"""
        self.etym_text.config(state=tk.NORMAL)
        self.etym_text.delete("1.0", tk.END)
        
        if not etymology:
            self.etym_text.insert(tk.END, "No etymology information available for this word.", "normal")
        else:
            self.etym_text.insert(tk.END, etymology, "normal")
            
        self.etym_text.config(state=tk.DISABLED)
    
    def update_examples(self, examples):
        """Update examples tab"""
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete("1.0", tk.END)
        
        if not examples:
            self.examples_text.insert(tk.END, "No example sentences available for this word.", "normal")
            self.examples_text.config(state=tk.DISABLED)
            return
            
        for i, example in enumerate(examples, 1):
            self.examples_text.insert(tk.END, f"{i}. ", "normal")
            self.examples_text.insert(tk.END, f"{example}\n\n", "example")
            
        self.examples_text.config(state=tk.DISABLED)
    
    def update_related_words(self, related_words):
        """Update related words tab"""
        for child in self.related_frame.winfo_children():
            child.destroy()
            
        if not related_words.get("synonyms") and not related_words.get("antonyms"):
            ttk.Label(self.related_frame, 
                    text="No related words information available.",
                    font=AppTheme.BODY_FONT).pack(pady=20)
            return
            
        if related_words.get("synonyms"):
            syn_label = ttk.Label(self.related_frame, 
                                text="Synonyms:", 
                                font=AppTheme.SUBHEADING_FONT,
                                foreground=AppTheme.PRIMARY_DARK)
            syn_label.pack(anchor=tk.W, pady=(0, 5))
            
            syn_frame = ttk.Frame(self.related_frame)
            syn_frame.pack(fill=tk.X, pady=(0, 15))
            
            for i, word in enumerate(related_words["synonyms"]):
                btn = ttk.Button(syn_frame, text=word, style="Word.TButton",
                               command=lambda w=word: self._on_related_word_click(w))
                btn.grid(row=i//3, column=i%3, padx=5, pady=3, sticky=tk.W)

        if related_words.get("antonyms"):
            ant_label = ttk.Label(self.related_frame, 
                                text="Antonyms:", 
                                font=AppTheme.SUBHEADING_FONT,
                                foreground=AppTheme.PRIMARY_DARK)
            ant_label.pack(anchor=tk.W, pady=(0, 5))
            
            ant_frame = ttk.Frame(self.related_frame)
            ant_frame.pack(fill=tk.X)
            
            for i, word in enumerate(related_words["antonyms"]):
                btn = ttk.Button(ant_frame, text=word, style="Word.TButton",
                               command=lambda w=word: self._on_related_word_click(w))
                btn.grid(row=i//3, column=i%3, padx=5, pady=3, sticky=tk.W)
    
    def _on_related_word_click(self, word):
        """Handle click on related word"""
        pass