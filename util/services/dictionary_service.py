class DictionaryService:
    def __init__(self):
        self.dictionary = {
            "hello": "world",
            "world": "hello"
        }

    def get_word(self, word):
        return self.dictionary.get(word, None)