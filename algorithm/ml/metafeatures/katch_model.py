from ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import pandas as pd

class KatchModel(AbstractMetaFeature):
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:  
        return data.apply(lambda row: 370 + 21.6 * row['ffm'], axis=1)
    
    