from util.services.online_service import WiktionaryService, TatoebaService
import threading
import re

class WordDataService:
    def __init__(self):
        self.wiktionary_service = WiktionaryService()
        self.tatoeba_service = TatoebaService()
    
    def fetch_word_data_async(self, word, source_lang="English", callback=None):
        thread = threading.Thread(
            target=self._fetch_data_thread,
            args=(word, source_lang, callback),
            daemon=True
        )
        thread.start()
        return thread
    
    def _fetch_data_thread(self, word, source_lang, callback):
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
        result = {
            "word": word,
            "definitions_by_pos": {},
            "etymology": raw_data.get("etymology", ""),
            "pronunciation": raw_data.get("pronunciation", ""),
            "related_words": {"synonyms": [], "antonyms": []}
        }
        
        definitions = raw_data.get("definitions", [])
        if definitions:
            result["definitions_by_pos"] = {"noun": definitions}
        
        wiktionary_examples = raw_data.get("examples", [])
        
        if len(wiktionary_examples) < 3:
            tatoeba_examples = self.fetch_example_sentences(word, limit=5-len(wiktionary_examples))
            result["examples"] = wiktionary_examples + tatoeba_examples
        else:
            result["examples"] = wiktionary_examples[:5] 
        
        related_terms = raw_data.get("related_terms", [])
        if isinstance(related_terms, list) and related_terms:
            mid = len(related_terms) // 2
            result["related_words"]["synonyms"] = related_terms[:mid]
            result["related_words"]["antonyms"] = related_terms[mid:]
        
        if "error" in raw_data:
            result["error"] = raw_data["error"]
            
        return result

    def speak(self, word, lang_code="en"):
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
                speaker.Speak(word)
                return None
            except Exception as e:
                return e

    def fetch_example_sentences(self, word, limit=5, min_length=6, max_length=100):
        lang_map = {"English": "eng", "Spanish": "spa", "French": "fra", "German": "deu"}
        source_lang = lang_map.get("English", "eng")
        
        response = self.tatoeba_service.search_sentences(
            word=word,
            source_lang=source_lang,
            limit=limit
        )
        
        examples = []
        sentences = []
        
        if isinstance(response, dict) and "results" in response:
            sentences = response["results"]
        elif isinstance(response, list):
            sentences = response
            
        for item in sentences:
            if isinstance(item, dict) and "text" in item:
                sentence = item["text"].strip()
                if min_length <= len(sentence) <= max_length:
                    word_pattern = rf'\b{re.escape(word)}\b'
                    highlighted = re.sub(word_pattern, f"*{word}*", sentence, flags=re.IGNORECASE)
                    examples.append(highlighted)
        
        return examples[:limit]