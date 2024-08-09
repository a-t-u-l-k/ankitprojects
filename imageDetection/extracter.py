import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import fitz  # PyMuPDF
import io

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:\packages\Tesseract\tesseract.exe'

def preprocess_image(img):
    try:
        img = img.convert('L')  # Convert to grayscale
        img = img.resize((int(img.width * 3), int(img.height * 3)), Image.LANCZOS)
        img = ImageOps.autocontrast(img, cutoff=0)
        img = img.point(lambda x: 0 if x < 180 else 255)
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        return img
    except Exception as e:
        print(f'Error during preprocessing: {e}')
        return None

def extract_text(image):
    try:
        img = preprocess_image(image)
        if img:
            text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
            return text.strip()
        else:
            print('Failed to preprocess image.')
            return None
    except Exception as e:
        print(f'Error during text extraction: {e}')
        return None

def extract_text_from_pdf(pdf_path):
    try:
        if not os.path.isfile(pdf_path):
            print(f"File not found: {pdf_path}")
            return
        print(f'Processing PDF file: {pdf_path}')
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            extracted_text = extract_text(img)
            if extracted_text:
                print(f'Page {page_number + 1} Text:\n{extracted_text}')
    except Exception as e:
        print(f'Error during PDF extraction: {e}')

def main():
    while True:
        file_path = input("Enter the path to the image or PDF file (or 'exit' to quit): ").strip()
        if file_path.lower() == 'exit':
            break
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue
        print(f'Processing file: {file_path}')
        if file_path.lower().endswith('.pdf'):
            extract_text_from_pdf(file_path)
        else:
            try:
                img = Image.open(file_path)
                extracted_text = extract_text(img)
                if extracted_text:
                    print(f'Extracted Text:\n{extracted_text}')
            except Exception as e:
                print(f'Error: {e}')

if __name__ == "__main__":
    main()
