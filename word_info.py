import tkinter as tk
from controller.word_info_controller import WordInfoController

class WordInfoPopup:
    def __init__(self, parent, word):
        self.controller = WordInfoController(parent, word)
        self.view = self.controller.view