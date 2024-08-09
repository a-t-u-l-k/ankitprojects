import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define L2 Regularization
l2_regularizer = regularizers.l2(0.001)  # Reduced regularization strength

# Load VGG16 model pre-trained on ImageNet, excluding the top layer
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
base_model.trainable = False  # Freeze the base model

# Define the CNN model with Transfer Learning and L2 Regularization
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu', kernel_regularizer=l2_regularizer),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),  # Lower learning rate
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Set up data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Load and augment the data
train_generator = train_datagen.flow_from_directory(
    'path_to_train_directory',
    target_size=(128, 128),
    batch_size=32,
    class_mode='sparse'
)

validation_generator = validation_datagen.flow_from_directory(
    'path_to_validation_directory',
    target_size=(128, 128),
    batch_size=32,
    class_mode='sparse'
)

# Define callbacks for saving the model and early stopping
callbacks = [
    tf.keras.callbacks.ModelCheckpoint('model_checkpoint.h5', save_best_only=True, monitor='val_loss'),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
]

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=20,  # Increased number of epochs
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // 32,
    callbacks=callbacks
)

# Save the final model
model.save('final_model.h5')
