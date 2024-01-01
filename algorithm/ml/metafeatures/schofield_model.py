from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_age_category
import pandas as pd

class SchofieldModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        schofield = {
            "Male": {
                "0-3": lambda row: 59.512 * row['weight'] - 30.4,
                "3-10": lambda row: 22.706 * row['weight'] + 504.3,
                "10-18": lambda row: 17.686 * row['weight'] + 658.2,
                "18-30": lambda row: 15.057 * row['weight'] + 692.2,
                "30-60": lambda row: 11.472 * row['weight'] + 873.1,
                ">60": lambda row: 11.711 * row['weight'] + 587.7,
            },
            "Female": {
                "0-3": lambda row: 58.317 * row['weight'] - 31.1,
                "3-10": lambda row: 20.315 * row['weight'] + 485.9,
                "10-18": lambda row: 13.384 * row['weight'] + 692.6,
                "18-30": lambda row: 14.818 * row['weight'] + 486.6,
                "30-60": lambda row: 8.126 * row['weight'] + 845.6,
                ">60": lambda row: 9.082 * row['weight'] + 658.5
            }
        }
        # Apply the function to each row in the DataFrame
        return data.apply(lambda row: process_age_category(row, schofield), axis=1)