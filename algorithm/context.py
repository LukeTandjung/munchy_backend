from algorithm.strategies.bmr_strategy import BMRStrategy

class BMRContext:
    def __init__(self, strategy: BMRStrategy):
        self.strategy = strategy

    def calculate_bmr(self, user_data: dict) -> float:
        return self.strategy.calculate_bmr(user_data)
