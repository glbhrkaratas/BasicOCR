import cv2
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    img = cv2.resize(img, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    gray = cv2.medianBlur(gray, 5)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    return thresh


def detect_language(image_path):
    processed_image = preprocess_image(image_path)
    pil_image = Image.fromarray(processed_image)
    osd = pytesseract.image_to_osd(pil_image, config='--dpi 400')
    for line in osd.split('\n'):
        if 'Script' in line:
            script = line.split(': ')[1].strip()
            script_to_lang = {
                'Latin': 'eng',
                'Turkish': 'tur',
                'Cyrillic': 'rus',
                'Arabic': 'ara',
            }
            return script_to_lang.get(script, 'eng')
    return 'eng'


def extract_text(image_path, lang='eng'):
    processed_image = preprocess_image(image_path)
    pil_image = Image.fromarray(processed_image)
    custom_config = r'--oem 3 --psm 6 --dpi 400 -c preserve_interword_spaces=1'
    text = pytesseract.image_to_string(pil_image, lang=lang, config=custom_config)
    return text