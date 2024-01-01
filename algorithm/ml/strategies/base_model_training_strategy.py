from abc import ABC, abstractmethod

class BaseModelTrainingStrategy(ABC):
    @abstractmethod
    def train(self, features, response):
        pass

    @abstractmethod
    def save_model(self, model, scaler):
        pass
