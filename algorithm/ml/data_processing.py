import pandas as pd

class DataProcessor:
    def __init__(self, data):
        if isinstance(data, dict):
            self._process_user_data(data)
        elif isinstance(data, pd.DataFrame):
            self._process_dataframe(data)
        else:
            raise ValueError("Data must be a dictionary or a pandas DataFrame")

    def _process_user_data(self, user_data):
        self.bmr = pd.DataFrame([{
            'sex': user_data["sex"],
            'age': int(user_data["age"]),
            'weight': float(user_data["weight"]),
            'height': float(user_data["height"]),
            'fat_percent': float(user_data["fat_percent"]),
            'bmi': round(10000 * (float(user_data["weight"]) / (float(user_data["height"]) ** 2)), 1),
            'ffm': (1 - (float(user_data["fat_percent"]) / 100)) * float(user_data["weight"])
        }])

    def _process_dataframe(self, data):
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