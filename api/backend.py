from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from fastapi import File, UploadFile
from typing import List
import numpy as np
from io import BytesIO
from PIL import Image
import uvicorn
import pyttsx3
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()
app.mount("/static", StaticFiles(directory="D:/mtech/major/Signliingo-Major/api", html=True), name="static")
# Add CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This will allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
               "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
               "U", "V", "W", "X", "Y", "Z"]

model_json_path = "D:/mtech/major/Signliingo-Major/model_new.json"
model_weights_path = "D:/mtech/major/Signliingo-Major/model_new.weights.h5"
SIGN_IMAGES_DIR = "D:/mtech/major/Signliingo-Major/dataset"
# Directory path containing alphabet sign images
LETTER_TO_FILENAME = {
    "0": "D:/mtech/major/Signlingo/dataset/0/zero_480.jpg",
    "1": "D:/mtech/major/Signlingo/dataset/1/one_437.jpg",
    "2": "D:/mtech/major/Signlingo/dataset/2/two_313.jpg",
    "3": "C:/Users/Sys/Signlingo/dataset/ISL_Dataset/3/three_403.jpg",
    "4": "C:/Users/Sys/Signlingo/dataset/ISL_Dataset/4/four_357.jpg",
    "5": "C:/Users/Sys/Signlingo/dataset/ISL_Dataset/5/five_201.jpg",
    "6": "D:/mtech/major/Signlingo/dataset/6/4.jpg",
    "7": "D:/mtech/major/Signlingo/dataset/7/6.jpg",
    "8": "D:/mtech/major/Signlingo/dataset/8/7.jpg",
    "9": "D:/mtech/major/Signlingo/dataset/9/9.jpg",
    "A": "D:/mtech/major/Signliingo-Major/dataset/A/A (8).jpg",
    "B": "D:/mtech/major/Signliingo-Major/dataset/B/B (15).jpg",
    "C": "D:/mtech/major/Signliingo-Major/dataset/C/C (15).jpg",
    "D": "D:/mtech/major/Signliingo-Major/dataset/D/D (29).jpg",
    "E": "D:\mtech\major\Signliingo-Major\dataset\E\E (39).jpg",
    "F": "D:\mtech\major\Signliingo-Major\dataset\F\F (18).jpg",
    "G": "D:\mtech\major\Signliingo-Major\dataset\G\G (25).jpg",
    "H": ""D:\mtech\major\Signliingo-Major\dataset\H\25.jpg"",
    "I": "D:/mtech/major/Signlingo/dataset/I/I (9).jpg",
    "J": "D:/mtech/major/Signlingo/dataset/J/7.jpg",
    "K": "D:/mtech/major/Signlingo/dataset/K/K (5).jpg",
    "L": "D:/mtech/major/Signlingo/dataset/L/L (5).jpg",
    "M": "D:/mtech/major/Signlingo/dataset/M/M (6).jpg",
    "N": "D:/mtech/major/Signlingo/dataset/N/N (9).jpg",
    "O": "D:/mtech/major/Signlingo/dataset/O/O (6).jpg",
    "P": "D:/mtech/major/Signlingo/dataset/P/P (12).jpg",
    "Q": "D:/mtech/major/Signlingo/dataset/Q/Q (25).jpg",
    "R": "D:/mtech/major/Signlingo/dataset/R/R (24).jpg",
    "S": "D:/mtech/major/Signlingo/dataset/S/S (10).jpg",
    "T": "D:/mtech/major/Signlingo/dataset/T/T (26).jpg",
    "U": "D:/mtech/major/Signlingo/dataset/U/U (24).jpg",
    "V": "D:/mtech/major/Signlingo/dataset/V/V (6).jpg",
    "W": "D:/mtech/major/Signlingo/dataset/W/W (25).jpg",
    "X": "D:/mtech/major/Signlingo/dataset/X/X (21).jpg",
    "Y": "D:/mtech/major/Signlingo/dataset/Y/15.jpg",
    "Z": "D:/mtech/major/Signlingo/dataset/Z/Z (24).jpg",
}

engine = pyttsx3.init()

try:
    with open(model_json_path, "r") as json_file:
        loaded_model_json = json_file.read()
    MODEL = tf.keras.models.model_from_json(loaded_model_json)
    MODEL.load_weights(model_weights_path)
    
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading the model:", e)
    logging.error("Error loading the model: %s", str(e))


def preprocess_image(image):
    if(image.mode=='RGB'):
        image=image.convert('L')
    else:
        image=image
    # Resize the image to the desired size
    resized_image = image.resize((128, 128))
    # Convert image to numpy array and normalize pixel values
    image_array = np.array(resized_image) / 255.0
    # Expand dimensions to make it compatible with model input shape
    processed_image = np.expand_dims(image_array, axis=0)
    return processed_image

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    return image

def recognize_word(sign_sequence):
    word = ''
    for sign_gesture in sign_sequence:
        preprocessed_gesture = preprocess_image(sign_gesture)
        predictions = MODEL.predict(preprocessed_gesture)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        word += predicted_class + " "  # Add space between words
    return word.strip()  # Remove trailing space
def recognize_word(sign_sequence):
    word = ''
    for sign_gesture in sign_sequence:
        preprocessed_gesture = preprocess_image(sign_gesture)
        predictions = MODEL.predict(preprocessed_gesture)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        word += predicted_class
    
    return word

def load_sign_image(filename):
    image_path = os.path.join(SIGN_IMAGES_DIR, filename)
    image = Image.open(image_path)
    return np.array(image)
@app.options("/generate_sign_images")
async def options_generate_sign_images():
    """
    This function handles OPTIONS requests for the /generate_sign_images endpoint.
    It returns the allowed HTTP methods and headers for CORS.
    """
    return JSONResponse(
        content={"message": "OPTIONS request handled"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
    )

@app.post("/generate_sign_images")
async def generate_sign_images(request: Request):
    try:
        data = await request.json()
        word = data.get("word", "").upper()
        # Check if the word contains only alphabets, digits, and spaces
        if not word.replace(" ", "").isalnum():
            return JSONResponse(content={"error": "Invalid input. Please provide a word containing only alphabets, digits, and spaces."}, status_code=422)
        
        sign_images = []
        for letter in word:
            if letter in LETTER_TO_FILENAME:
                filename = LETTER_TO_FILENAME[letter]
                sign_image = load_sign_image(filename)
                # Convert numpy array to PIL Image
                sign_image_pil = Image.fromarray(sign_image)
                sign_images.append(sign_image_pil)  # Append PIL Image to the list
            else:
                continue
        
        
        # Combine all sign images horizontally
        combined_image = Image.new('RGB', (128 * len(sign_images), 128))
        for i, image in enumerate(sign_images):
            combined_image.paste(image, (i * 128, 0))
        
        # Save the combined image to a temporary file
        temp_image_path = "SignImage.png"
        combined_image.save(temp_image_path)
        
        # Construct the image URL with the /static prefix
        image_url = f"/static/SignImage.png"

        return {"image_url": image_url}
    
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

@app.post("/translate")
async def translate(
        files: List[UploadFile] = File(...)
):
    try:
        recognized_words = []
        for file in files:
            image = read_file_as_image(await file.read())
            recognized_word = recognize_word([image])
            recognized_words.append(recognized_word)
        
        combined_word = " ".join(recognized_words)
        return JSONResponse(content={"recognized_word": combined_word})
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return JSONResponse(content={"error": "Internal Server Error"})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
