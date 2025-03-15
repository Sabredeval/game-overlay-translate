import tkinter as tk
from tkinter import Label, Text, Scrollbar, Button, OptionMenu, StringVar, messagebox
from selection_tool import GlobalSelectionApp
from pystray import Icon, Menu, MenuItem
from database_manager import WordDatabase
from PIL import Image
import threading
import keyboard


class MainInterface(tk.Tk):
    def __init__(self):

        super().__init__()
        self.title("Pymage - Main Interface")
        self.geometry("800x600")

        self.word_db = WordDatabase()

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Dropdowns for "Choose language"
        dropdown_frame = tk.Frame(self)
        dropdown_frame.grid(row=0, column=0, pady=10, sticky="ew")

        self.native_language_var = StringVar(self)
        self.native_language_var.set("English")
        languages = ["English", "Spanish", "French", "German"]
        native_language_dropdown = OptionMenu(dropdown_frame, self.native_language_var, *languages)
        native_language_dropdown.pack(side=tk.LEFT, padx=10)

        self.translated_language_var = StringVar(self)
        self.translated_language_var.set("Spanish")
        translated_language_dropdown = OptionMenu(dropdown_frame, self.translated_language_var, *languages)
        translated_language_dropdown.pack(side=tk.LEFT, padx=10)

        # Buttons: "Saved Words", "Browse Words", "Settings", "Start Selection"
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        self.saved_words_button = Button(button_frame, text="Saved Words", command=self.saved_words)
        self.saved_words_button.pack(side=tk.LEFT, padx=10)

        self.browse_words_button = Button(button_frame, text="Browse Words", command=self.browse_words)
        self.browse_words_button.pack(side=tk.LEFT, padx=10)

        self.settings_button = Button(button_frame, text="Settings", command=self.on_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        self.start_selection_button = Button(button_frame, text="Start Selection", command=self.start_selection)
        self.start_selection_button.pack(side=tk.LEFT, padx=10)

        self.save_word_button = Button(button_frame, text="Save word", command=self.save_word)
        self.save_word_button.pack(side=tk.LEFT, padx=10)

        # Native language text
        native_text_frame = tk.Frame(self)
        native_text_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        native_label = Label(native_text_frame, text="Native Text:")
        native_label.pack(anchor=tk.W)

        native_scrollbar = Scrollbar(native_text_frame)
        native_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.native_text_widget = Text(native_text_frame, wrap=tk.WORD, yscrollcommand=native_scrollbar.set)
        self.native_text_widget.pack(fill=tk.BOTH, expand=True)

        native_scrollbar.config(command=self.native_text_widget.yview)

        # Translated language text
        translated_text_frame = tk.Frame(self)
        translated_text_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        translated_label = Label(translated_text_frame, text="Translated Text:")
        translated_label.pack(anchor=tk.W)

        translated_scrollbar = Scrollbar(translated_text_frame)
        translated_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.translated_text_widget = Text(translated_text_frame, wrap=tk.WORD, yscrollcommand=translated_scrollbar.set)
        self.translated_text_widget.config(state=tk.DISABLED)
        self.translated_text_widget.pack(fill=tk.BOTH, expand=True)

        translated_scrollbar.config(command=self.translated_text_widget.yview)
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        self.tray_icon = None
        self.create_tray_icon()
        keyboard.add_hotkey("ctrl+e", self.start_selection)

    def create_tray_icon(self):
        icon_image = Image.open("icon.png")

        menu = Menu(
            MenuItem("Restore", self.restore_window),
            MenuItem("Exit", self.exit_application)
        )

        self.tray_icon = Icon("Pymage", icon_image, "Pymage", menu)

        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def minimize_to_tray(self):
        self.withdraw()

    def restore_window(self):
        self.deiconify()
        self.tray_icon.stop()

    def exit_application(self):
        self.tray_icon.stop()
        self.destroy()

    def browse_words(self):
        print("Browse Words...")

    def on_settings(self):
        print("Settings...")

    def start_selection(self):
        if not hasattr(self, "selection_app") or self.selection_app is None:
            self.selection_app = GlobalSelectionApp(self)
        self.selection_app.on_ctrl_e()

    def saved_words(self):
        """Open a window to view saved words"""
        saved_window = tk.Toplevel(self)
        saved_window.title("Saved Words")
        saved_window.geometry("500x400")
        saved_window.minsize(400, 300)
        
        search_frame = tk.Frame(saved_window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, width=20)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        def search_words():
            query = search_entry.get().strip()
            if query:
                words = self.word_db.search_words(query)
            else:
                words = self.word_db.get_saved_words()
            
            update_word_list(words)
        
        search_button = tk.Button(search_frame, text="Search", command=search_words)
        search_button.pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(saved_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        word_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
        word_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=word_listbox.yview)
        
        button_frame = tk.Frame(saved_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def delete_selected_word():
            selection = word_listbox.curselection()
            if selection:
                index = selection[0]
                word_id = word_items[index][0]
                
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this word?"):
                    self.word_db.delete_word(word_id)
                    words = self.word_db.get_saved_words()
                    update_word_list(words)
        
        def toggle_favorite():
            selection = word_listbox.curselection()
            if selection:
                index = selection[0]
                word_id = word_items[index][0]
                
                self.word_db.toggle_favorite(word_id)
                words = self.word_db.get_saved_words()
                update_word_list(words)
        
        delete_button = tk.Button(button_frame, text="Delete", command=delete_selected_word)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        favorite_button = tk.Button(button_frame, text="Toggle Favorite", command=toggle_favorite)
        favorite_button.pack(side=tk.LEFT, padx=5)
        
        def update_word_list(words):
            word_listbox.delete(0, tk.END)
            nonlocal word_items
            word_items = words
            
            for word_item in word_items:
                word_id, word_text, lang, date, favorite = word_item
                star = "★" if favorite else "☆"
                display_text = f"{star} {word_text} ({lang})"
                word_listbox.insert(tk.END, display_text)
        
        # Initialize list with all saved words
        word_items = self.word_db.get_saved_words()
        update_word_list(word_items)

    def save_word(self):
        # Gets user selected text
        if self.native_text_widget.tag_ranges(tk.SEL):
            selected_text = self.native_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            print(f"Selected text: {selected_text}")
        # If nothing is selected get the current line and the first word
        else:
            current_line = self.native_text_widget.get("insert linestart", "insert lineend").strip()
            if current_line:
                # Split by spaces and get the first word
                selected_text = current_line.split()[0]
            else:
                messagebox.showinfo("No word selected", "Please select a word to save.")
                return
        
        if not selected_text:
            messagebox.showinfo("No word selected", "Please select a word to save.")
            return
        
        source_lang = self.native_language_var.get()
            
        # Check if word already exists
        if self.word_db.word_exists(selected_text):
            messagebox.showinfo("Word Already Saved", f"The word '{selected_text}' is already saved.")
            return
        
        word_id = self.word_db.save_word(selected_text, source_lang)
        
        # Check if word was saved
        if word_id:
            messagebox.showinfo("Success", f"Word '{selected_text}' saved successfully!")
        else:
            messagebox.showinfo("Already Saved", f"The word '{selected_text}' is already in your saved list.")

if __name__ == "__main__":
    app = MainInterface()
    app.mainloop()