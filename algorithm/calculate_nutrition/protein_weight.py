from algorithm.calculate_nutrition.abstract_nutrition_weight import AbstractNutritionWeight

class ProteinWeight(AbstractNutritionWeight):
    def compute(self, user_data: dict, user_bmr: float) -> float:
        protein = {
            "Male": lambda user_data: user_data["weight"] * (1 - user_data["fat_percent"] / 100) * (3.7044 - 3.528 * user_data["fat_percent"] / 100),
            "Female": lambda user_data: user_data["weight"] * (1 - user_data["fat_percent"] / 100) * (3.7485 - 2.75625 * user_data["fat_percent"] / 100)
        }
        return protein[user_data["sex"]](user_data)