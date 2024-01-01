from abc import ABC, abstractmethod

class BMRStrategy(ABC):
    @abstractmethod
    def calculate_bmr(self, user_data):
        pass
