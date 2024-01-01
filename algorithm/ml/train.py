import pandas as pd
from sklearn.preprocessing import StandardScaler
from data_processing import DataProcessor
from .strategies.base_model_training_strategy import BaseModelTrainingStrategy
from meta_feature_manager import MetaFeatureManager

class TrainBasalRateModel:
    def __init__(self, training_strategy: BaseModelTrainingStrategy, data_processor: DataProcessor, meta_feature_manager: MetaFeatureManager):
        self.dataset = pd.read_excel("model_data.xlsx")
        self.data_processor = data_processor
        self.meta_feature_manager = meta_feature_manager
        self.training_strategy = training_strategy

        # Process the dataset
        self.processed_data = self.data_processor.process_data(self.dataset)

        # Apply meta-features
        self.meta_features = self.meta_feature_manager.apply_meta_features(self.processed_data)
        self.response = self.processed_data['iCal [kcal]']

    def train_model(self):
        # Impute missing values in meta features with the mean of the row
        imputed_meta_features = self.meta_features.apply(lambda row: row.fillna(row.mean()), axis=1)

        # Identify columns based on data type
        numeric_columns = self.features.select_dtypes(include=['float64', 'int64']).columns
        categorical_columns = self.features.select_dtypes(include=['object']).columns

        # Split features based on data type
        numeric_features = self.features[numeric_columns]
        sex_feature = self.features[categorical_columns]

        # Combine numeric features and meta features
        combined_features = pd.concat([numeric_features, imputed_meta_features], axis=1)

        # Standardize numeric columns
        scaler = StandardScaler()
        standardized_features = scaler.fit_transform(combined_features)
        standardized_features_df = pd.DataFrame(standardized_features, columns=combined_features.columns)

        # One-hot encode the 'sex' column
        encoded_sex = pd.get_dummies(sex_feature, columns=['sex'])

        # Combine encoded sex feature with standardized features
        prepared_features = pd.concat([encoded_sex, standardized_features_df], axis=1)

        # Train the ElasticNet model. Save the Elastic Model and the Scaler into the file.
        self.meta_model = self.training_strategy.train(prepared_features, self.response)
        self.training_strategy.save_model(self.meta_model, scaler)

