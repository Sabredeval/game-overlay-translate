import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text(img):
    # text = pytesseract.image_to_string(img)
    # save_text(text)
    return pytesseract.image_to_string(img)

def save_text(text):
    f = open("text/demo.txt", "w")
    f.write(text)
    f.close()