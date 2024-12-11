import os
import tensorflow as tf
import requests

def load_model(model_url_or_path):
     # Check if the path is a URL or local file
    if model_url_or_path.startswith("https://"):
        response = requests.get(model_url_or_path)
        if response.status_code == 200:
            # Save the model temporarily
            temp_model_path = "/tmp/temp_model.h5"
            with open(temp_model_path, "wb") as f:
                f.write(response.content)
            model_path = temp_model_path
        else:
            raise Exception(f"Failed to download model from {model_url_or_path}. Status code: {response.status_code}")
    else:
        model_path = model_url_or_path
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

    
    # Determine model type and load
    if model_path.endswith(".h5"):
        return tf.keras.models.load_model(model_path)  # Load Keras model
    elif model_path.endswith(".tflite"):
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
    else:
        raise ValueError(f"Unsupported model format for {model_path}")
