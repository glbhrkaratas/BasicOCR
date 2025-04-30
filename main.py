import cv2
import pytesseract
from PIL import Image



def preprocess_image(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh


def extract_text(image_path):
    processed_image = preprocess_image(image_path)

    pil_image = Image.fromarray(processed_image)

    text = pytesseract.image_to_string(pil_image, lang='eng')

    return text


def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


def main():
    image_path = 'input/sample_image.png'

    output_path = 'output/extracted_text.txt'

    try:
        extracted_text = extract_text(image_path)

        print("Çıkarılan Metin:")
        print(extracted_text)

        save_text_to_file(extracted_text, output_path)
        print("Metin {output_path} dosyasına kaydedildi.")

    except Exception as e:
        print("Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()