import os
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress info and warning messages

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# Load MobileNetV2 with pre-trained weights
print("Loading MobileNetV2 model...")
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Save the model in the native Keras format
model.save('mobilenet_v2.keras')

print("Model downloaded and saved as 'mobilenet_v2.keras'")

# Define root directories to search for images
search_directories = [
    r'C:\\',
    r'D:\\',
    r'E:\\',
    # Add specific folders if necessary
]

def find_image_file(file_name):
    """Search for the file in predefined directories and all subdirectories."""
    print(f"Searching for file '{file_name}'...")
    start_time = time.time()
    for directory in search_directories:
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                end_time = time.time()
                print(f"File found in {end_time - start_time:.2f} seconds.")
                return os.path.join(root, file_name)
    end_time = time.time()
    print(f"File not found after {end_time - start_time:.2f} seconds.")
    return None

def get_image_file_name_or_path():
    """Prompt the user to enter a file name or path and handle validation."""
    while True:
        user_input = input("Please enter the image file name (e.g., '1714513388194.jpeg') or full file path, or type 'exit' to quit: ")

        if user_input.lower() == 'exit':
            print("Exiting the program.")
            return None

        if os.path.isfile(user_input):
            return user_input  # Full path provided
        else:
            # File name provided, search in predefined directories
            file_path = find_image_file(user_input)
            if file_path is None:
                print(f"File '{user_input}' not found in the specified drives. Please try again.")
            else:
                return file_path

# Main loop
while True:
    # Get the valid image file path from the user
    img_path = get_image_file_name_or_path()

    # If user chooses to exit, break the loop
    if img_path is None:
        break

    print(f"Loading and processing image from '{img_path}'...")
    # Load and preprocess the image
    start_time = time.time()
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Preprocess the image
    img_array = preprocess_input(img_array)
    end_time = time.time()
    print(f"Image loaded and preprocessed in {end_time - start_time:.2f} seconds.")

    # Make predictions
    print("Making predictions...")
    start_time = time.time()
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    end_time = time.time()
    print(f"Predictions made in {end_time - start_time:.2f} seconds.")

    # Create a dictionary for simple label mappings
    simple_labels = {
        'tabby': 'cat',
        'tiger_cat': 'cat',
        'Egyptian_cat': 'cat',
        'Labrador_retriever': 'dog',
        'golden_retriever': 'dog',
        'Pembroke': 'dog',
        # Add more mappings as needed
    }

    # Extract and map the top class label to a simpler word
    top_prediction = decoded_predictions[0][1]
    simple_prediction = simple_labels.get(top_prediction, top_prediction)  # Use the mapped label if available, otherwise use the original

    print('Predicted:', simple_prediction)
