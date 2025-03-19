import threading
from util.services.wiktionary_service import WiktionaryService

class WordInfoModel:
    """Manages the data for a word information window"""
    def __init__(self, word, source_lang="English"):
        self.word = word
        self.source_lang = source_lang
        self.definitions_by_pos = {}
        self.etymology = ""
        self.examples = []
        self.pronunciation = ""
        self.related_words = {"synonyms": [], "antonyms": []}
        self.loading = True
        self.error = None
        
        self.wiktionary_service = WiktionaryService()
    
    def fetch_data(self, callback=None):
        """Fetch word data asynchronously"""
        thread = threading.Thread(
            target=self._fetch_data_thread,
            args=(callback,),
            daemon=True
        )
        thread.start()
        return thread
    
    def _fetch_data_thread(self, callback):
        """Background thread to fetch word data"""
        try:
            word_data = self.wiktionary_service.get_word_data(self.word, self.source_lang)
            
            if "error" in word_data:
                self.error = word_data["error"]
            else:
                self._process_definitions(word_data.get("definitions", []))
                
                self.etymology = word_data.get("etymology", "")
                self.examples = word_data.get("examples", [])
                self.pronunciation = word_data.get("pronunciation", "")
                
                if "related_terms" in word_data:
                    self._process_related_terms(word_data["related_terms"])
        except Exception as e:
            self.error = f"Error retrieving word data: {str(e)}"
        finally:
            self.loading = False
            if callback:
                callback()
    
    def _process_definitions(self, definitions):
        """Process raw definitions into organized structure"""
        # TODO - remove placeholder and add real processing
        self.definitions_by_pos = {"noun": definitions}
    
    def _process_related_terms(self, related_terms):
        """Extract related terms into synonyms/antonyms"""
        # TODO - remove placeholder and add real processing
        if isinstance(related_terms, list) and related_terms:
            mid = len(related_terms) // 2
            self.related_words["synonyms"] = related_terms[:mid]
            self.related_words["antonyms"] = related_terms[mid:]

    def save_word(self, word_db, word, source_lang):
        """Save word to database"""
        if not word_db:
            return False

        if word_db.word_exists(word):
            return None
        
        return word_db.save_word(word, source_lang)