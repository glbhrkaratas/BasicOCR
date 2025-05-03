from app.ocr_engine import extract_text, detect_language

def process_image(image_path, lang):
    if lang == "auto":
        lang = detect_language(image_path)
    text = extract_text(image_path, lang)
    return text, lang

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)