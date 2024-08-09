import cv2
import pytesseract
import pandas as pd
import os

# Specify the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:\packages\Tesseract\tesseract.exe'

def preprocess_image(image_path):
    # Check if the file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read the image file: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_bounding_boxes(image):
    # Extract bounding boxes for each word in the image
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
    return data

def parse_text_with_bounding_boxes(data):
    # Parse the text using bounding boxes
    rows = []
    current_row = []
    last_bottom = 0

    for i in range(len(data['level'])):
        top, left, width, height, text = data['top'][i], data['left'][i], data['width'][i], data['height'][i], data['text'][i]
        bottom = top + height

        # Check if we are in a new row
        if top > last_bottom:
            if current_row:
                rows.append(current_row)
                current_row = []
        current_row.append((left, text))
        last_bottom = bottom

    if current_row:
        rows.append(current_row)

    return rows

def align_columns(rows):
    # Align text in columns based on their bounding box left positions
    columns = {}
    for row in rows:
        for left, text in row:
            if text.strip():
                if left not in columns:
                    columns[left] = []
                columns[left].append(text)

    # Create a sorted list of columns based on their left positions
    sorted_columns = sorted(columns.items())

    # Create the final aligned rows
    aligned_rows = []
    max_length = max(len(col[1]) for col in sorted_columns)

    for i in range(max_length):
        aligned_row = []
        for _, texts in sorted_columns:
            aligned_row.append(texts[i] if i < len(texts) else '')
        aligned_rows.append(aligned_row)

    return aligned_rows

def display_table(table_data):
    # Convert list of lists into DataFrame
    df = pd.DataFrame(table_data)
    # Print DataFrame to console
    print(df)

def main():
    # Get user input for file path
    image_path = input("Enter the path to the image file: ").strip()
    
    try:
        preprocessed_image = preprocess_image(image_path)
        data = extract_bounding_boxes(preprocessed_image)
        rows = parse_text_with_bounding_boxes(data)
        table_data = align_columns(rows)
        display_table(table_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
