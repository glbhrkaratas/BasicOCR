# OCR OpenCV Uygulaması

Bu proje, OpenCV ve Pytesseract kullanarak görüntülerden metin okuma (OCR) işlemi yapmayı amaçlayan bir Python uygulamasıdır. OCR, optik karakter tanıma anlamına gelir ve görsel içerikteki metni dijital metne dönüştürmek için kullanılır.

## Özellikler
- Görsellerden metin çıkarma
- OpenCV ile görüntü işleme (filtreler, tespitler)
- Pytesseract ile metin okuma

## Gereksinimler

Projenin çalışabilmesi için aşağıdaki Python kütüphanelerine ihtiyaç vardır:

- OpenCV
- Pytesseract
- Pillow


## Kurulum
- Bu projeyi klonlayın veya indirin.
- Proje dizinine gidin ve sanal ortam oluşturun:python -m venv .venv


- Sanal ortamı etkinleştirin:
`Windows: .venv\Scripts\activate
`Linux/Mac: source .venv/bin/activate


- Gerekli kütüphaneleri yükleyin:pip install -r requirements.txt


- Tesseract'ı bilgisayarınıza kurun:`
Windows: https://github.com/UB-Mannheim/tesseract/wiki
Linux: sudo apt-get install tesseract-ocr
Mac: brew install tesseract`



## Kullanım

- input klasörüne bir görüntü dosyası koyun (örneğin sample_image.png).
  main.py dosyasını çalıştırın:python main.py


- Çıkarılan metin ekrana yazdırılacak ve output/extracted_text.txt dosyasına kaydedilecektir.

## Proje Yapısı

- input/: Görüntü dosyalarını buraya koyun.
- output/: Çıkarılan metinler buraya kaydedilir.
- main.py: Tüm OCR işlemlerini yapan ana dosya.

