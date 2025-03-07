import sys
import mss
import numpy as np
import cv2
import pytesseract
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QGuiApplication
from PyQt6.QtCore import Qt, QRect, QTimer, QEvent
from pynput import keyboard

# Set Tesseract path (Windows only, update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class ScreenTextSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Selector")
        self.setGeometry(0, 0, QGuiApplication.primaryScreen().geometry().width(), 
                         QGuiApplication.primaryScreen().geometry().height())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.start_pos = None
        self.end_pos = None
        self.selection_rect = None

        self.setMouseTracking(True)
        self.showFullScreen()

    def mousePressEvent(self, event):
        """Start selection."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = None
            self.selection_rect = None
            self.update()

    def mouseMoveEvent(self, event):
        """Update selection rectangle while dragging."""
        if self.start_pos:
            self.end_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, self.end_pos)
            self.update()

    def mouseReleaseEvent(self, event):
        """Finalize selection and extract text."""
        if event.button() == Qt.MouseButton.LeftButton and self.selection_rect:
            self.extract_text()
            self.close()

    def paintEvent(self, event):
        """Draw the selection rectangle."""
        if self.selection_rect:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 255, 0, 200), 2))  # Green border
            painter.setBrush(QColor(0, 255, 0, 50))  # Transparent green fill
            painter.drawRect(self.selection_rect)
            painter.end()

    def extract_text(self):
        """Extract text from the selected area."""
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])  # Capture full screen
            img = np.array(screenshot)

            # Get selected area coordinates
            x1, y1 = self.selection_rect.topLeft().x(), self.selection_rect.topLeft().y()
            x2, y2 = self.selection_rect.bottomRight().x(), self.selection_rect.bottomRight().y()

            cropped_img = img[y1:y2, x1:x2]  # Crop selection
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            text = pytesseract.image_to_string(gray, config="--psm 6")  # Extract text

            print("Extracted Text:\n", text)  # Later replace with translation logic

def on_shortcut():
    """Trigger selection window when shortcut is pressed."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    selector = ScreenTextSelector()
    app.exec()

# Listen for shortcut (Ctrl + T)
listener = keyboard.GlobalHotKeys({'<ctrl>+3': on_shortcut})
listener.start()

if __name__ == "__main__":
    print("Press Ctrl + T to select text area for translation...")
    listener.join()  # Keep the script running
