import tkinter as tk
from tkinter import Label, Text, Scrollbar, Button, OptionMenu, StringVar
from selection_tool import GlobalSelectionApp  # Import the selection functionality
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import keyboard


class MainInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pymage - Main Interface")
        self.geometry("800x600")

        # Configure grid layout for dynamic resizing
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

        self.saved_words_button = Button(button_frame, text="Saved Words", command=self.on_saved_words)
        self.saved_words_button.pack(side=tk.LEFT, padx=10)

        self.browse_words_button = Button(button_frame, text="Browse Words", command=self.on_browse_words)
        self.browse_words_button.pack(side=tk.LEFT, padx=10)

        self.settings_button = Button(button_frame, text="Settings", command=self.on_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        self.start_selection_button = Button(button_frame, text="Start Selection", command=self.start_selection)
        self.start_selection_button.pack(side=tk.LEFT, padx=10)

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

    def on_saved_words(self):
        print("Saved Words...")

    def on_browse_words(self):
        print("Browse Words...")

    def on_settings(self):
        print("Settings...")

    def start_selection(self):
        if not hasattr(self, "selection_app") or self.selection_app is None:
            self.selection_app = GlobalSelectionApp(self)
        self.selection_app.on_ctrl_e()


if __name__ == "__main__":
    app = MainInterface()
    app.mainloop()