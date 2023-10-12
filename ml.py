import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

class MetaFeatures:
    def __init__(self, data):
        if isinstance(data, dict):
            self.process_user_data(data)
        elif isinstance(data, pd.DataFrame):
            self.process_dataframe(data)

    def process_user_data(self, user_data):
        self.bmr = pd.DataFrame([{
            'sex': user_data["sex"],
            'age': int(user_data["age"]),
            'weight': float(user_data["weight"]),
            'height': float(user_data["height"]),
            'fat_percent': float(user_data["fat_percent"]),
            'bmi': round(10000 * (float(user_data["weight"]) / (float(user_data["height"]) ** 2)), 1),
            'ffm': (1 - (float(user_data["fat_percent"]) / 100)) * float(user_data["weight"])
        }])

    def process_dataframe(self, data):
        self.bmr = pd.DataFrame({
            'sex': data['Sex'],
            'age': data['Age'],
            'weight': data['Weight [kg]'],
            'height': data['Height [cm]'],
            'fat_percent': data['FM [%]'],
            'bmi': data['BMI [kg/m2]'],
            'ffm': data['FFM [kg]']
        })
        self.bmr_actual = data['iCal [kcal]']
    
    def process_age_category(self, row, function_dict, bmi = False, age_list = None):
        age_category = None
        for category in (list(function_dict[row['sex']].keys()) if bmi == False else age_list):
            if '-' in category:
                lower, upper = category.split('-')
                if int(lower) <= row['age'] <= int(upper):
                    age_category = category
                    break
            elif category.startswith('<') and row['age'] < int(category[1:]):
                age_category = category
                break
            elif category.startswith('>') and row['age'] > int(category[1:]):
                age_category = category
                break

        if bmi == False:
            selected_function = function_dict[row['sex']][age_category]
            if callable(selected_function):
                return selected_function(row)
            else:
                return np.nan
        else:
            return age_category

    def process_age_category_index(self, row, function_dict, bmi = False, age_list = None):
        age_category = None
        for i, category in enumerate((list(function_dict[row['sex']].keys()) if bmi == False else age_list)):
            if '-' in category:
                lower, upper = category.split('-')
                if int(lower) <= row['age'] <= int(upper):
                    age_category = i
                    break
            elif category.startswith('<') and row['age'] < int(category[1:]):
                age_category = i
                break
            elif category.startswith('>') and row['age'] > int(category[1:]):
                age_category = i
                break
        return age_category

        
    def process_bmi_category(self, row, function_dict):
        bmi_category = None
        for category in list(function_dict[row['sex']].keys()):
            if '-' in category:
                lower, upper = category.split('-')
                if float(lower) <= row['bmi'] <= float(upper):
                    bmi_category = category
                    break
            elif category.startswith('<') and row['bmi'] < float(category[1:]):
                bmi_category = category
                break
            elif category.startswith('>') and row['bmi'] > float(category[1:]):
                bmi_category = category
                break
        
        return bmi_category

    def harris_model(self):
        return self.bmr.apply(
            lambda row: 66.5 + (13.75 * row['weight']) + (5.003 * row['height']) - (6.755 * row['age']) 
            if (25.0 <= row['weight'] <= 124.9 and 151 <= row['height'] <= 200 and 21 <= row['age'] <= 70 and row['sex'] == 'Male') 
            else (655.1 + (9.563 * row['weight']) + (1.850 * row['height']) - (4.676 * row['age']) 
            if (25.0 <= row['weight'] <= 124.9 and 151 <= row['height'] <= 200 and 21 <= row['age'] <= 70 and row['sex'] == 'Female') 
            else np.nan), axis=1)

    def roza_model(self):
        return self.bmr.apply(
            lambda row: 10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] + 5 
            if (18 <= row['age'] <= 86 and row['sex'] == "Male") 
            else (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] - 161 
            if (18 <= row['age'] <= 86 and row['sex'] == "Female") 
            else np.nan), axis=1)

    def mifflin_model(self):
        return self.bmr.apply(
            lambda row: (80/100) * (1.5) * (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] + 5) 
            if (19 <= row['age'] <= 78 and row['sex'] == "Male") 
            else ((80/100) * (1.5) * (10.0 * row['weight'] + 6.25 * row['height'] - 5.0 * row['age'] - 161) 
            if (19 <= row['age'] <= 78 and row['sex'] == "Female") 
            else np.nan), axis=1)

    def schofield_model(self):
        schofield = {
            "Male": {
                "0-3": lambda row: 59.512 * row['weight'] - 30.4,
                "3-10": lambda row: 22.706 * row['weight'] + 504.3,
                "10-18": lambda row: 17.686 * row['weight'] + 658.2,
                "18-30": lambda row: 15.057 * row['weight'] + 692.2,
                "30-60": lambda row: 11.472 * row['weight'] + 873.1,
                ">60": lambda row: 11.711 * row['weight'] + 587.7,
            },
            "Female": {
                "0-3": lambda row: 58.317 * row['weight'] - 31.1,
                "3-10": lambda row: 20.315 * row['weight'] + 485.9,
                "10-18": lambda row: 13.384 * row['weight'] + 692.6,
                "18-30": lambda row: 14.818 * row['weight'] + 486.6,
                "30-60": lambda row: 8.126 * row['weight'] + 845.6,
                ">60": lambda row: 9.082 * row['weight'] + 658.5
            }
        }
        # Apply the function to each row in the DataFrame
        return self.bmr.apply(lambda row: self.process_age_category(row, schofield), axis=1)

    def WHO_model(self):
        WHO = {
            "Male": {
                "<10": np.nan,
                "10-18": lambda row: 16.6 * row['weight'] + 0.77 * row['height'] + 572,
                "18-30": lambda row: 15.4 * row['weight'] - 0.27 * row['height'] + 717,
                "30-60": lambda row: 11.3 * row['weight'] + 0.16 * row['height'] + 901,
                ">60": lambda row: 8.8 * row['weight'] + 11.28 * row['height'] - 1071
            },
            "Female": {
                "<10": np.nan,
                "10-18": lambda row: 7.4 * row['weight'] + 4.82 * row['height'] + 217,
                "18-30": lambda row: 13.3 * row['weight'] + 3.34 * row['height'] + 35,
                "30-60": lambda row: 8.7 * row['weight'] - 0.25 * row['height'] + 865,
                ">60": lambda row: 9.2 * row['weight'] + 6.37 * row['height'] - 302
            }
        }
        return self.bmr.apply(lambda row: self.process_age_category(row, WHO), axis=1)
      
    def owen_model(self):
        return self.bmr.apply(
            lambda row: 879 + (10.2 * row['weight']) 
            if (18 <= row['age'] <= 82 and row['sex'] == 'Male') 
            else (795 + (7.18 * row['weight']) 
            if (18 <= row['age'] <= 65 and row['sex'] == 'Female') 
            else np.nan), axis=1)

    def muller_model(self):
        return self.bmr.apply(
            lambda row: 238.846 * (0.02219 * row['weight'] + 0.02118 * row['height'] + 0.884 - 0.01191 * row['age'] + 1.233) 
            if (18.5 < row['bmi'] <= 25.0 and row['sex'] == 'Male') 
            else (238.846 * (0.02219 * row['weight'] + 0.02118 * row['height'] - 0.01191 * row['age'] + 1.233) 
            if (18.5 < row['bmi'] <= 25.0 and row['sex'] == 'Female') 
            else (238.846 * (0.04507 * row['weight'] + 1006 - 0.01553 * row['age'] + 3.407) 
            if (25.0 < row['bmi'] <= 30 and row['sex'] == 'Male') 
            else (238.846 * (0.04507 * row['weight'] - 0.01553 * row['age'] + 3.407) 
            if (25.0 < row['bmi'] <= 30 and row['sex'] == 'Female') 
            else np.nan))), axis=1)

    def henry_one_model(self):
        henry_one = {
            "Male": {
                "0-3": lambda row: 61.0 * row['weight'] - 33.7,
                "3-10": lambda row: 23.3 * row['weight'] + 514,
                "10-18": lambda row: 18.4 * row['weight'] + 581,
                "18-30": lambda row: 16.0 * row['weight'] + 545,
                "30-60": lambda row: 14.2 * row['weight'] + 593,
                ">60": lambda row: 13.5 * row['weight'] + 514,
            },
            "Female": {
                "0-3": lambda row: 58.9 * row['weight'] - 23.1,
                "3-10": lambda row: 20.1 * row['weight'] + 507,
                "10-18": lambda row: 11.1 * row['weight'] + 761,
                "18-30": lambda row: 13.1 * row['weight'] + 558,
                "30-60": lambda row: 9.74 * row['weight'] + 694,
                ">60": lambda row: 10.1 * row['weight'] + 569
            }
        }
        return self.bmr.apply(lambda row: self.process_age_category(row, henry_one), axis=1)

    def henry_two_model(self):
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
        return self.bmr.apply(lambda row: self.process_age_category(row, henry_two), axis=1)

    def DGEM_model(self):
        DGEM = {
            "Male": {
                "<20": np.nan,
                "20-30": lambda row: 25 * row['weight'],
                "30-70": lambda row: 22.5 * row['weight'],
                ">70": lambda row: 20 * row['weight']
            },
            "Female": {
                "<20": np.nan,
                "20-30": lambda row: 25 * row['weight'],
                "30-70": lambda row: 22.5 * row['weight'],
                ">70": lambda row: 20 * row['weight']
            }
        }
        return self.bmr.apply(lambda row: self.process_age_category(row, DGEM), axis=1)

    def BASAROTS_model(self):
        basarot = {
            "Male": {
                '<14': [30.6, 29.0, 28.7, 26.9, 25.6, 24.6, 22.6],
                '14-16.4': [30.0, 28.4, 27.0, 25.6, 24.4, 23.4, 21.6],
                '16.5-18.4': [28.4, 27.0, 25.7, 24.4, 23.2, 22.2, 20.2],
                '18.5-19.9': [27.1, 25.5, 24.6, 23.2, 22.8, 21.2, 19.6],
                '20-24.9': [25.4, 23.6, 23.1, 21.9, 21.1, 19.9, 19.0],
                '25-29.9': [22.8, 22.5, 21.3, 20.5, 19.8, 18.9, 18.3],
                '30-34.9': [19.6, 18.9, 17.8, 17.7, 16.6, 16.1, 15.2],
                '>35': [17.7, 17.1, 16.6, 15.9, 14.6, 14.9, 14.0]
            },
            "Female": {
                '<14': [31.4, 30.1, 28.9, 27.7, 26.4, 25.2, 24.0],
                '14-16.4': [28.3, 27.2, 26.1, 25.1, 24.1, 23.1, 22.6],
                '16.5-18.4': [26.2, 25.2, 24.3, 23.3, 22.4, 21.6, 20.5],
                '18.5-19.9': [23.7, 23.6, 22.9, 21.8, 21.5, 20.8, 20.1],
                '20-24.9': [22.6, 21.8, 21.2, 19.8, 19.2, 18.8, 18.2],
                '25-29.9': [20.2, 19.2, 18.7, 18.4, 17.8, 17.2, 16.8],
                '30-34.9': [16.4, 16.0, 16.0, 15.5, 14.8, 14.5, 14.5],
                '>35': [14.3, 14.3, 14.1, 13.3, 13.2, 13.3, 12.4]
            }
        }
        age_index = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100']
        def apply_func(row):
            bmi_category = self.process_bmi_category(row, basarot)
            age_category_index = self.process_age_category_index(row, basarot, bmi = True, age_list = age_index)
            return basarot[row['sex']][bmi_category][age_category_index] * row['weight']
        return self.bmr.apply(apply_func, axis=1)

    def katch_model(self):  
        return self.bmr.apply(lambda row: 370 + 21.6 * row['ffm'], axis=1)
    
    def meta(self):
        return pd.DataFrame({
        'harris_model': self.harris_model(),
        'roza_model': self.roza_model(), 
        'mifflin_model': self.mifflin_model(), 
        'schofield_model': self.schofield_model(), 
        'owen_model': self.owen_model(), 
        'WHO_model': self.WHO_model(), 
        'muller_model': self.muller_model(), 
        'henry_one_model': self.henry_one_model(), 
        'henry_two_model': self.henry_two_model(), 
        'DGEM_model': self.DGEM_model(), 
        'BASAROTS_model': self.BASAROTS_model(), 
        'katch_model': self.katch_model()
    })

