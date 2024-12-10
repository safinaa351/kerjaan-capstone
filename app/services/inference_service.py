import numpy as np
import tensorflow as tf
from .exceptions import InputError
from services.food_list import food_list

def predict_food_recommendations(model, input_json):
    try:
        user_allergens = input_json["user_allergens"]
        user_last_order = input_json["user_last_order"]
        food_category = input_json["food_category"]
        food_ingredients = input_json["food_ingredients"]

        input_data = [user_allergens, user_last_order, food_category, food_ingredients]
        tensor_input = np.array([input_data], dtype=np.float32)

        # Set input tensor for TFLite interpreter
        input_details = model.get_input_details()
        output_details = model.get_output_details()

        model.set_tensor(input_details[0]['index'], tensor_input)
        model.invoke()

        # Get the result from the output tensor
        predictions = model.get_tensor(output_details[0]['index'])
        confidence_scores = predictions.flatten()

        recommended_foods = [
            {"food": food["name"], "confidence": score * 100}
            for food, score in zip(food_list, confidence_scores)
        ]
        recommended_foods.sort(key=lambda x: x["confidence"], reverse=True)

        return [food["food"] for food in recommended_foods]
    except Exception as e:
        raise InputError(f"An error occurred during prediction: {str(e)}")
