from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import numpy as np
import pandas as pd

class MullerModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.apply(
            lambda row: 238.846 * (0.02219 * row['weight'] + 0.02118 * row['height'] + 0.884 - 0.01191 * row['age'] + 1.233) 
            if (18.5 < row['bmi'] <= 25.0 and row['sex'] == 'Male') 
            else (238.846 * (0.02219 * row['weight'] + 0.02118 * row['height'] - 0.01191 * row['age'] + 1.233) 
            if (18.5 < row['bmi'] <= 25.0 and row['sex'] == 'Female') 
            else (238.846 * (0.04507 * row['weight'] + 1006 - 0.01553 * row['age'] + 3.407) 
            if (25.0 < row['bmi'] <= 30 and row['sex'] == 'Male') 
            else (238.846 * (0.04507 * row['weight'] - 0.01553 * row['age'] + 3.407) 
            if (25.0 < row['bmi'] <= 30 and row['sex'] == 'Female') 
            else np.nan))), axis=1)