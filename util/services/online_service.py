import requests
import json
from bs4 import BeautifulSoup

class WiktionaryService:
    def __init__(self):
        self.base_url = "https://en.wiktionary.org/w/api.php"
        self.pos_tags = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", 
                        "Preposition", "Conjunction", "Interjection"]
        
    def get_word_data(self, word, language="English"):
        params = {
            "action": "parse",
            "page": word,
            "format": "json",
            "prop": "text",
            "formatversion": "2"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                return {"error": f"Word not found: {word}"}
            
            html_content = data["parse"]["text"]
            
            return self.parse_wiktionary_content(html_content, language)
            
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except KeyError as e:
            return {"error": f"Failed to parse response for word: {word} - {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
    
    def parse_wiktionary_content(self, html_content, target_language):
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {
            "definitions": [],
            "etymology": "",
            "pronunciation": "",
            "examples": [],
            "related_terms": [],
            "translations": {}
        }
        
        # Try to find the language section
        language_header = None
        for header in soup.find_all(['h2']):
            header_text = header.get_text().strip()
            if header_text == target_language:
                language_header = header
                break
        
        if not language_header:
            pass
        
        # Extract definitions usually ordered lists (ol)
        definition_lists = soup.find_all('ol')
        for ol in definition_lists:
            for li in ol.find_all('li', recursive=False):
                definition_text = li.get_text().strip()
                if definition_text and len(definition_text) > 1:
                    result["definitions"].append(definition_text)
                    
                    # Look for examples within this definition (often in italics or quotes)
                    examples = li.find_all(['dd', 'i', 'cite'])
                    for example in examples:
                        example_text = example.get_text().strip()
                        if example_text and len(example_text) > 12: 
                            result["examples"].append(example_text)
        
        etymology_section = soup.find(lambda tag: tag.name in ["h3", "h4"] and "Etymology" in tag.get_text())
        if etymology_section:
            next_elem = etymology_section.find_next(['p', 'div'])
            if next_elem:
                result["etymology"] = next_elem.get_text().strip()
        
        pron_section = soup.find(lambda tag: tag.name in ["h3", "h4"] and "Pronunciation" in tag.get_text())
        if pron_section:
            ipa_spans = soup.find_all('span', class_="IPA")
            if ipa_spans:
                pronunciations = [span.get_text() for span in ipa_spans]
                result["pronunciation"] = ", ".join(pronunciations)
            else:
                next_elem = pron_section.find_next(['p', 'div', 'ul'])
                if next_elem:
                    result["pronunciation"] = next_elem.get_text().strip()
        
        if not result["definitions"]:
            result["definitions"] = ["Definition parsing failed. Click 'Open in Browser' to see the full entry."]
        
        return result
    
    def search_similar_words(self, prefix, limit=10):
        params = {
            "action": "opensearch",
            "search": prefix,
            "limit": limit,
            "namespace": 0,
            "format": "json"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if len(data) >= 2:
                return data[1]
            return []
            
        except requests.RequestException:
            return []
        
class TatoebaService:
    def __init__(self):
        self.base_url = "https://tatoeba.org/eng/api_v0/"
        """search?from=eng&query=%3Dplay&to=eng"""
    def search_sentences(self, word, source_lang="eng", target_lang=None, 
                        has_audio=None, page=1, limit=10, sort=None):
        """
        Search for sentences containing a word or phrase
        - word: Word to search for
        - source_lang: Source language code (default `eng`)
        - target_lang: Target language code for translations (optional)
        - has_audio: Filter for sentences with audio ("yes" or "no") (optional)
        - page: Page number for results pagination (default 1)
        - limit: Number of results per page (default 10)
        - sort: Sort order ("relevance", "random", "created", "modified") (optional)
            
        Returns:
            Dictionary with search results or error message
        """
        # Prepare query with exact word matching
        if not word.startswith("=") and not word.startswith('"'):
            query = f"={word}"
        else:
            query = word
            
        params = {
            "from": source_lang,
            "query": query,
            "page": page,
            "limit": limit
        }
        
        if target_lang:
            params["to"] = target_lang
        if has_audio:
            params["has_audio"] = has_audio
        if sort:
            params["sort"] = sort

        try:
            response = requests.get(self.base_url + "search", params=params)
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                return {"error": f"Sentences not found for word: {word}"}
            
            return self._process_search_results(data, target_lang)
            
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
        
    def _process_search_results(self, data, target_lang):
        results = []

        # paging = data.get("paging", {}).get("Sentences", {})

        if "sentences" in data:
            result["sentences"] = data["sentences"]
            
            if target_lang and "translations" in data:
                result["translations"] = data["translations"]
            
        for result in data.get("results", []):
            sentence = {
                "id": result.get("id"),
                "text": result.get("text"),
                "language": {
                    "code": result.get("lang"),
                    "name": result.get("lang_name"),
                    "direction": result.get("dir")
                },
                "has_audio": bool(result.get("audios")),
                "translations": []
            }
            
            if "translations" in result:
                for translation_group in result["translations"]:
                    for translation in translation_group:
                        if not target_lang or translation.get("lang") == target_lang:
                            translation_item = {
                                "id": translation.get("id"),
                                "text": translation.get("text"),
                                "language": {
                                    "code": translation.get("lang"),
                                    "name": translation.get("lang_name"),
                                    "direction": translation.get("dir")
                                },
                                "has_audio": bool(translation.get("audios")),
                                "is_direct": translation.get("isDirect", False)
                            }
                            sentence["translations"].append(translation_item)
            
            results.append(sentence)
        
        return results    
        # return {
        #     "total": paging.get("count", 0),
        #     "page": paging.get("current", 1),
        #     "page_count": paging.get("pageCount", 1),
        #     "results_per_page": paging.get("perPage", len(results)),
        #     "results": results
        # }
    
    def get_audio_url(self, sentence_id):
        """Get audio URL for a sentence if available"""
        return f"https://audio.tatoeba.org/sentences/{sentence_id}.mp3"

# Run to test the service
if __name__ == "__main__":
    service = WiktionaryService()
    # tatoeba = TatoebaService()
    result = service.get_word_data("hello")
    # result = tatoeba.search_sentences(
    #     word="hello", 
    #     source_lang="eng", 
    # )
    # print(json.dumps(result, indent=2))