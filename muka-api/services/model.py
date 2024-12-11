import tensorflow as tf
import io
from PIL import Image
import numpy as np
from google.cloud import storage
from services.cache import set_cached_model

# Global variable for the model cache
MODEL = None

def load_model_from_gcs(model_path):
    client = storage.Client()
    bucket = client.bucket(model_path.split('/')[2])
    blob = bucket.blob('/'.join(model_path.split('/')[3:]))
    model_data = blob.download_as_string()
    model = tf.keras.models.load_model(io.BytesIO(model_data))
    set_cached_model(model)
    return model

def load_model_from_gcs(model_path):
    #model_path format: 'capstone-c242-ps370.appspot.com/ml-models/face-recognition/siamesemodel.h5'
    client = storage.Client()
    bucket_name = model_path.split('/')[0]
    blob_path = '/'.join(model_path.split('/')[1:])
    
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    
    model_data = blob.download_as_string()
    model = tf.keras.models.load_model(io.BytesIO(model_data))
    
    set_cached_model(model)
    return model

def load_model():
    global MODEL
    if MODEL is None:
        # Ganti dengan path model Anda
        MODEL = load_model_from_gcs('https://storage.googleapis.com/capstone-c242-ps370.appspot.com/ml-models/face-recognition/siamesemodel.h5')
    return MODEL

def compare_faces(test_image, reference_image, model=None):
    # Proses gambar dan bandingkan menggunakan model
    test_image = np.array(Image.open(test_image))
    reference_image = np.array(Image.open(reference_image))
    
    # Implementasikan face recognition logic di sini
    result = model.predict([test_image, reference_image])  # Ini contoh, sesuaikan dengan model Anda
    if result > 0.9:  # Ambil threshold sesuai model
        return {"message": "user sesuai, silakan lanjut proses berikutnya"}
    else:
        return {"message": "user tidak sesuai!"}
