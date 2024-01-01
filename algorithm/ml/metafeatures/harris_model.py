from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import numpy as np
import pandas as pd

class HarrisModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.apply(
            lambda row: 66.5 + (13.75 * row['weight']) + (5.003 * row['height']) - (6.755 * row['age']) 
            if (25.0 <= row['weight'] <= 124.9 and 151 <= row['height'] <= 200 and 21 <= row['age'] <= 70 and row['sex'] == 'Male') 
            else (655.1 + (9.563 * row['weight']) + (1.850 * row['height']) - (4.676 * row['age']) 
            if (25.0 <= row['weight'] <= 124.9 and 151 <= row['height'] <= 200 and 21 <= row['age'] <= 70 and row['sex'] == 'Female') 
            else np.nan), axis=1)