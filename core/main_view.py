import tkinter as tk
from tkinter import Text, StringVar, ttk
from common.app_theme import IconManager, AppTheme, ToolTip


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pymage - Language Learning Assistant")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        AppTheme.configure_styles()
        
        self.icon_manager = IconManager()
        
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Controls
        self.grid_rowconfigure(2, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)
        
        self.native_language_var = StringVar(self)
        self.translated_language_var = StringVar(self)
        self.search_var = StringVar(self)
        self.search_var.trace("w", self._on_search_changed)
        
        self._create_header()
        self._create_language_dropdowns()
        self._create_buttons()
        self._create_notebook()
        
        self._create_status_bar()
        
    def _create_header(self):
        header = ttk.Frame(self, style='Header.TFrame')
        header.grid(row=0, column=0, sticky="ew")
        header.configure(height=50)
        
        logo_frame = ttk.Frame(header, style='Header.TFrame')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        app_name = ttk.Label(logo_frame, text="Pymage", style='Header.TLabel', font=("Segoe UI", 16, "bold"))
        app_name.pack(side=tk.LEFT)
        
        app_subtitle = ttk.Label(logo_frame, text="Language Learning Assistant", 
                               style='Header.TLabel', font=("Segoe UI", 10))
        app_subtitle.pack(side=tk.LEFT, padx=10)
        
    def _create_language_dropdowns(self):
        """Create language selection area"""
        dropdown_container = ttk.Frame(self)
        dropdown_container.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        
        dropdown_frame = ttk.LabelFrame(dropdown_container, text="Language Selection")
        dropdown_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        native_frame = ttk.Frame(dropdown_frame)
        native_frame.pack(side=tk.LEFT, padx=20, pady=10)
        native_label = ttk.Label(native_frame, text="Native Language:")
        native_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.native_dropdown = ttk.Combobox(native_frame, textvariable=self.native_language_var, state="readonly", width=15)
        self.native_dropdown.pack(side=tk.TOP, pady=5)
        
        translated_frame = ttk.Frame(dropdown_frame)
        translated_frame.pack(side=tk.LEFT, padx=20, pady=10)
        translated_label = ttk.Label(translated_frame, text="Learning Language:")
        translated_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.translated_dropdown = ttk.Combobox(translated_frame, textvariable=self.translated_language_var, state="readonly", width=15)
        self.translated_dropdown.pack(side=tk.TOP, pady=5)
        
        search_frame = ttk.Frame(dropdown_frame)
        search_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.TOP, anchor=tk.W)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.TOP, pady=5, fill=tk.X)
        
        return dropdown_frame
        
    def _create_buttons(self):
        button_container = ttk.Frame(self)
        button_container.grid(row=1, column=0, pady=0, padx=10, sticky="ew")
        
        button_frame = ttk.LabelFrame(button_container, text="Tools")
        button_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        toolbar = ttk.Frame(button_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        start_selection_button = ttk.Button(toolbar, text="Select Text", style="Accent.TButton")
        start_selection_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(start_selection_button, "Capture text from screen (Ctrl+E)")
        
        save_word_button = ttk.Button(toolbar, text="Save Word")
        save_word_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(save_word_button, "Save selected word (Ctrl+S)")
        
        separator = ttk.Separator(toolbar, orient="vertical")
        separator.pack(side=tk.LEFT, padx=10, fill="y")
        
        saved_words_button = ttk.Button(toolbar, text="Saved Words")
        saved_words_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(saved_words_button, "View saved words")
        
        browse_words_button = ttk.Button(toolbar, text="Browse Words")
        browse_words_button.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(browse_words_button, "Browse dictionary")
        
        settings_button = ttk.Button(toolbar, text="Settings")
        settings_button.pack(side=tk.RIGHT, padx=5, pady=5)
        ToolTip(settings_button, "Application settings")
        
        return button_frame
    
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # 1. Dictionary & Lookup Tab
        self.dictionary_tab = self._create_dictionary_tab()
        self.notebook.add(self.dictionary_tab, text="Dictionary")
        
        # 2. Reading Assistant Tab
        self.reading_tab = self._create_reading_assistant_tab()
        self.notebook.add(self.reading_tab, text="Reading Assistant")
        
        # 3. Vocabulary Builder Tab
        self.vocab_tab = self._create_vocabulary_builder_tab()
        self.notebook.add(self.vocab_tab, text="Vocabulary Builder")
        
        # 4. Word Explorer Tab
        self.explorer_tab = self._create_word_explorer_tab()
        self.notebook.add(self.explorer_tab, text="Word Explorer")
        
        # 5. Study Dashboard Tab
        self.dashboard_tab = self._create_study_dashboard_tab()
        self.notebook.add(self.dashboard_tab, text="Study Dashboard")
    
    def _create_dictionary_tab(self):
        tab = ttk.Frame(self.notebook)
        
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_label = ttk.Label(search_frame, text="Lookup Word:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.dict_search_var = StringVar()
        self.dict_search_var.trace("w", self._on_dict_search_changed)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.dict_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        search_button = ttk.Button(search_frame, text="Look Up", command=self._perform_dictionary_search)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # TODO - implement _on_suggestion_selected
        suggestion_frame = ttk.Frame(tab)
        suggestion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.suggestion_listbox = tk.Listbox(suggestion_frame, height=5)
        self.suggestion_listbox.pack(fill=tk.X)
        self.suggestion_listbox.bind("<<ListboxSelect>>", self._on_suggestion_selected)
        
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.dict_notebook = ttk.Notebook(left_frame)
        self.dict_notebook.pack(fill=tk.BOTH, expand=True)
        
        self.definition_tab, self.definition_text = self._create_text_widget_tab(
            self.dict_notebook, "Definition"
        )
        self.examples_tab, self.examples_text = self._create_text_widget_tab(
            self.dict_notebook, "Examples"
        )
        self.etymology_tab, self.etymology_text = self._create_text_widget_tab(
            self.dict_notebook, "Etymology"
        )
        
        right_frame = ttk.Frame(content_frame, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)  # Prevent shrinking
        
        related_label = ttk.Label(right_frame, text="Related Words", font=AppTheme.HEADING_FONT)
        related_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.related_listbox = tk.Listbox(right_frame, height=10)
        self.related_listbox.pack(fill=tk.X, pady=5)
        
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        save_button = ttk.Button(action_frame, text="Save to Vocabulary")
        save_button.pack(fill=tk.X, pady=2)
        
        pronunciation_button = ttk.Button(action_frame, text="Pronunciation")
        pronunciation_button.pack(fill=tk.X, pady=2)
        
        browser_button = ttk.Button(action_frame, text="Open in Browser")
        browser_button.pack(fill=tk.X, pady=2)
        
        return tab
    
    def _create_reading_assistant_tab(self):
        tab = ttk.Frame(self.notebook)
        
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        import_button = ttk.Button(toolbar, text="Import Text")
        import_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(toolbar, text="Clear")
        clear_button.pack(side=tk.LEFT, padx=5)
        
        analyze_button = ttk.Button(toolbar, text="Analyze Text", style="Accent.TButton")
        analyze_button.pack(side=tk.RIGHT, padx=5)
        
        content_frame = ttk.Frame(tab)
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
        
        reading_scrollbar = ttk.Scrollbar(reading_frame, orient="vertical", command=self.reading_text.yview)
        reading_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.reading_text.config(yscrollcommand=reading_scrollbar.set)
        
        sidebar = ttk.Frame(content_frame, width=250)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        sidebar.pack_propagate(False)  # Prevent shrinking
        
        stats_frame = ttk.LabelFrame(sidebar, text="Reading Statistics")
        stats_frame.pack(fill=tk.X, pady=5)
        
        stats_content = ttk.Frame(stats_frame)
        stats_content.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(stats_content, text="Words:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_content, text="0").grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(stats_content, text="Unique Words:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(stats_content, text="0").grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(stats_content, text="Reading Level:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(stats_content, text="N/A").grid(row=2, column=1, sticky=tk.W)
        
        unknown_frame = ttk.LabelFrame(sidebar, text="Unknown Words")
        unknown_frame.pack(fill=tk.X, pady=10, expand=True)
        
        self.unknown_listbox = tk.Listbox(unknown_frame, height=10)
        self.unknown_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        add_all_button = ttk.Button(unknown_frame, text="Add All to Vocabulary")
        add_all_button.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        return tab
    
    def _create_vocabulary_builder_tab(self):
        """Create the vocabulary builder tab"""
        tab = ttk.Frame(self.notebook)
        
        collections_frame = ttk.LabelFrame(tab, text="Collections")
        collections_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.collections_tree = ttk.Treeview(collections_frame, height=20)
        self.collections_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TODO - Add actual collections import from database
        self.collections_tree.insert("", "end", text="Recently Added", iid="recent", open=True)
        self.collections_tree.insert("", "end", text="Favorites", iid="favorites")
        self.collections_tree.insert("", "end", text="By Theme", iid="themes")
        self.collections_tree.insert("themes", "end", text="Travel")
        self.collections_tree.insert("themes", "end", text="Academic")
        self.collections_tree.insert("", "end", text="By Level", iid="levels")
        self.collections_tree.insert("levels", "end", text="Beginner")
        self.collections_tree.insert("levels", "end", text="Intermediate")
        self.collections_tree.insert("levels", "end", text="Advanced")
        
        collection_buttons = ttk.Frame(collections_frame)
        collection_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(collection_buttons, text="New").pack(side=tk.LEFT, padx=2)
        ttk.Button(collection_buttons, text="Edit").pack(side=tk.LEFT, padx=2)
        ttk.Button(collection_buttons, text="Delete").pack(side=tk.LEFT, padx=2)
        
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        vocab_toolbar = ttk.Frame(cards_frame)
        vocab_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(vocab_toolbar, text="View:").pack(side=tk.LEFT, padx=5)
        
        view_var = StringVar(value="cards")
        ttk.Radiobutton(vocab_toolbar, text="Cards", variable=view_var, value="cards").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(vocab_toolbar, text="List", variable=view_var, value="list").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(vocab_toolbar, text="Study Selected", style="Accent.TButton").pack(side=tk.RIGHT, padx=5)
        
        cards_container = ttk.Frame(cards_frame)
        cards_container.pack(fill=tk.BOTH, expand=True)
        
        # TODO - import actual cards from database
        for i in range(12):
            row, col = i // 4, i % 4
            card_frame = ttk.Frame(cards_container, borderwidth=1, relief="solid")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ttk.Label(card_frame, text=f"Word {i+1}", font=AppTheme.HEADING_FONT).pack(pady=(10, 5))
            ttk.Label(card_frame, text="Definition goes here").pack(pady=5)
            ttk.Label(card_frame, text="★★★☆☆", foreground=AppTheme.ACCENT).pack(pady=5)
        
        for i in range(3):
            cards_container.rowconfigure(i, weight=1)
        for i in range(4):
            cards_container.columnconfigure(i, weight=1)
        
        return tab
    
    def _create_word_explorer_tab(self):
        """Create the word explorer tab"""
        tab = ttk.Frame(self.notebook)
        
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Explore Word:").pack(side=tk.LEFT, padx=5)
        
        self.explorer_search_var = StringVar()
        explorer_entry = ttk.Entry(search_frame, textvariable=self.explorer_search_var, width=30)
        explorer_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        explore_button = ttk.Button(search_frame, text="Explore", style="Accent.TButton")
        explore_button.pack(side=tk.LEFT, padx=5)
        
        options_frame = ttk.Frame(tab)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="View:").pack(side=tk.LEFT, padx=5)
        
        view_options = ["Word Network", "Etymology Tree", "Word Family", "Semantic Field"]
        view_var = StringVar(value=view_options[0])
        view_dropdown = ttk.Combobox(options_frame, textvariable=view_var, values=view_options, state="readonly", width=15)
        view_dropdown.pack(side=tk.LEFT, padx=5)
        
        viz_frame = ttk.LabelFrame(tab, text="Word Network")
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        viz_placeholder = ttk.Label(viz_frame, text="Enter a word above to explore its relationships", font=AppTheme.HEADING_FONT)
        viz_placeholder.pack(expand=True, pady=50)
        
        canvas = tk.Canvas(viz_frame, background="white")
        canvas.pack(fill=tk.BOTH, expand=True)
        
        return tab
    
    def _create_study_dashboard_tab(self):
        """Create the study dashboard tab"""
        tab = ttk.Frame(self.notebook)
        
        summary_frame = ttk.LabelFrame(tab, text="Learning Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_grid = ttk.Frame(summary_frame)
        stats_grid.pack(fill=tk.X, padx=20, pady=10)
        
        stats_data = [
            ("Total Words", "0"),
            ("Words to Learn", "0"),
            ("Learning Streak", "0 days"),
            ("Words Mastered", "0"),
            ("Review Due", "0"),
            ("Last Activity", "Never")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row, col = i // 3, i % 3
            
            stat_frame = ttk.Frame(stats_grid, padding=10)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            
            ttk.Label(stat_frame, text=label, font=AppTheme.SMALL_FONT).pack(anchor=tk.W)
            ttk.Label(stat_frame, text=value, font=AppTheme.HEADING_FONT).pack(anchor=tk.W)
        
        for i in range(2):
            stats_grid.rowconfigure(i, weight=1)
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
        
        charts_frame = ttk.Frame(tab)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TODO - Add a proper chart visualization
        progress_frame = ttk.LabelFrame(charts_frame, text="Learning Progress")
        progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        progress_canvas = tk.Canvas(progress_frame, background="white", height=200)
        progress_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TODO - Add a pie chart visualization
        categories_frame = ttk.LabelFrame(charts_frame, text="Word Categories")
        categories_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        categories_canvas = tk.Canvas(categories_frame, background="white", height=200)
        categories_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        recommendations_frame = ttk.LabelFrame(tab, text="Recommendations")
        recommendations_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for i in range(3):
            rec_frame = ttk.Frame(recommendations_frame, padding=10)
            rec_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            rec_title = ttk.Label(rec_frame, text=f"Recommendation {i+1}", font=AppTheme.HEADING_FONT)
            rec_title.pack(fill=tk.X)
            
            rec_desc = ttk.Label(rec_frame, text="Description of this recommendation goes here. It explains what to do next.", wraplength=200)
            rec_desc.pack(fill=tk.X, pady=5)
            
            rec_button = ttk.Button(rec_frame, text="Start Activity")
            rec_button.pack(pady=5)
        
        return tab

    def _create_text_widget_tab(self, notebook, name):
        """Create a tab with a scrollable text widget"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=name)
        
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

        text_widget.tag_configure("heading", font=AppTheme.HEADING_FONT)
        text_widget.tag_configure("subheading", font=("Segoe UI", 11, "bold"))
        text_widget.tag_configure("normal", font=AppTheme.BODY_FONT)
        text_widget.tag_configure("example", font=AppTheme.BODY_FONT, foreground="#0077CC")
        text_widget.tag_configure("highlight", background="#FFEB3B")
        
        return tab, text_widget
    
    def _create_status_bar(self):
        """Create status bar at the bottom of the window"""
        status_frame = ttk.Frame(self, relief="sunken", style='TFrame')
        status_frame.grid(row=3, column=0, sticky="ew")
        
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W, padding=(5, 2))
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        version_label = ttk.Label(status_frame, text="v0.1.0", padding=(5, 2))
        version_label.pack(side=tk.RIGHT)
    
    def set_language_options(self, languages, native_default, translated_default):
        """Set language dropdown options"""
        self.native_language_var.set(native_default)
        self.translated_language_var.set(translated_default)
        
        self.native_dropdown['values'] = languages
        self.translated_dropdown['values'] = languages
    
    def create_buttons(self, commands):
        """Set button commands"""
        button_container = self.grid_slaves(row=1, column=0)[0]
        button_frame = button_container.winfo_children()[0]
        toolbar = button_frame.winfo_children()[0]
        
        buttons = [b for b in toolbar.winfo_children() if isinstance(b, ttk.Button)]
        
        # Order: Select Text, Save Word, [separator], Saved Words, Browse Words, Settings
        buttons[0].config(command=commands["start_selection"])
        buttons[1].config(command=commands["save_word"])
        buttons[2].config(command=commands["saved_words"])
        buttons[3].config(command=commands["browse_words"])
        buttons[4].config(command=commands["settings"])
    
    def _on_search_changed(self, *args):
        """Handle changes to the global search field"""
        search_text = self.search_var.get()
        if len(search_text) >= 3:
            self.show_status(f"Searching for: {search_text}")
    
    def _on_dict_search_changed(self, *args):
        """Handle changes to the dictionary search field"""
        search_text = self.dict_search_var.get()
        if len(search_text) >= 2:
            self._update_suggestions(["apple", "application", "apply", "appointment"])
    def _perform_dictionary_search(self):
        """Search for a word in the dictionary"""
        word = self.dict_search_var.get().strip()
        if word:
            self.show_status(f"Looking up: {word}")

    def display_word_info(self, word_data):
        """Display word information in the dictionary tab"""
        if not word_data:
            return
            
        self.definition_text.config(state=tk.NORMAL)
        self.definition_text.delete(1.0, tk.END)
        self.examples_text.config(state=tk.NORMAL)
        self.examples_text.delete(1.0, tk.END)
        self.etymology_text.config(state=tk.NORMAL)
        self.etymology_text.delete(1.0, tk.END)
        
        self.related_listbox.delete(0, tk.END)
        for word in word_data.get("related_words", {}).get("synonyms", []):
            self.related_listbox.insert(tk.END, word)
            
        self.definition_text.insert(tk.END, f"{word_data['word']}\n", "heading")
        if word_data.get("pronunciation"):
            self.definition_text.insert(tk.END, f"/{word_data['pronunciation']}/\n\n", "normal")
        else:
            self.definition_text.insert(tk.END, "\n", "normal")
            
        for pos, definitions in word_data.get("definitions_by_pos", {}).items():
            self.definition_text.insert(tk.END, f"{pos.capitalize()}\n", "subheading")
            for i, definition in enumerate(definitions, 1):
                self.definition_text.insert(tk.END, f"{i}. {definition}\n\n", "normal")
                
        if word_data.get("examples"):
            for example in word_data["examples"]:
                self.examples_text.insert(tk.END, f"• {example}\n\n", "example")
        if word_data.get("etymology"):
            self.etymology_text.insert(tk.END, "Etymology:\n", "subheading")
            self.etymology_text.insert(tk.END, f"{word_data['etymology']}\n", "normal")
            
        self.definition_text.config(state=tk.DISABLED)
        self.examples_text.config(state=tk.DISABLED)
        self.etymology_text.config(state=tk.DISABLED)

    def show_status(self, message):
        """Updates message in the status bar"""
        self.status_label.config(text=message)

    def _on_suggestion_selected(self, suggestion):
        pass

    def _update_suggestions(self, suggestion):
        pass
