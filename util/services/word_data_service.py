from util.services.wiktionary_service import WiktionaryService
import threading

class WordDataService:
    """Central service for fetching and processing word data"""
    
    def __init__(self):
        self.wiktionary_service = WiktionaryService()
    
    def fetch_word_data_async(self, word, source_lang="English", callback=None):
        """Fetch word data asynchronously and execute callback when done"""
        thread = threading.Thread(
            target=self._fetch_data_thread,
            args=(word, source_lang, callback),
            daemon=True
        )
        thread.start()
        return thread
    
    def _fetch_data_thread(self, word, source_lang, callback):
        """Background thread to fetch word data"""
        try:
            word_data = self.wiktionary_service.get_word_data(word, source_lang)
            processed_data = self._process_word_data(word, word_data)
            
            if callback:
                callback(processed_data)
                
        except Exception as e:
            error_data = {
                "word": word,
                "error": f"Error retrieving data: {str(e)}",
                "definitions_by_pos": {},
                "examples": [],
                "etymology": "",
                "pronunciation": "",
                "related_words": {"synonyms": [], "antonyms": []}
            }
            if callback:
                callback(error_data)
    
    def _process_word_data(self, word, raw_data):
        """Process and structure raw word data from Wiktionary"""
        result = {
            "word": word,
            "definitions_by_pos": {},
            "examples": raw_data.get("examples", []),
            "etymology": raw_data.get("etymology", ""),
            "pronunciation": raw_data.get("pronunciation", ""),
            "related_words": {"synonyms": [], "antonyms": []}
        }
        
        # TODO - Fill with real data
        definitions = raw_data.get("definitions", [])
        if definitions:
            result["definitions_by_pos"] = {"noun": definitions}
        
        related_terms = raw_data.get("related_terms", [])
        if isinstance(related_terms, list) and related_terms:
            mid = len(related_terms) // 2
            result["related_words"]["synonyms"] = related_terms[:mid]
            result["related_words"]["antonyms"] = related_terms[mid:]
        
        if "error" in raw_data:
            result["error"] = raw_data["error"]
            
        return result
        
    def get_word_data_sync(self, word, source_lang="English"):
        """Get word data synchronously (blocking)"""
        raw_data = self.wiktionary_service.get_word_data(word, source_lang)
        return self._process_word_data(word, raw_data)
    
    def speak(self, word, lang_code="en"):
        """Play pronunciation of the word"""
        try:
            from gtts import gTTS
            import os
            import tempfile
            from playsound import playsound
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            tts = gTTS(text=word, lang=lang_code)
            tts.save(temp_file.name)
            
            playsound(temp_file.name)
                
            os.unlink(temp_file.name)
            return None
        except Exception as e:
            try:
                # If no internet connection, use Windows TTS
                import win32com.client
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(self.word)
                return None
            except Exception as e:
                return e
    