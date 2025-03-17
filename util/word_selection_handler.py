import tkinter as tk

class WordSelectionHandler:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def get_selected_text(self):
        if self.text_widget.tag_ranges(tk.SEL):
            return self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        return ""
    
    def get_first_word_from_current_line(self):
        current_line = self.text_widget.get("insert linestart", "insert lineend").strip()
        if current_line:
            return current_line.split()[0]
        return ""