class TrainBasalRateModel:
    def __init__(self):
        self.dataset = pd.read_excel("model_data.xlsx")
        base_model = MetaFeatures(self.dataset)
        self.features = base_model.bmr
        self.meta_features = base_model.meta()
        self.response = base_model.bmr_actual
        self.meta_model = None
    
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
        self.meta_model = ElasticNet()
        self.meta_model.fit(prepared_features, self.response)
        joblib.dump(self.meta_model, 'bmr_model.pkl')
        joblib.dump(scaler, 'scaler.pkl')

class PredictBasalRateModel:
    def __init__(self, user_data):
        base_model = MetaFeatures(user_data)
        self.features = base_model.bmr
        self.meta_features = base_model.meta()
        self.meta_model = joblib.load('bmr_model.pkl')
        self.scaler = joblib.load('scaler.pkl')
    
    def predict_model(self):
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

        # Standardize numeric columns using the same instance of scaler
        standardized_features = self.scaler.transform(combined_features)
        standardized_features_df = pd.DataFrame(standardized_features, columns=combined_features.columns)

        # One-hot encode the 'sex' column
        encoded_sex = pd.get_dummies(sex_feature, columns=['sex'])

        # Combine encoded sex feature with standardized features
        prepared_features = pd.concat([encoded_sex, standardized_features_df], axis=1)

        # Train the ElasticNet model. Save the Elastic Model and the Scaler into the file.
        predictions = self.meta_model.fit(prepared_features)[0]
        return predictions

# Run this block of code if you want to re-train the ElasticNet model with new data.
data = TrainBasalRateModel()
data.train_model()
