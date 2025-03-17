###
# This class is used to store the configuration of the application.
# TOBE extended in the future to allow for user customization via settings.
###
class ConfigModel:
    def __init__(self):
        self.languages = ["English", "Spanish", "French", "German"]
        self.default_native = "English"
        self.default_translated = "Spanish"
        
    def get_languages(self):
        return self.languages