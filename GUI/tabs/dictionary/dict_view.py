import tkinter as tk
from tkinter import StringVar, ttk, Text
from GUI.common.app_theme import AppTheme

class DictionaryView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize variables
        self.dict_search_var = StringVar()
        self.controller = None
        
        self._create_search_area()
        self._create_content_area()
    
    def set_controller(self, controller):
        """Binds view with its controller"""
        self.controller = controller
        
        # Connect events
        self.dict_search_var.trace("w", self._on_search_changed)
        self.search_button.config(command=self._on_search_button)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self._on_suggestion_selected)
        
        # Connect buttons in the side panel
        self.save_button.config(command=self._on_save_word)
        self.pronunciation_button.config(command=self._on_pronunciation)
        self.browser_button.config(command=self._on_open_browser)
    
    def _create_search_area(self):
        """Create search field and suggestions"""
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_label = ttk.Label(search_frame, text="Lookup Word:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.dict_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.search_button = ttk.Button(search_frame, text="Look Up")
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        suggestion_frame = ttk.Frame(self)
        suggestion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.suggestion_listbox = tk.Listbox(suggestion_frame, height=5)
        self.suggestion_listbox.pack(fill=tk.X)
    
    def _create_content_area(self):
        """Create the main content area with dictionary content"""
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side for definitions
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Dictionary notebook
        self.dict_notebook = ttk.Notebook(left_frame)
        self.dict_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.definition_tab, self.definition_text = self._create_text_tab("Definition")
        self.examples_tab, self.examples_text = self._create_text_tab("Examples")
        self.etymology_tab, self.etymology_text = self._create_text_tab("Etymology")
        
        # Create a dictionary for easy access to text widgets
        self.tabs_dict = {
            "definition": self.definition_text,
            "examples": self.examples_text,
            "etymology": self.etymology_text
        }
        
        # Right sidebar
        right_frame = ttk.Frame(content_frame, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)  # Prevent shrinking
        
        related_label = ttk.Label(right_frame, text="Related Words", font=AppTheme.HEADING_FONT)
        related_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.related_listbox = tk.Listbox(right_frame, height=10)
        self.related_listbox.pack(fill=tk.X, pady=5)
        self.related_listbox.bind("<<ListboxSelect>>", self._on_related_word_selected)
        
        # Action buttons
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.save_button = ttk.Button(action_frame, text="Save to Vocabulary")
        self.save_button.pack(fill=tk.X, pady=2)
        
        self.pronunciation_button = ttk.Button(action_frame, text="Pronunciation")
        self.pronunciation_button.pack(fill=tk.X, pady=2)
        
        self.browser_button = ttk.Button(action_frame, text="Open in Browser")
        self.browser_button.pack(fill=tk.X, pady=2)
    
    def _create_text_tab(self, name):
        """Create a tab with a Text widget and scrollbar"""
        tab = ttk.Frame(self.dict_notebook)
        self.dict_notebook.add(tab, text=name)
        
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = Text(
            text_frame, 
            wrap=tk.WORD, 
            font=AppTheme.BODY_FONT,
            background="white",
            foreground=AppTheme.TEXT_DARK,
            padx=10,
            pady=10,
            state=tk.NORMAL
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Configure text tags for formatting
        text_widget.tag_configure("heading", font=AppTheme.HEADING_FONT)
        text_widget.tag_configure("subheading", font=("Segoe UI", 11, "bold"))
        text_widget.tag_configure("normal", font=AppTheme.BODY_FONT)
        text_widget.tag_configure("example", font=AppTheme.BODY_FONT, foreground="#0077CC")
        text_widget.tag_configure("highlight", background="#FFEB3B")
        
        return tab, text_widget
    
    def display_word_info(self, word_data):
        """Display word information in the tabs"""
        if not word_data:
            return
        
        # Clear and update definition tab
        self.definition_text.config(state=tk.NORMAL)
        self.definition_text.delete(1.0, tk.END)
        self.definition_text.insert(tk.END, f"{word_data['word']}\n", "heading")
        
        if word_data.get("pronunciation"):
            self.definition_text.insert(tk.END, f"/{word_data['pronunciation']}/\n\n", "normal")
        else:
            self.definition_text.insert(tk.END, "\n", "normal")
        
        # Display definitions by part of speech
        for pos, definitions in word_data.get("definitions_by_pos", {}).items():
            self.definition_text.insert(tk.END, f"{pos.capitalize()}\n", "subheading")
            for i, definition in enumerate(definitions, 1):
                self.definition_text.insert(tk.END, f"{i}. {definition}\n\n", "normal")
        
        # Clear and update examples tab
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete(1.0, tk.END)
        if word_data.get("examples"):
            for example in word_data["examples"]:
                self.examples_text.insert(tk.END, f"• {example}\n\n", "example")
        
        # Clear and update etymology tab
        self.etymology_text.config(state=tk.NORMAL)
        self.etymology_text.delete(1.0, tk.END)
        if word_data.get("etymology"):
            self.etymology_text.insert(tk.END, "Etymology:\n", "subheading")
            self.etymology_text.insert(tk.END, f"{word_data['etymology']}\n", "normal")
        
        # Set all text widgets to read-only
        self.definition_text.config(state=tk.DISABLED)
        self.examples_text.config(state=tk.DISABLED)
        self.etymology_text.config(state=tk.DISABLED)
        
        # Update related words
        self.update_related_words(word_data.get("related_words", {}))
    
    def update_related_words(self, related_words_dict):
        """Update the related words listbox"""
        self.related_listbox.delete(0, tk.END)
        
        # Add synonyms with a prefix
        for word in related_words_dict.get("synonyms", []):
            self.related_listbox.insert(tk.END, f"Syn: {word}")
        
        # Add antonyms with a prefix
        for word in related_words_dict.get("antonyms", []):
            self.related_listbox.insert(tk.END, f"Ant: {word}")
    
    def update_suggestions(self, suggestions):
        """Update suggestion listbox with new suggestions"""
        self.suggestion_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestion_listbox.insert(tk.END, suggestion)
    
    def show_loading(self):
        """Show loading state in definition tab"""
        self.definition_text.config(state=tk.NORMAL)
        self.definition_text.delete(1.0, tk.END)
        self.definition_text.insert(tk.END, "Looking up definition...", "normal")
        self.definition_text.config(state=tk.DISABLED)
    
    def get_current_word(self):
        """Get the currently searched word"""
        return self.dict_search_var.get().strip()
    
    def _on_search_changed(self, *args):
        """Handle changes to the search field"""
        if self.controller:
            search_text = self.dict_search_var.get()
            if len(search_text) >= 2:
                self.controller.on_search_text_changed(search_text)
    
    def _on_search_button(self):
        """Handle search button click"""
        if self.controller:
            self.controller.lookup_word()
    
    def _on_suggestion_selected(self, event):
        """Handle selection from suggestion listbox"""
        if self.controller and self.suggestion_listbox.curselection():
            index = self.suggestion_listbox.curselection()[0]
            selected_word = self.suggestion_listbox.get(index)
            self.controller.on_suggestion_selected(selected_word)
    
    def _on_related_word_selected(self, event):
        """Handle selection from related words listbox"""
        if self.controller and self.related_listbox.curselection():
            index = self.related_listbox.curselection()[0]
            selected_item = self.related_listbox.get(index)
            
            # Remove prefix if present
            if ": " in selected_item:
                _, word = selected_item.split(": ", 1)
                self.controller.on_related_word_selected(word)
    
    def _on_save_word(self):
        """Handle save button click"""
        if self.controller:
            self.controller.save_current_word()
    
    def _on_pronunciation(self):
        """Handle pronunciation button click"""
        if self.controller:
            self.controller.play_pronunciation()
    
    def _on_open_browser(self):
        """Handle open in browser button click"""
        if self.controller:
            self.controller.open_in_browser()