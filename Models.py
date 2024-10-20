from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import numpy as np
import torch
import tensorflow as tf
import cv2


def KaludiPredications(imagepath):
    """Make predictions using the Kaludi model for food recognition and get the category"""

    # Inference of the Kaludi model from hugging face
    KaludiProcessor = AutoImageProcessor.from_pretrained("Kaludi/food-category-classification-v2.0")
    KaludiModel = AutoModelForImageClassification.from_pretrained("Kaludi/food-category-classification-v2.0")

    # Preprocess the image
    image__ = Image.open(imagepath).convert("RGB")

    # Gives the image to the Processor
    inputs = KaludiProcessor(images=image__, return_tensors="pt")

    # Make predictions
    with torch.no_grad():
        outputs = KaludiModel(**inputs)

    # Get predicted class
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

    # Get the class labels
    labels = KaludiModel.config.id2label

    # Return the predicted class label
    predicted_class_label = labels[predicted_class_idx]
    return predicted_class_label


def NaterawPredications(imagepath):
    """Make predictions using the Nateraw model for food recognition and get the recipe"""

    # Inference of the Nateraw model from hugging face
    NaterawProcessor = AutoImageProcessor.from_pretrained("nateraw/food")
    NaterawModel = AutoModelForImageClassification.from_pretrained("nateraw/food")

    # Preprocess the image
    image__ = Image.open(imagepath).convert("RGB")

    # Gives the image to the Processor
    inputs = NaterawProcessor(images=image__, return_tensors="pt")

    # Make predictions
    with torch.no_grad():
        outputs = NaterawModel(**inputs)

    # Get predicted class
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

    # Get the class labels
    labels = NaterawModel.config.id2label

    # Return the predicted class label
    predicted_class_label = labels[predicted_class_idx]
    return predicted_class_label


def FruVegPredictions(image_path):
    """Make predictions using the Our trained model for Fruit and Vegetable recognition"""

    # Loading the vegetables and fruits trained model
    FruVegModel = tf.keras.models.load_model('Trained_Model.keras')

    image = tf.keras.preprocessing.image.load_img(image_path , target_size=(64,64))
    input_array = tf.keras.preprocessing.image.img_to_array(image)
    input_array = np.array([input_array])
    predictions = FruVegModel.predict(input_array)

    result_index = np.argmax(predictions)
    class_names = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'papaya', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon'] # Define the Class_Names variable with a list of possible classifications
    return class_names[result_index]
