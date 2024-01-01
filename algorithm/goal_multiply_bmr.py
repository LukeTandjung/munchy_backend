def goal_multiply_bmr(user_data: dict, bmr: float) -> float:
    # This needs to be rewritten for the specific parameters!
    multiplier_table = {
        "Lose fat": 0.85,
        "Gain muscle": 1.15,
        "Lose fat and gain muscle": 1,
        "Gain muscle and fat": 1.2,
        "Maintain weight and health": 0.95
    }
    bmr_multiplier = multiplier_table[user_data["goal"]]
    calories = bmr * bmr_multiplier
    return calories