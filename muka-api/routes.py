from flask import Blueprint, request, jsonify
from services.model import compare_faces

face_api = Blueprint('face_api', __name__)

@face_api.route('/verify', methods=['POST'])
def verify_faces():
    
    test_image = request.files.get('test_image')
    reference_image = request.files.get('reference_image')
    
    if not test_image or not reference_image:
        return jsonify({"message": "test_image dan reference_image dibutuhkan!"}), 400
    
    result = compare_faces(test_image, reference_image)
    return jsonify(result)
