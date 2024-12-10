import uuid
import logging 
from datetime import datetime
from flask import request, jsonify, current_app
from services.inference_service import predict_food_recommendations
from services.store_data import store_data
from services.get_all_data import get_all_data

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)
def post_predict_handler():
    try:
        payload = request.get_json()
        logging.debug("Payload received: %s", payload)

        model = current_app.config["model"]
        logging.debug("Model loaded: %s", model)

        allergens = payload.get("allergens")
        ingredients = payload.get("ingredients")
        last_order = payload.get("lastOrder")
        category = payload.get("category")

        logging.debug("Allergens: %s, Ingredients: %s, Last Order: %s, Category: %s",
                      allergens, ingredients, last_order, category)

        recommendations = predict_food_recommendations(model, {
            "user_allergens": allergens,
            "user_last_order": last_order,
            "food_category": category,
            "food_ingredients": ingredients
        })

        logging.debug("Recommendations: %s", recommendations)

        record_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        data = {
            "id": record_id,
            "recommendations": recommendations,
            "createdAt": created_at
        }

        store_data(record_id, data)
        logging.debug("Data stored in Firestore.")

        response = {
            "status": "success",
            "message": "Menu recommendations generated successfully",
            "data": data
        }

        return jsonify(response), 201

    except Exception as e:
        logging.error("Error in post_predict_handler: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

def get_predict_histories_handler():
    all_data = get_all_data()

    formatted_data = [
        {
            "id": doc.id,
            "history": {
                "recommendations": doc.to_dict().get("recommendations"),
                "createdAt": doc.to_dict().get("createdAt"),
                "id": doc.id
            }
        }
        for doc in all_data
    ]

    response = {"status": "success", "data": formatted_data}
    return jsonify(response), 200
