from flask import Flask, request, jsonify
from services.model import load_model, compare_faces
from services.cache import get_cached_model

app = Flask(__name__)



# Load model once and cache it
model = get_cached_model()

@app.route('/verify', methods=['POST'])
def verify_faces():
    test_image = request.files.get('test_image')
    reference_image = request.files.get('reference_image')
    
    if not test_image or not reference_image:
        return jsonify({"message": "test_image dan reference_image dibutuhkan!"}), 400
    
    # Process images and compare faces
    result = compare_faces(test_image, reference_image, model)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
