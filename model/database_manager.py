import sqlite3
import os

class WordDatabase:
    """Manages the SQLite database for saved words"""
    def __init__(self, db_path="saved_words.db"):
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER PRIMARY KEY,
            word TEXT UNIQUE,
            source_language TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            favorite BOOLEAN DEFAULT 0
        )
        ''')
        
        self.conn.commit()
    
    def save_word(self, word, source_lang):
        try:
            self.cursor.execute('''
            INSERT INTO saved_words (word, source_language)
            VALUES (?, ?)
            ''', (word, source_lang))
            
            word_id = self.cursor.lastrowid
            self.conn.commit()
            return word_id
        except sqlite3.IntegrityError:
            # Word already exists due to UNIQUE constraint
            return None
    
    def get_saved_words(self, limit=100, offset=0):
        self.cursor.execute('''
        SELECT * FROM saved_words
        ORDER BY date_added DESC
        LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        return self.cursor.fetchall()
    
    def search_words(self, query):
        query = f"%{query}%"
        self.cursor.execute('''
        SELECT * FROM saved_words
        WHERE word LIKE ?
        ORDER BY date_added DESC
        ''', (query,))
        
        return self.cursor.fetchall()
    
    def delete_word(self, word_id):
        self.cursor.execute('DELETE FROM saved_words WHERE id = ?', (word_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def toggle_favorite(self, word_id):
        self.cursor.execute('SELECT favorite FROM saved_words WHERE id = ?', (word_id,))
        result = self.cursor.fetchone()
        if not result:
            return False
            
        current_status = result[0]
        new_status = 0 if current_status else 1
        
        self.cursor.execute('UPDATE saved_words SET favorite = ? WHERE id = ?', (new_status, word_id))
        self.conn.commit()
        return new_status
    
    def get_favorites(self):
        self.cursor.execute('''
        SELECT * FROM saved_words
        WHERE favorite = 1
        ORDER BY date_added DESC
        ''')
        
        return self.cursor.fetchall()
    
    def word_exists(self, word):
        self.cursor.execute('SELECT id FROM saved_words WHERE word = ?', (word,))
        return self.cursor.fetchone() is not None
    
    def close(self):
        if self.conn:
            self.conn.close()