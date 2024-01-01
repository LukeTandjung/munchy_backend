def activity_lifestyle_multiply_bmr(user_data: dict, bmr: float) -> float:
    # This needs to be rewritten for the specific parameters!
    multiplier_table = {
        "Sedentary": {
            "Light exercise": 1.2,
            "Medium exercise": 1.3,
            "Heavy exercise": 1.5
        },
        "Lightly active": {
            "Light exercise": 1.4,
            "Medium exercise": 1.6,
            "Heavy exercise": 1.8
        },
        "Moderately active": {
            "Light exercise": 1.8,
            "Medium exercise": 1.9,
            "Heavy exercise": 2.0
        },
        "Highly active": {
            "Light exercise": 2.0,
            "Medium exercise": 2.1,
            "Heavy exercise": 2.2
        }
    }
    bmr_multiplier = multiplier_table[user_data["lifestyle"]][user_data["activity"]]
    calories = bmr * bmr_multiplier
    return calories