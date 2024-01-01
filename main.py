from flask import Flask, request, jsonify
from algorithm.plan_diet import Diet
import pandas as pd

app = Flask(__name__)

@app.route("/<string:uid>/diet", methods=["POST"])
def create_user_diet(uid):
    request_data = request.get_json()
    user = {
        "uid": uid,
        "age": request_data["Age"],
        "sex": request_data["Sex"],
        "height": request_data["Height"],
        "weight": request_data["Weight"],
        "fat_percent": request_data["Body Fat"],
        "goal": request_data["Goal"],
        "meals": request_data["Meals"],
        "interval": request_data["Interval"],
        "cheat_meals": request_data["Cheat Meals"],
        "lifestyle": request_data["Lifestyle"],
        "activity": request_data["Activity"],
        "excluded_food": request_data["Excluded Food"]
    }
    diet = Diet(user)
    raw_data = diet.iterate()  # Placeholder for the diet plan logic
    user_diet_dict = {date.strftime("%d %B %Y"): value for date, value in raw_data.items()}
    return jsonify(user_diet_dict)

if __name__ == '__main__':
    app.run(threaded=True)
