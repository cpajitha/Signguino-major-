TF_ENABLE_ONEDNN_OPTS=0
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
EPOCHS=50
# Ensure that TensorFlow version is compatible
print("TensorFlow version:", tf.__version__)

# Data Augmentation and Preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load Training and Test Data
train_set = train_datagen.flow_from_directory(
    'C:/Users/Sys/Signliingo-Major/dataset/isl_data_grey_split/train',
    target_size=(128, 128),
    batch_size=32,
    color_mode='grayscale',
    class_mode='categorical'
)

test_set = test_datagen.flow_from_directory(
    'C:/Users/Sys/Signliingo-Major/dataset/isl_data_grey_split/test',
    target_size=(128, 128),
    batch_size=32,
    color_mode='grayscale',
    class_mode='categorical'
)

# Define Model Architecture
classifier = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu", input_shape=(128, 128, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=2, strides=2, padding='valid'),
    tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=2, strides=2, padding='valid'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(units=96, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=36, activation='softmax')  # Output layer with softmax activation for multi-class classification
])

# Compile Model
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy','precision','recall'])

# Display Model Summary
classifier.summary()

# Train the Model
history = classifier.fit(
    train_set,
    epochs=EPOCHS,
    validation_data=test_set
)

scores=classifier.evaluate(test_set)


acc=history.history["accuracy"]
val_acc=history.history["val_accuracy"]
prec=history.history["precision"]
val_prec=history.history["val_precision"]
recall=history.history["recall"]
val_recall=history.history["val_recall"]
loss=history.history["loss"]
val_loss=history.history["val_loss"]

plt.figure(figsize=(8,8))
plt.subplot(2,2,1)
plt.plot(range(EPOCHS),acc,label="Training Accuracy")
plt.plot(range(EPOCHS),val_acc,label="Validation Accuracy")
plt.legend(loc="lower right")
plt.title("Training and validation accuracy")

plt.subplot(2,2,2)
plt.plot(range(EPOCHS),loss,label="Training Loss")
plt.plot(range(EPOCHS),val_loss,label="Validation Loss")
plt.legend(loc="upper right")
plt.title("Training and validation loss")

plt.subplot(2,2,3)
plt.plot(range(EPOCHS),prec,label="Training precision")
plt.plot(range(EPOCHS),val_prec,label="Validation precision")
plt.legend(loc="lower right")
plt.title("Training and validation precision")

plt.subplot(2,2,4)
plt.plot(range(EPOCHS),recall,label="Training Recall")
plt.plot(range(EPOCHS),val_recall,label="Validation Reacll")
plt.legend(loc="lower right")
plt.title("Training and validation recall")
plt.show()

# Save Model and Weights
model_json = classifier.to_json()
with open("model_new.json", "w") as json_file:
    json_file.write(model_json)
print('Model Saved')

classifier.save_weights('model_new.weights.h5')
print('Weights saved')

