import tkinter as tk
from tkinter import ttk
from GUI.common.app_theme import AppTheme

class WordDisplay:
    """Reusable word display component that can be embedded in various views"""
    
    def __init__(self, parent, enable_tabs=True):
        self.parent = parent
        self.enable_tabs = enable_tabs
        
        if enable_tabs:
            self.notebook = ttk.Notebook(parent)
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
            self.def_tab, self.def_text = self._create_text_tab(self.notebook, "Definition")
            self.examples_tab, self.examples_text = self._create_text_tab(self.notebook, "Examples")
            self.etym_tab, self.etym_text = self._create_text_tab(self.notebook, "Etymology")
            self.related_tab, self.related_frame = self._create_related_tab(self.notebook)
        else:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.BOTH, expand=True)
            
            self.def_tab = frame
            _, self.def_text = self._create_text_widget(frame)
        
        for text_widget in self._get_text_widgets():
            self._configure_text_tags(text_widget)
    
    def _get_text_widgets(self):
        """Get all text widgets in this component"""
        widgets = [self.def_text]
        if self.enable_tabs:
            widgets.extend([self.examples_text, self.etym_text])
        return widgets
    
    def _configure_text_tags(self, text_widget):
        """Configure text tags for formatting"""
        text_widget.tag_configure("heading", font=AppTheme.HEADING_FONT, foreground=AppTheme.PRIMARY)
        text_widget.tag_configure("pos", font=AppTheme.SUBHEADING_FONT, foreground=AppTheme.PRIMARY_DARK)
        text_widget.tag_configure("normal", font=AppTheme.BODY_FONT)
        text_widget.tag_configure("italic", font=AppTheme.BODY_FONT)
        text_widget.tag_configure("example", font=AppTheme.BODY_FONT, foreground=AppTheme.ACCENT)
        text_widget.tag_configure("error", foreground="red")
    
    def _create_text_tab(self, parent, name):
        """Create a tab with a scrollable text widget"""
        tab = ttk.Frame(parent)
        parent.add(tab, text=name)
        
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        return tab, self._create_text_widget(frame)[1]
    
    def _create_text_widget(self, parent):
        """Create a text widget with scrollbar"""
        text = tk.Text(
            parent,
            wrap=tk.WORD, 
            padx=10, 
            pady=10,
            background="white", 
            highlightthickness=0,
            relief="flat", 
            font=AppTheme.BODY_FONT,
            height=10
        )
        text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(parent, command=text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        text.config(yscrollcommand=scrollbar.set)
        
        return parent, text
    
    def _create_related_tab(self, parent):
        """Create tab for related words"""
        tab = ttk.Frame(parent)
        parent.add(tab, text="Related Words")
        
        content_frame = ttk.Frame(tab, padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return tab, content_frame
    
    def display_word_data(self, word_data, on_related_word_click=None):
        """Display word data in the component"""
        if not word_data:
            return
            
        if "error" in word_data:
            self.display_error(word_data["error"])
            return
        
        self.update_definitions(word_data["word"], 
                              word_data.get("pronunciation", ""),
                              word_data.get("definitions_by_pos", {}))
        
        if self.enable_tabs:
            self.update_examples(word_data.get("examples", []))
            self.update_etymology(word_data.get("etymology", ""))
            self.update_related_words(
                word_data.get("related_words", {}), 
                on_related_word_click
            )
    
    def display_error(self, error_message):
        """Display error message"""
        self.def_text.config(state=tk.NORMAL)
        self.def_text.delete("1.0", tk.END)
        self.def_text.insert(tk.END, f"Error: {error_message}\n\n", "error")
        self.def_text.insert(tk.END, "Try opening the word in browser for more information.", "normal")
        self.def_text.config(state=tk.DISABLED)
        
        if self.enable_tabs:
            self.examples_text.config(state=tk.NORMAL)
            self.examples_text.delete("1.0", tk.END)
            self.examples_text.insert(tk.END, "No examples available due to error.", "normal")
            self.examples_text.config(state=tk.DISABLED)
            
            self.etym_text.config(state=tk.NORMAL)
            self.etym_text.delete("1.0", tk.END)
            self.etym_text.insert(tk.END, "No information available due to error.", "normal")
            self.etym_text.config(state=tk.DISABLED)
    
    def update_definitions(self, word, pronunciation, definitions_by_pos):
        """Update definitions display"""
        self.def_text.config(state=tk.NORMAL)
        self.def_text.delete("1.0", tk.END)
        
        self.def_text.insert(tk.END, f"{word}\n", "heading")
        
        if pronunciation:
            self.def_text.insert(tk.END, f"/{pronunciation}/\n\n", "normal")
        else:
            self.def_text.insert(tk.END, "\n", "normal")
        
        if not definitions_by_pos:
            self.def_text.insert(tk.END, "No definitions found for this word.", "normal")
        else:
            for pos, definitions in definitions_by_pos.items():
                self.def_text.insert(tk.END, f"{pos.capitalize()}\n", "pos")
                
                for i, definition in enumerate(definitions, 1):
                    self.def_text.insert(tk.END, f"{i}. {definition}\n\n", "normal")
        
        self.def_text.config(state=tk.DISABLED)
    
    def update_examples(self, examples):
        """Update examples display"""
        if not self.enable_tabs:
            return
            
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete("1.0", tk.END)
        
        if not examples:
            self.examples_text.insert(tk.END, "No example sentences available for this word.", "normal")
        else:
            for i, example in enumerate(examples, 1):
                self.examples_text.insert(tk.END, f"{i}. ", "normal")
                self.examples_text.insert(tk.END, f"{example}\n\n", "example")
        
        self.examples_text.config(state=tk.DISABLED)
    
    def update_etymology(self, etymology):
        """Update etymology display"""
        if not self.enable_tabs:
            return
            
        self.etym_text.config(state=tk.NORMAL)
        self.etym_text.delete("1.0", tk.END)
        
        if not etymology:
            self.etym_text.insert(tk.END, "No etymology information available for this word.", "normal")
        else:
            self.etym_text.insert(tk.END, etymology, "normal")
        
        self.etym_text.config(state=tk.DISABLED)
    
    def update_related_words(self, related_words, on_click_callback=None):
        """Update related words display"""
        if not self.enable_tabs:
            return
            
        for child in self.related_frame.winfo_children():
            child.destroy()
        
        if not related_words.get("synonyms") and not related_words.get("antonyms"):
            ttk.Label(
                self.related_frame,
                text="No related words information available.",
                font=AppTheme.BODY_FONT
            ).pack(pady=20)
            return
        
        if related_words.get("synonyms"):
            syn_label = ttk.Label(
                self.related_frame,
                text="Synonyms:",
                font=AppTheme.SUBHEADING_FONT,
                foreground=AppTheme.PRIMARY_DARK
            )
            syn_label.pack(anchor=tk.W, pady=(0, 5))
            
            syn_frame = ttk.Frame(self.related_frame)
            syn_frame.pack(fill=tk.X, pady=(0, 15))
            
            for i, word in enumerate(related_words["synonyms"]):
                btn = ttk.Button(
                    syn_frame, 
                    text=word,
                    command=lambda w=word: on_click_callback(w) if on_click_callback else None
                )
                btn.grid(row=i//3, column=i%3, padx=5, pady=3, sticky=tk.W)
        
        if related_words.get("antonyms"):
            ant_label = ttk.Label(
                self.related_frame,
                text="Antonyms:",
                font=AppTheme.SUBHEADING_FONT,
                foreground=AppTheme.PRIMARY_DARK
            )
            ant_label.pack(anchor=tk.W, pady=(0, 5))
            
            ant_frame = ttk.Frame(self.related_frame)
            ant_frame.pack(fill=tk.X)
            
            for i, word in enumerate(related_words["antonyms"]):
                btn = ttk.Button(
                    ant_frame, 
                    text=word,
                    command=lambda w=word: on_click_callback(w) if on_click_callback else None
                )
                btn.grid(row=i//3, column=i%3, padx=5, pady=3, sticky=tk.W)
    
    def show_loading(self, message="Loading..."):
        self.def_text.config(state=tk.NORMAL)
        self.def_text.delete("1.0", tk.END)
        self.def_text.insert(tk.END, message, "normal")
        self.def_text.config(state=tk.DISABLED)