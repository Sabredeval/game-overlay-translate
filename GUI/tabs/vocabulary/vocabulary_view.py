import tkinter as tk
from tkinter import StringVar, ttk
from GUI.common.app_theme import AppTheme

class VocabularyView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.controller = None
        self.view_type_var = StringVar(value="cards")
        
        self._create_collections_panel()
        self._create_word_display_panel()
    
    def set_controller(self, controller):
        """Binds view with its controller"""
        self.controller = controller
        
        # Connect event handlers
        self.collections_tree.bind("<<TreeviewSelect>>", self._on_collection_selected)
        self.new_collection_button.config(command=self._on_new_collection)
        self.edit_collection_button.config(command=self._on_edit_collection)
        self.delete_collection_button.config(command=self._on_delete_collection)
        self.study_button.config(command=self._on_study_selected)
        
        for rb in self.view_radio_buttons:
            rb.config(command=self._on_view_type_changed)
    
    def _create_collections_panel(self):
        """Create the collections panel on the left"""
        collections_frame = ttk.LabelFrame(self, text="Collections")
        collections_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.collections_tree = ttk.Treeview(collections_frame, height=20)
        self.collections_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        collection_buttons = ttk.Frame(collections_frame)
        collection_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        self.new_collection_button = ttk.Button(collection_buttons, text="New")
        self.new_collection_button.pack(side=tk.LEFT, padx=2)
        
        self.edit_collection_button = ttk.Button(collection_buttons, text="Edit")
        self.edit_collection_button.pack(side=tk.LEFT, padx=2)
        
        self.delete_collection_button = ttk.Button(collection_buttons, text="Delete")
        self.delete_collection_button.pack(side=tk.LEFT, padx=2)
    
    def _create_word_display_panel(self):
        """Create the word cards/list panel on the right"""
        self.cards_frame = ttk.Frame(self)
        self.cards_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        vocab_toolbar = ttk.Frame(self.cards_frame)
        vocab_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(vocab_toolbar, text="View:").pack(side=tk.LEFT, padx=5)
        
        self.view_radio_buttons = []
        rb_cards = ttk.Radiobutton(
            vocab_toolbar, 
            text="Cards", 
            variable=self.view_type_var, 
            value="cards"
        )
        rb_cards.pack(side=tk.LEFT, padx=5)
        self.view_radio_buttons.append(rb_cards)
        
        rb_list = ttk.Radiobutton(
            vocab_toolbar, 
            text="List", 
            variable=self.view_type_var, 
            value="list"
        )
        rb_list.pack(side=tk.LEFT, padx=5)
        self.view_radio_buttons.append(rb_list)
        
        # Study button
        self.study_button = ttk.Button(
            vocab_toolbar, 
            text="Study Selected", 
            style="Accent.TButton"
        )
        self.study_button.pack(side=tk.RIGHT, padx=5)
        
        self.cards_container = ttk.Frame(self.cards_frame)
        self.cards_container.pack(fill=tk.BOTH, expand=True)
        
        for i in range(3):
            self.cards_container.rowconfigure(i, weight=1)
        for i in range(4):
            self.cards_container.columnconfigure(i, weight=1)

        self.list_container = ttk.Frame(self.cards_frame)
        
        list_columns = ("word", "definition", "mastery")
        self.word_list = ttk.Treeview(
            self.list_container, 
            columns=list_columns,
            show="headings",
            selectmode="extended"
        )
        self.word_list.heading("word", text="Word")
        self.word_list.heading("definition", text="Definition")
        self.word_list.heading("mastery", text="Mastery")
        
        self.word_list.column("word", width=100)
        self.word_list.column("definition", width=300)
        self.word_list.column("mastery", width=80)
        
        self.word_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        list_scrollbar = ttk.Scrollbar(
            self.list_container, 
            orient="vertical", 
            command=self.word_list.yview
        )
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.word_list.config(yscrollcommand=list_scrollbar.set)
    
    def populate_collections(self, collections_data):
        """Populate the collections tree with data"""
        for item in self.collections_tree.get_children():
            self.collections_tree.delete(item)
        
        for collection in collections_data:
            if 'parent_id' in collection and collection['parent_id']:
                self.collections_tree.insert(
                    collection['parent_id'], 
                    "end", 
                    text=collection['name'],
                    iid=collection['id'],
                    open=collection.get('open', False)
                )
            else:
                self.collections_tree.insert(
                    "", 
                    "end", 
                    text=collection['name'],
                    iid=collection['id'],
                    open=collection.get('open', False)
                )
    
    def display_words_as_cards(self, words_data):
        """Display words as cards"""
        self.list_container.pack_forget()
        self.cards_container.pack(fill=tk.BOTH, expand=True)
        
        for widget in self.cards_container.winfo_children():
            widget.destroy()
        
        for i, word_data in enumerate(words_data):
            row, col = i // 4, i % 4
            
            card_frame = ttk.Frame(self.cards_container, borderwidth=1, relief="solid")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            word_label = ttk.Label(
                card_frame, 
                text=word_data['word'], 
                font=AppTheme.HEADING_FONT
            )
            word_label.pack(pady=(10, 5))
            
            def_label = ttk.Label(
                card_frame, 
                text=word_data['definition'][:50] + ('...' if len(word_data['definition']) > 50 else '')
            )
            def_label.pack(pady=5)
            
            mastery_label = ttk.Label(
                card_frame, 
                text=self._get_star_rating(word_data['mastery']),
                foreground=AppTheme.ACCENT
            )
            mastery_label.pack(pady=5)
            
            card_frame.word_id = word_data['id']
            
            card_frame.bind("<Button-1>", lambda e, id=word_data['id']: self._on_card_click(id))
    
    def display_words_as_list(self, words_data):
        """Display words as a list"""
        self.cards_container.pack_forget()
        self.list_container.pack(fill=tk.BOTH, expand=True)
        
        for item in self.word_list.get_children():
            self.word_list.delete(item)

        for word_data in words_data:
            self.word_list.insert(
                "",
                "end",
                values=(
                    word_data['word'],
                    word_data['definition'][:50] + ('...' if len(word_data['definition']) > 50 else ''),
                    self._get_star_rating(word_data['mastery'])
                ),
                tags=(str(word_data['id']),)
            )
    
    def _get_star_rating(self, mastery_level):
        """Convert mastery level (0-5) to stars"""
        return "★" * mastery_level + "☆" * (5 - mastery_level)
    
    def get_selected_collection_id(self):
        """Get the ID of the selected collection"""
        selection = self.collections_tree.selection()
        if selection:
            return selection[0]
        return None
    
    def get_selected_word_ids(self):
        """Get IDs of selected words"""
        if self.view_type_var.get() == "cards":
            # In cards view, we'd need to track selected cards
            # For simplicity, let's assume we store selected card IDs in a list
            return self.selected_card_ids if hasattr(self, 'selected_card_ids') else []
        else:
            # In list view, get selected items from treeview
            selection = self.word_list.selection()
            return [self.word_list.item(item, "tags")[0] for item in selection]
    
    def _on_collection_selected(self, event):
        """Handle collection selection"""
        if self.controller:
            collection_id = self.get_selected_collection_id()
            if collection_id:
                self.controller.load_collection_words(collection_id)
    
    def _on_new_collection(self):
        """Handle new collection button"""
        if self.controller:
            self.controller.create_new_collection()
    
    def _on_edit_collection(self):
        """Handle edit collection button"""
        if self.controller:
            collection_id = self.get_selected_collection_id()
            if collection_id:
                self.controller.edit_collection(collection_id)
    
    def _on_delete_collection(self):
        """Handle delete collection button"""
        if self.controller:
            collection_id = self.get_selected_collection_id()
            if collection_id:
                self.controller.delete_collection(collection_id)
    
    def _on_study_selected(self):
        """Handle study selected button"""
        if self.controller:
            word_ids = self.get_selected_word_ids()
            if word_ids:
                self.controller.start_study_session(word_ids)
    
    def _on_view_type_changed(self):
        """Handle view type change"""
        if self.controller:
            view_type = self.view_type_var.get()
            self.controller.change_view_type(view_type)
    
    def _on_card_click(self, word_id):
        """Handle click on a word card"""
        if self.controller:
            self.controller.select_word(word_id)