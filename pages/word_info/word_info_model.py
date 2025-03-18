class WordInfoModel:
    """This class is responsible for managing the data of a word info window"""
    def __init__(self, word, source_lang="English"):
        self.word = word
        self.source_lang = source_lang
        self.definitions = []
        self.etymology = ""
        self.examples = []

    def fetch_data(self):
        # TODO - Implement actual data fetching
        self.definitions = [
            "This is a placeholder definition.",
            "In a real implementation, this would show actual word data."
        ]
        self.etymology = "From Latin placeholder, from Greek placeholderus."
        self.examples = [
            f"This is an example sentence using the word '{self.word}'.",
            f"Another example with '{self.word}' in context."
        ]
        return self


class DatabaseHandler:
    def save_word(self, word_db, word, source_lang):
        if not word_db:
            return False

        if word_db.word_exists(word):
            return None
        
        return word_db.save_word(word, source_lang)