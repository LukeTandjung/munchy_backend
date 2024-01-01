from algorithm.ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import numpy as np
import pandas as pd

class MifflinModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.apply(
            lambda row: (80/100) * (1.5) * (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] + 5) 
            if (19 <= row['age'] <= 78 and row['sex'] == "Male") 
            else ((80/100) * (1.5) * (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] - 161) 
            if (19 <= row['age'] <= 78 and row['sex'] == "Female") 
            else np.nan), axis=1)