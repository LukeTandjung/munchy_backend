from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_bmi_category, process_age_category_index
import pandas as pd

class BasarotModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        basarot = {
            "Male": {
                '<14': [30.6, 29.0, 28.7, 26.9, 25.6, 24.6, 22.6],
                '14-16.4': [30.0, 28.4, 27.0, 25.6, 24.4, 23.4, 21.6],
                '16.5-18.4': [28.4, 27.0, 25.7, 24.4, 23.2, 22.2, 20.2],
                '18.5-19.9': [27.1, 25.5, 24.6, 23.2, 22.8, 21.2, 19.6],
                '20-24.9': [25.4, 23.6, 23.1, 21.9, 21.1, 19.9, 19.0],
                '25-29.9': [22.8, 22.5, 21.3, 20.5, 19.8, 18.9, 18.3],
                '30-34.9': [19.6, 18.9, 17.8, 17.7, 16.6, 16.1, 15.2],
                '>35': [17.7, 17.1, 16.6, 15.9, 14.6, 14.9, 14.0]
            },
            "Female": {
                '<14': [31.4, 30.1, 28.9, 27.7, 26.4, 25.2, 24.0],
                '14-16.4': [28.3, 27.2, 26.1, 25.1, 24.1, 23.1, 22.6],
                '16.5-18.4': [26.2, 25.2, 24.3, 23.3, 22.4, 21.6, 20.5],
                '18.5-19.9': [23.7, 23.6, 22.9, 21.8, 21.5, 20.8, 20.1],
                '20-24.9': [22.6, 21.8, 21.2, 19.8, 19.2, 18.8, 18.2],
                '25-29.9': [20.2, 19.2, 18.7, 18.4, 17.8, 17.2, 16.8],
                '30-34.9': [16.4, 16.0, 16.0, 15.5, 14.8, 14.5, 14.5],
                '>35': [14.3, 14.3, 14.1, 13.3, 13.2, 13.3, 12.4]
            }
        }

        age_index = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100']

        def apply_func(row):
            bmi_category = process_bmi_category(row, basarot)
            age_category_index = process_age_category_index(row, basarot, bmi = True, age_list = age_index)
            return basarot[row['sex']][bmi_category][age_category_index] * row['weight']
        
        return data.apply(apply_func, axis=1)