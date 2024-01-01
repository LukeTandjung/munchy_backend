from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_age_category
import pandas as pd

class HenryOneModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        henry_one = {
            "Male": {
                "0-3": lambda row: 61.0 * row['weight'] - 33.7,
                "3-10": lambda row: 23.3 * row['weight'] + 514,
                "10-18": lambda row: 18.4 * row['weight'] + 581,
                "18-30": lambda row: 16.0 * row['weight'] + 545,
                "30-60": lambda row: 14.2 * row['weight'] + 593,
                ">60": lambda row: 13.5 * row['weight'] + 514,
            },
            "Female": {
                "0-3": lambda row: 58.9 * row['weight'] - 23.1,
                "3-10": lambda row: 20.1 * row['weight'] + 507,
                "10-18": lambda row: 11.1 * row['weight'] + 761,
                "18-30": lambda row: 13.1 * row['weight'] + 558,
                "30-60": lambda row: 9.74 * row['weight'] + 694,
                ">60": lambda row: 10.1 * row['weight'] + 569
            }
        }
        return data.apply(lambda row: process_age_category(row, henry_one), axis=1)