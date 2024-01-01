from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
from utils import process_age_category
import pandas as pd

class HenryTwoModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        henry_two = {
            "Male": {
                "0-3": lambda row: 28.2 * row['weight'] + 8.59 * row['height'] - 371,
                "3-10": lambda row: 15.1 * row['weight'] + 7.42 * row['height'] + 306,
                "10-18": lambda row: 15.6 * row['weight'] + 2.66 * row['height'] + 299,
                "18-30": lambda row: 14.4 * row['weight'] + 3.13 * row['height'] + 113,
                "30-60": lambda row: 11.4 * row['weight'] + 5.41 * row['height'] - 137,
                ">60": lambda row: 11.4 * row['weight'] + 5.41 * row['height'] - 256
            },
            "Female": {
                "0-3": lambda row: 30.4 * row['weight'] + 7.03 * row['height'] - 287,
                "3-10": lambda row: 15.9 * row['weight'] + 2.10 * row['height'] + 349,
                "10-18": lambda row: 9.40 * row['weight'] + 2.49 * row['height'] + 462,
                "18-30": lambda row: 10.4 * row['weight'] + 6.15 * row['height'] - 282,
                "30-60": lambda row: 8.18 * row['weight'] + 5.02 * row['height'] - 11.6,
                ">60": lambda row: 8.52 * row['weight'] + 4.21 * row['height'] + 10.7
            }
        }
        return data.apply(lambda row: process_age_category(row, henry_two), axis=1)

