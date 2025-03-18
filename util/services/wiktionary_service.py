import requests
import json
from bs4 import BeautifulSoup

class WiktionaryService:
    def __init__(self):
        self.base_url = "https://en.wiktionary.org/w/api.php"
        
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
        for header in soup.find_all(['h2', 'h3', 'h4']):
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
        """
        Search for words that start with the given prefix
        
        Args:
            prefix: Beginning of the word
            limit: Maximum number of results to return
            
        Returns:
            List of words starting with the prefix
        """
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

# Run to test the service
if __name__ == "__main__":
    service = WiktionaryService()
    result = service.get_word_data("hello")
    print(json.dumps(result, indent=2))