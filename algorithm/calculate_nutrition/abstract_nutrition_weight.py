from abc import ABC, abstractmethod

class AbstractNutritionWeight(ABC):
    @abstractmethod
    def compute(self, user_data: dict, user_bmr: float) -> float:
        pass