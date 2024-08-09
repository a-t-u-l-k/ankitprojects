import os
import shutil
import re
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def rename_and_prepare_data(base_dir, output_dir, category_mappings):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for dir_name in os.listdir(base_dir):
        match = re.match(r'category_\d+_(.*)', dir_name)
        if match:
            category = match.group(1).lower()
            if category in category_mappings:
                single_word = category_mappings[category]
                category_path = os.path.join(base_dir, dir_name)
                single_word_path = os.path.join(output_dir, single_word)
                if not os.path.exists(single_word_path):
                    os.makedirs(single_word_path)
                
                for file_name in os.listdir(category_path):
                    old_file_path = os.path.join(category_path, file_name)
                    new_file_name = f"{single_word}_{file_name}"
                    new_file_path = os.path.join(single_word_path, new_file_name)
                    try:
                        shutil.copy2(old_file_path, new_file_path)
                        print(f"Copied: {old_file_path} to {new_file_path}")
                    except Exception as e:
                        print(f"Failed to copy {old_file_path}: {e}")

def split_data_into_train_val(output_dir):
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    for category in os.listdir(output_dir):
        category_path = os.path.join(output_dir, category)
        if os.path.isdir(category_path) and category not in ['train', 'val']:
            files = os.listdir(category_path)
            np.random.shuffle(files)
            split_idx = int(0.8 * len(files))
            train_files = files[:split_idx]
            val_files = files[split_idx:]

            train_category_path = os.path.join(train_dir, category)
            val_category_path = os.path.join(val_dir, category)
            if not os.path.exists(train_category_path):
                os.makedirs(train_category_path)
            if not os.path.exists(val_category_path):
                os.makedirs(val_category_path)

            for file in train_files:
                try:
                    shutil.copy2(os.path.join(category_path, file), os.path.join(train_category_path, file))
                except Exception as e:
                    print(f"Failed to copy {file} to train directory: {e}")
            for file in val_files:
                try:
                    shutil.copy2(os.path.join(category_path, file), os.path.join(val_category_path, file))
                except Exception as e:
                    print(f"Failed to copy {file} to val directory: {e}")

def fetch_and_train_model(train_dir, val_dir):
    train_datagen = ImageDataGenerator(rescale=1./255)
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='sparse'
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='sparse'
    )

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(len(train_generator.class_indices), activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.fit(train_generator, epochs=10, validation_data=val_generator)
    
    return model

def main():
    base_dir = "D:\\Projects\\E"
    output_dir = "D:\\categorymappingoutput"

    category_mappings = {
        "tornado": "tornado",
        "lightning": "lightning",
        "cloud": "cloud",
        "tulip": "tulip",
        "sunflower": "sunflower",
        "daisy": "daisy",
        "orchid": "orchid",
        "cactus": "cactus",
        "rose": "rose",
        "leaf": "leaf",
        "mushroom": "mushroom",
        "frog": "frog",
        "spider": "spider",
        "bee": "bee",
        "butterfly": "butterfly",
        "peacock": "peacock",
        "parrot": "parrot",
        "monkey": "monkey",
        "kangaroo": "kangaroo",
        "zebra": "zebra",
        "giraffe": "giraffe",
        "elephant": "elephant",
        "bear": "bear",
        "tiger": "tiger",
        "lion": "lion",
        "eagle": "eagle",
        "penguin": "penguin",
        "jellyfish": "jellyfish",
        "turtle": "turtle",
        "whale": "whale",
        "shark": "shark",
        "dolphin": "dolphin",
        "coral": "coral",
        "reef": "reef",
        "wave": "wave",
        "ocean": "ocean",
        "aurora": "aurora",
        "eclipse": "eclipse",
        "sunrise": "sunrise",
        "sky": "sky",
        "night": "night",
        "star": "star",
        "planet": "planet",
        "glacier": "glacier",
        "canyon": "canyon",
        "desert": "desert",
        "volcano": "volcano",
        "rainbow": "rainbow",
        "waterfall": "waterfall",
        "cup": "cup",
        "camera": "camera",
        "violin": "violin",
        "piano": "piano",
        "guitar": "guitar",
        "keyboard": "keyboard",
        "glasses": "glasses",
        "pen": "pen",
        "lamp": "lamp",
        "clock": "clock",
        "bag": "bag",
        "shoe": "shoe",
        "hat": "hat",
        "watch": "watch",
        "building": "building",
        "road": "road",
        "garden": "garden",
        "forest": "forest",
        "street": "street",
        "bicycle": "bicycle",
        "boat": "boat",
        "airplane": "airplane",
        "bridge": "bridge",
        "bed": "bed",
        "table": "table",
        "chair": "chair",
        "computer": "computer",
        "house": "house",
        "horse": "horse",
        "fish": "fish",
        "bird": "bird",
        "sunset": "sunset",
        "city": "city",
        "beach": "beach",
        "river": "river",
        "mountain": "mountain",
        "flower": "flower",
        "tree": "tree",
        "car": "car",
        "dog": "dog",
        "cat": "cat",
        "ball": "ball",
        "bat": "bat",
        "fan": "fan",
        "furniture": "furniture",
        "gun": "gun",
        "bags": "bags",
        "deodorants": "deodorants",
        "water": "water",
        "mountains": "mountains",
        "cars": "cars",
        "animals": "animals",
        "flowers": "flowers"
    }
    
    rename_and_prepare_data(base_dir, output_dir, category_mappings)
    split_data_into_train_val(output_dir)
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    model = fetch_and_train_model(train_dir, val_dir)
    model.save('my_image_recognition_model.h5')
    print("Model training complete and saved as 'my_image_recognition_model.h5'.")

if __name__ == "__main__":
    main()
