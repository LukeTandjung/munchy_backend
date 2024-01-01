from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_age_category
import numpy as np
import pandas as pd

class DgemModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        DGEM = {
            "Male": {
                "<20": np.nan,
                "20-30": lambda row: 25 * row['weight'],
                "30-70": lambda row: 22.5 * row['weight'],
                ">70": lambda row: 20 * row['weight']
            },
            "Female": {
                "<20": np.nan,
                "20-30": lambda row: 25 * row['weight'],
                "30-70": lambda row: 22.5 * row['weight'],
                ">70": lambda row: 20 * row['weight']
            }
        }
        return data.apply(lambda row: process_age_category(row, DGEM), axis=1)