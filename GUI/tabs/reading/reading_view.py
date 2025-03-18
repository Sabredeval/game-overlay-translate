import tkinter as tk
from tkinter import Text, StringVar, ttk
from GUI.common.app_theme import AppTheme

class ReadingView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.controller = None
        self.reading_stats = {
            "word_count": StringVar(value="0"),
            "unique_words": StringVar(value="0"),
            "reading_level": StringVar(value="N/A")
        }
        
        self._create_toolbar()
        self._create_content_area()
    
    def set_controller(self, controller):
        """Binds view with its controller"""
        self.controller = controller
        
        self.import_button.config(command=self._on_import)
        self.clear_button.config(command=self._on_clear)
        self.analyze_button.config(command=self._on_analyze)
        self.add_all_button.config(command=self._on_add_all)
        
        self.reading_text.bind("<Button-3>", self._on_text_right_click)
    
    def _create_toolbar(self):
        """Create the toolbar with buttons"""
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        self.import_button = ttk.Button(toolbar, text="Import Text")
        self.import_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(toolbar, text="Clear")
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = ttk.Button(toolbar, text="Analyze Text", style="Accent.TButton")
        self.analyze_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_content_area(self):
        """Create reading area and sidebar"""
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        reading_frame = ttk.Frame(content_frame)
        reading_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.reading_text = Text(
            reading_frame,
            wrap=tk.WORD,
            font=AppTheme.BODY_FONT,
            background="white",
            foreground=AppTheme.TEXT_DARK,
            insertbackground=AppTheme.PRIMARY,
            padx=10,
            pady=10
        )
        self.reading_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure tags for highlighting
        self.reading_text.tag_configure("highlight", background="#FFEB3B")
        self.reading_text.tag_configure("unknown", background="#ffcdd2")
        self.reading_text.tag_configure("known", background="#c8e6c9")
        self.reading_text.tag_configure("learning", background="#bbdefb")
        
        reading_scrollbar = ttk.Scrollbar(reading_frame, orient="vertical", command=self.reading_text.yview)
        reading_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reading_text.config(yscrollcommand=reading_scrollbar.set)
        
        # Sidebar (right side)
        sidebar = ttk.Frame(content_frame, width=250)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        sidebar.pack_propagate(False)  # Prevent shrinking
        
        # Statistics section
        stats_frame = ttk.LabelFrame(sidebar, text="Reading Statistics")
        stats_frame.pack(fill=tk.X, pady=5)
        
        stats_content = ttk.Frame(stats_frame)
        stats_content.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(stats_content, text="Words:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_content, textvariable=self.reading_stats["word_count"]).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(stats_content, text="Unique Words:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(stats_content, textvariable=self.reading_stats["unique_words"]).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(stats_content, text="Reading Level:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(stats_content, textvariable=self.reading_stats["reading_level"]).grid(row=2, column=1, sticky=tk.W)
        
        # Unknown words section
        unknown_frame = ttk.LabelFrame(sidebar, text="Unknown Words")
        unknown_frame.pack(fill=tk.X, pady=10, expand=True)
        
        self.unknown_listbox = tk.Listbox(unknown_frame, height=10)
        self.unknown_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind double-click on unknown words
        self.unknown_listbox.bind("<Double-Button-1>", self._on_unknown_word_double_click)
        
        self.add_all_button = ttk.Button(unknown_frame, text="Add All to Vocabulary")
        self.add_all_button.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def get_text(self):
        """Get the current text content"""
        return self.reading_text.get("1.0", "end-1c")
    
    def set_text(self, text):
        """Set the text content"""
        self.reading_text.delete("1.0", tk.END)
        self.reading_text.insert("1.0", text)
    
    def update_statistics(self, stats):
        """Update the reading statistics"""
        self.reading_stats["word_count"].set(str(stats.get("word_count", 0)))
        self.reading_stats["unique_words"].set(str(stats.get("unique_words", 0)))
        self.reading_stats["reading_level"].set(stats.get("reading_level", "N/A"))
    
    def update_unknown_words(self, words):
        """Update the unknown words list"""
        self.unknown_listbox.delete(0, tk.END)
        for word in words:
            self.unknown_listbox.insert(tk.END, word)
    
    def highlight_word(self, word, tag="highlight"):
        """Highlight all occurrences of a word"""
        content = self.reading_text.get("1.0", tk.END)
        
        self.reading_text.tag_remove(tag, "1.0", tk.END)
        
        start_idx = "1.0"
        while True:
            start_idx = self.reading_text.search(
                word, start_idx, tk.END, 
                nocase=True, 
                regexp=False
            )
            
            if not start_idx:
                break
            
            end_idx = f"{start_idx}+{len(word)}c"
            self.reading_text.tag_add(tag, start_idx, end_idx)
            start_idx = end_idx
    
    def clear_highlights(self, tag=None):
        """Clear all or specific highlights"""
        if tag:
            self.reading_text.tag_remove(tag, "1.0", tk.END)
        else:
            for tag_name in ["highlight", "unknown", "known", "learning"]:
                self.reading_text.tag_remove(tag_name, "1.0", tk.END)
    
    def _on_import(self):
        """Handle import button click"""
        if self.controller:
            self.controller.import_text()
    
    def _on_clear(self):
        """Handle clear button click"""
        if self.controller:
            self.controller.clear_text()
    
    def _on_analyze(self):
        """Handle analyze button click"""
        if self.controller:
            self.controller.analyze_text()
    
    def _on_add_all(self):
        """Handle add all button click"""
        if self.controller:
            self.controller.add_all_unknown_words()
    
    def _on_text_right_click(self, event):
        """Handle right-click on text area"""
        if self.controller:
            index = self.reading_text.index(f"@{event.x},{event.y}")
            
            self.controller.on_text_right_click(index, event.x_root, event.y_root)
    
    def _on_unknown_word_double_click(self, event):
        """Handle double-click on an unknown word"""
        if self.controller and self.unknown_listbox.curselection():
            index = self.unknown_listbox.curselection()[0]
            word = self.unknown_listbox.get(index)
            self.controller.on_unknown_word_selected(word)
    
    def show_context_menu(self, x, y, word, commands):
        """Show a context menu for a word"""
        menu = tk.Menu(self, tearoff=0)
        
        menu.add_command(label=f"Look up '{word}'", command=commands.get("lookup", lambda: None))
        menu.add_command(label=f"Add '{word}' to vocabulary", command=commands.get("add", lambda: None))
        menu.add_separator()
        menu.add_command(label="Highlight all occurrences", command=commands.get("highlight", lambda: None))
        
        menu.post(x, y)