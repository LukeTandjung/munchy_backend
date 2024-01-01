from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import numpy as np
import pandas as pd

class RozaModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.apply(
            lambda row: 10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] + 5 
            if (18 <= row['age'] <= 86 and row['sex'] == "Male") 
            else (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] - 161 
            if (18 <= row['age'] <= 86 and row['sex'] == "Female") 
            else np.nan), axis=1)