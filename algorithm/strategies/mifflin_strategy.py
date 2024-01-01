from algorithm.strategies.bmr_strategy import BMRStrategy
from algorithm.ml.metafeatures.mifflin_model import MifflinModel
from algorithm.ml.data_processing import DataProcessor
from algorithm.ml.meta_feature_manager import MetaFeatureManager

class MifflinStJeorStrategy(BMRStrategy):
    def calculate_bmr(self, user_data: dict) -> float:
        data_processor = DataProcessor(user_data).bmr
        meta_feature_manager = MetaFeatureManager()
        meta_feature_manager.add_meta_feature(MifflinModel())
        result = meta_feature_manager.apply_meta_features(data_processor)

        return result.iloc[0, 0]
