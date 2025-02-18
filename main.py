import sys
import pytesseract
import mss
import numpy as np
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer, QRect
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

        self.text_boxes = []  # Store detected text regions
        self.translations = {}  # Store translations for each region

        self.show()

    def on_hotkey_press(self, key):
        """Trigger screenshot and OCR when hotkey is pressed"""
        try:
            if key == keyboard.Key.f9:  # Press F9 to activate
                self.capture_screen()
                print("GAY")
        except AttributeError:
            pass

    def capture_screen(self):
        """Take a screenshot and extract text"""
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])  # Capture main screen
            img = np.array(screenshot)  # Convert to NumPy array
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)  # Convert color format

            with mss.mss() as sct:
                screenshot = sct.grab(sct.monitors[1])  # Capture main screen
                img = np.array(screenshot)  # Convert to NumPy array
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)  # Convert to grayscale

                # Apply thresholding to enhance text detection
                thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                # Find contours (text block detection)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                self.text_boxes.clear()
                self.translations.clear()

                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if w > 50 and h > 20:  # Filter out small noise
                        self.text_boxes.append(QRect(x, y, w, h))
                        
                        # Crop the detected text area
                        text_region = img[y:y+h, x:x+w]
                        
                        # OCR on the cropped region
                        extracted_text = pytesseract.image_to_string(text_region, config='--psm 6')
                        # if text.strip():
                        #     translated_text = self.translate_text(text)
                        #     self.show_overlay(translated_text)

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
