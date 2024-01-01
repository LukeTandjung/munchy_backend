from algorithm.calculate_nutrition.abstract_nutrition_weight import AbstractNutritionWeight

class FatsWeight(AbstractNutritionWeight):
    def compute(self, user_data: dict, user_bmr: float) -> float:
        fats = {
            "Male": lambda user_data, user_bmr: (user_bmr * ((75 * user_data["fat_percent"] / 100 + 16.25) / 100)) / 9,
            "Female": lambda user_data, user_bmr: (user_bmr * ((50 * user_data["fat_percent"] + 15) / 100)) / 9
        }
        return fats[user_data["sex"]](user_data, user_bmr)
