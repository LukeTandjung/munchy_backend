from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import numpy as np
import pandas as pd

class OwenModel(AbstractMetaFeature):
   def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.apply(
            lambda row: 879 + (10.2 * row['weight']) 
            if (18 <= row['age'] <= 82 and row['sex'] == 'Male') 
            else (795 + (7.18 * row['weight']) 
            if (18 <= row['age'] <= 65 and row['sex'] == 'Female') 
            else np.nan), axis=1)