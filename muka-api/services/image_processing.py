import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO
from tensorflow.keras.preprocessing import image

def process_image(image_file):
    """Proses gambar yang diupload menjadi array numpy yang siap digunakan untuk model"""
    img = Image.open(image_file)
    img = img.convert('RGB')  # Pastikan gambar dalam format RGB
    img = img.resize((224, 224))  # Ubah ukuran gambar (sesuaikan dengan input model Anda)
    img_array = np.array(img)  # Ubah gambar menjadi array numpy
    
    # Normalisasi gambar sesuai dengan yang diharapkan model (misalnya, pixel dalam rentang 0-1)
    img_array = img_array / 255.0  # Jika model Anda mengharapkan gambar dalam rentang 0-1
    return img_array

def compare_faces(test_image, reference_image, model):
    """Bandingkan dua gambar dan cek apakah sesuai atau tidak"""
    
    # Proses gambar yang diterima
    test_image_processed = process_image(test_image)
    reference_image_processed = process_image(reference_image)

    # Perlu tambahkan dimensi untuk batch, TensorFlow mengharapkan input dengan dimensi [batch_size, height, width, channels]
    test_image_processed = np.expand_dims(test_image_processed, axis=0)
    reference_image_processed = np.expand_dims(reference_image_processed, axis=0)
    
    # Prediksi perbandingan wajah
    result = model.predict([test_image_processed, reference_image_processed])

    # Misalnya, jika model mengembalikan skor atau vektor perbandingan
    # Anda bisa menggunakan threshold tertentu untuk memutuskan apakah kedua gambar cocok
    if result[0] > 0.9:  # Threshold bisa disesuaikan dengan model
        return {"message": "user sesuai, silakan lanjut proses berikutnya"}
    else:
        return {"message": "user tidak sesuai!"}
