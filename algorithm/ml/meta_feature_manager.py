from algorithm.ml.metafeatures.abstract_meta_feature import AbstractMetaFeature
import pandas as pd

class MetaFeatureManager:
    def __init__(self):
        self.meta_features = []

    def add_meta_feature(self, meta_feature: AbstractMetaFeature):
        self.meta_features.append(meta_feature)

    def apply_meta_features(self, data: pd.DataFrame) -> pd.DataFrame:
        results = {}

        for feature in self.meta_features:
            result = feature.compute(data)
            results[feature.__class__.__name__] = result
            
        return pd.DataFrame(results)