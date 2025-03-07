import sys
import pytesseract
import mss
import numpy as np
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
from pynput import keyboard
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class ScreenCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Translator")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.translator = Translator()
        self.hotkey_listener = keyboard.Listener(on_press=self.on_hotkey_press)
        self.hotkey_listener.start()

        self.show()

    def on_hotkey_press(self, key):
        """Trigger screenshot and OCR when hotkey is pressed"""
        try:
            if key == keyboard.Key.f9:  # Press F9 to activate
                self.capture_screen()
        except AttributeError:
            pass

    def capture_screen(self):
        """Take a screenshot and extract text"""
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])  # Capture main screen
            img = np.array(screenshot)  # Convert to NumPy array
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)  # Convert color format

            # OCR (Extract text)
            text = pytesseract.image_to_string(img)
            print(f"Extracted Text: {text}")

            if text.strip():
                translated_text = self.translate_text(text)
                self.show_overlay(translated_text)

    def translate_text(self, text):
        """Translate text using Google Translate"""
        translated = self.translator.translate(text, dest='en')
        return translated.text

    def show_overlay(self, text):
        """Display overlay with translated text"""
        self.label.setText(text)
        self.label.adjustSize()
        self.label.move(100, 100)  # Position overlay
        self.label.show()

        # Auto-hide overlay after 5 seconds
        QTimer.singleShot(5000, self.label.hide)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenCaptureApp()
    sys.exit(app.exec())
