from algorithm.calculate_nutrition.abstract_nutrition_weight import AbstractNutritionWeight
from algorithm.calculate_nutrition.protein_weight import ProteinWeight
from algorithm.calculate_nutrition.fats_weight import FatsWeight


class CarbohydratesWeight(AbstractNutritionWeight):
    def compute(self, user_data: dict, user_bmr: float) -> float:
        protein_weight = ProteinWeight()
        protein = protein_weight.compute(user_data = user_data, user_bmr = user_bmr)
        fats_weight = FatsWeight()
        fats = fats_weight.compute(user_data = user_data, user_bmr = user_bmr)
        carbohydrates = (user_bmr - 4 * protein - 9 * fats) / 4
        
        return carbohydrates