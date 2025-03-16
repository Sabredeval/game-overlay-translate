import enchant

def validate_word(word, language="en_US"):
    dictionary = enchant.Dict(language)
    if dictionary.check(word):
        print(f"'{word}' is a valid word!")
    else:
        suggestions = dictionary.suggest(word)
        print(f"'{word}' is not a valid word. Did you mean: {', '.join(suggestions)}?")