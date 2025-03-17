class WordDatabaseController:
    """Controls word database operations"""
    def __init__(self, db):
        self.db = db
    
    def save_word(self, word, source_lang):
        """Save a word to the database"""
        if not word:
            return False
        
        if self.db.word_exists(word):
            return None
        
        return self.db.save_word(word, source_lang)