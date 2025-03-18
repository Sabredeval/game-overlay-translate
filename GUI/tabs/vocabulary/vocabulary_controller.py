import tkinter as tk
from tkinter import simpledialog, messagebox

class VocabularyController:
    def __init__(self, view, db_manager):
        """
        Initialize the vocabulary controller
        
        Args:
            view: The vocabulary tab view
            db_manager: Database manager for vocabulary operations
        """
        self.view = view
        self.view.set_controller(self)
        self.db_manager = db_manager
        self.current_collection_id = None
        self.selected_word_ids = set()
        
        # Initial view type
        self.current_view_type = "cards"
        
        # Load collections on startup
        self.load_collections()
    
    def load_collections(self):
        """Load all collections from database"""
        # This would fetch real data from your database
        # For now, we'll use sample data
        collections = [
            {'id': 'recent', 'name': 'Recently Added', 'open': True},
            {'id': 'favorites', 'name': 'Favorites'},
            {'id': 'themes', 'name': 'By Theme'},
            {'id': 'themes.travel', 'name': 'Travel', 'parent_id': 'themes'},
            {'id': 'themes.academic', 'name': 'Academic', 'parent_id': 'themes'},
            {'id': 'levels', 'name': 'By Level'},
            {'id': 'levels.beginner', 'name': 'Beginner', 'parent_id': 'levels'},
            {'id': 'levels.intermediate', 'name': 'Intermediate', 'parent_id': 'levels'},
            {'id': 'levels.advanced', 'name': 'Advanced', 'parent_id': 'levels'}
        ]
        
        self.view.populate_collections(collections)
    
    def load_collection_words(self, collection_id):
        """Load words for a specific collection"""
        self.current_collection_id = collection_id
        
        # This would fetch real data from your database
        # For now, we'll use sample data
        words_data = []
        for i in range(1, 13):
            words_data.append({
                'id': f"{collection_id}.{i}",
                'word': f"Word {i}",
                'definition': f"This is a definition for word {i} in collection {collection_id}.",
                'mastery': i % 6  # 0-5 mastery level
            })
        
        if self.current_view_type == "cards":
            self.view.display_words_as_cards(words_data)
        else:
            self.view.display_words_as_list(words_data)
    
    def change_view_type(self, view_type):
        """Change between cards and list view"""
        if view_type != self.current_view_type:
            self.current_view_type = view_type
            
            if self.current_collection_id:
                self.load_collection_words(self.current_collection_id)
    
    def create_new_collection(self):
        """Create a new word collection"""
        collection_name = simpledialog.askstring(
            "New Collection", 
            "Enter collection name:",
            parent=self.view
        )
        
        if collection_name:
            # This would save to your database
            # For demo, we'll just refresh the collections
            messagebox.showinfo(
                "Collection Created",
                f"Collection '{collection_name}' created successfully!"
            )
            self.load_collections()
    
    def edit_collection(self, collection_id):
        """Edit a collection name"""
        # Get current name
        for item_id in self.view.collections_tree.get_children():
            if item_id == collection_id:
                current_name = self.view.collections_tree.item(item_id, 'text')
                break
        else:
            current_name = ""
        
        new_name = simpledialog.askstring(
            "Edit Collection", 
            "Enter new collection name:",
            initialvalue=current_name,
            parent=self.view
        )
        
        if new_name:
            # This would update your database
            # For demo, we'll just show a message
            messagebox.showinfo(
                "Collection Updated",
                f"Collection renamed to '{new_name}'"
            )
    
    def delete_collection(self, collection_id):
        """Delete a collection"""
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this collection?",
            parent=self.view
        )
        
        if confirm:
            # This would delete from your database
            # For demo, we'll just refresh the collections
            self.load_collections()
    
    def select_word(self, word_id):
        """Select a word (toggle selection)"""
        if word_id in self.selected_word_ids:
            self.selected_word_ids.remove(word_id)
        else:
            self.selected_word_ids.add(word_id)
    
    def start_study_session(self, word_ids):
        """Start a study session with selected words"""
        if not word_ids:
            messagebox.showinfo(
                "No Words Selected",
                "Please select words to study",
                parent=self.view
            )
            return
        
        # This would launch your study session interface
        messagebox.showinfo(
            "Study Session",
            f"Starting study session with {len(word_ids)} words",
            parent=self.view
        )