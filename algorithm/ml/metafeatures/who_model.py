from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_age_category
import numpy as np
import pandas as pd

class WhoModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        WHO = {
            "Male": {
                "<10": np.nan,
                "10-18": lambda row: 16.6 * row['weight'] + 0.77 * row['height'] + 572,
                "18-30": lambda row: 15.4 * row['weight'] - 0.27 * row['height'] + 717,
                "30-60": lambda row: 11.3 * row['weight'] + 0.16 * row['height'] + 901,
                ">60": lambda row: 8.8 * row['weight'] + 11.28 * row['height'] - 1071
            },
            "Female": {
                "<10": np.nan,
                "10-18": lambda row: 7.4 * row['weight'] + 4.82 * row['height'] + 217,
                "18-30": lambda row: 13.3 * row['weight'] + 3.34 * row['height'] + 35,
                "30-60": lambda row: 8.7 * row['weight'] - 0.25 * row['height'] + 865,
                ">60": lambda row: 9.2 * row['weight'] + 6.37 * row['height'] - 302
            }
        }
        return data.apply(lambda row: process_age_category(row, WHO), axis=1)