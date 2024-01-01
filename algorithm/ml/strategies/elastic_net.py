from __init__ import BaseModelTrainingStrategy
from sklearn.linear_model import ElasticNet
import joblib

class ElasticNetTrainingStrategy(BaseModelTrainingStrategy):
    def train(self, features, response):
        meta_model = ElasticNet()
        meta_model.fit(features, response)
        return meta_model

    def save_model(self, model, scaler):
        joblib.dump(model, 'bmr_model.pkl')
        joblib.dump(scaler, 'scaler.pkl')
