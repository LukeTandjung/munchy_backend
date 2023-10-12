import requests
import math
import numpy as np
import pandas as pd
from scipy.optimize import LinearConstraint, milp, Bounds
from ml import PredictBasalRateModel
from datetime import date, datetime
# SERVER-SIDE CODE TO OPTIMISE DIET

class Algorithm:
    Foodbase = {}

    def __init__(self, user_data):
        self.name = user_data["name"]
        self.goal = user_data["goal"]
        self.target = user_data["target"]
        self.deadline = user_data["deadline"]
        self.num_meals = user_data["num_meals"]
        self.interval = user_data["interval"]
        self.num_cheat_meals = user_data["num_cheat_meals"]
        self.sex = user_data["sex"]
        self.age = int(user_data["age"])
        self.weight = float(user_data["weight"])
        self.height = float(user_data["height"])
        self.fat_percent = float(user_data["fat_percent"]) / 100
        self.bmi = 10000 * (self.weight / (self.height ** 2))
        self.ffm = (1 - self.fat_percent) * self.weight
        self.bmr = pd.DataFrame([{
            'sex': self.sex,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'fat_percent': self.fat_percent,
            'bmi': self.bmi,
            'ffm': self.ffm
        }])
        self.disorder = user_data["disorder"]
        self.lifestyle = user_data["lifestyle"]
        self.activity = user_data["activity"]
        self.health = user_data["health"]
        self.allergy = user_data["allergy"]
        self.food_menu_list = user_data["food_menu_list"]
        self.food_item = user_data["food_item"]
        self.user_data = user_data

    def calories(self):
        model = PredictBasalRateModel(self.user_data)
        bmr = model.predict_model(self.bmr)
        print(bmr)
        multiplier_table = {
            "Sedentary": {
                "Light exercise": 1.2,
                "Medium exercise": 1.3,
                "Heavy exercise": 1.5
            },
            "Lightly active": {
                "Light exercise": 1.4,
                "Medium exercise": 1.6,
                "Heavy exercise": 1.8
            },
            "Moderately active": {
                "Light exercise": 1.8,
                "Medium exercise": 1.9,
                "Heavy exercise": 2.0
            },
            "Highly active": {
                "Light exercise": 2.0,
                "Medium exercise": 2.1,
                "Heavy exercise": 2.2
            }
        }
        bmr_multiplier = multiplier_table[self.lifestyle][self.activity]
        calories = bmr * bmr_multiplier
        return calories

    def caloric_multiplier(self):
        user = Algorithm(self.users, self.chat_id)

        start_date = datetime.now().date()
        difference = self.deadline - start_date

        unknown_goal = {
            "Weight": {
                "Lose fat": lambda: self.weight * ((1 - self.fat_percent) / (1 - self.target_fat_percent)),
                "Gain muscle": lambda: self.weight * self.fat_percent / self.target_fat_percent,
                "Lose fat and gain muscle": lambda: self.weight,
                "Gain muscle and fat": lambda: self.weight + 5,
                "Maintain weight and health": lambda: self.weight
            },
            "Fat Percent": {
                "Lose fat": lambda: (self.weight / self.target_weight) * (self.fat_percent - 1) - 1,
                "Gain muscle": lambda: self.fat_percent * self.weight / self.target_weight,
                "Lose fat and gain muscle": lambda: self.fat_percent - 0.05,
                "Gain muscle and fat": lambda: self.fat_percent + 0.05,
                "Maintain weight and health": lambda: self.fat_percent
            },
            "Both": {
                "Lose fat": {
                    "Weight": lambda: self.fat_percent - 0.05,
                    "Fat Percent": lambda: self.weight * ((1 - self.fat_percent) / (1 - self.target_fat_percent))
                },
                "Gain muscle": {
                    "Weight": lambda: self.weight + 5,
                    "Fat Percent": lambda: self.weight * self.fat_percent / self.target_weight
                },
                "Lose fat and gain muscle": {
                    "Weight": lambda: self.weight,
                    "Fat Percent": lambda: self.fat_percent - 0.05
                },
                "Gain muscle and fat": {
                    "Weight": lambda: self.weight + 5,
                    "Fat Percent": lambda: (self.fat_percent * self.weight + 3) / self.target_weight
                },
                "Maintain weight and health": {
                    "Weight": lambda: self.weight,
                    "Fat Percent": lambda: self.fat_percent
                }
            }
        }

        if self.target_weight == "-" and self.target_fat_percent != "-":
            self.target_weight = unknown_goal["Weight"][self.goal]()
        elif self.target_weight != "-" and self.target_fat_percent == "-":
            self.target_fat_percent = unknown_goal["Fat Percent"][self.goal]()
        elif self.target_weight == "-" and self.target_fat_percent == "-":
            self.target_weight = unknown_goal["Both"][self.goal]["Weight"]()
            self.target_fat_percent = unknown_goal["Both"][self.goal]["Fat Percent"]()
        
        fat_mass_diff = self.target_weight * self.target_fat_percent - self.weight * self.fat_percent
        fat_free_mass_diff = self.target_weight * (1 - self.target_fat_percent) - self.weight * (1 - self.fat_percent)
        caloric_multiplier = (9440.5 * fat_mass_diff + 1814.6 * fat_free_mass_diff)/(user.calories * difference.days)

        caloric_multipliers = [
            (lambda: self.goal == "Lose fat" and (caloric_multiplier >= 1 or caloric_multiplier < 0.8), 0.8),
            (lambda: self.goal == "Gain muscle" and (caloric_multiplier < 1 or caloric_multiplier > 1.2), 1.2),
            (lambda: self.goal == "Lose fat and gain muscle" and caloric_multiplier != 1, 1),
            (lambda: self.goal == "Gain muscle and fat" and (caloric_multiplier < 1 or caloric_multiplier > 1.2), 1.2),
            (lambda: self.goal == "Maintain weight and health" and (caloric_multiplier >= 1 or caloric_multiplier < 0.9), 0.9)
        ]

        for condition, value in caloric_multipliers:
            if condition():
                return value
            else:
                return caloric_multiplier
    
    def get_dishes(self):

        total_calories = Algorithm.calories() * Algorithm.caloric_multiplier()
        app_id = "f4da6428"
        app_key = "e90d4a8810e64798659d4b3f3fbcbeab"
        number_search_results = 3
        health = ""
        diet = ""

        def append_api_parameter(diet, health, api_diet_params, api_health_params):
            if api_diet_params != None:
                diet = diet + "".join(params for params in api_diet_params if params not in diet)
            if api_health_params != None:
                health = health + "".join(params for params in api_health_params if params not in health)
            return diet, health
        
        health_conditions = {
            "Heart Disease or Stroke": {
                "api_diet_params": ["&diet=low-fat", "&diet=low-sodium", "&diet=high-fibre"],
                "api_health_params": ["&health=low-sugar"]
            },
            "Diabetes": {
                "api_diet_params": ["&diet=low-sodium", "&diet=low-fat"],
                "api_health_params": ["&health=low-sugar", "&health=sugar-conscious"]
            },
            "Gout": {
                "api_diet_params": ["&diet=low-fat"],
                "api_health_params": ["&health=red-meat-free", "&health=alcohol-free"]
            },
            "High Cholesterol": {
                "api_diet_params": ["&diet=low-fat"],
                "api_health_params": ["&health=low-sugar", "&health=alcohol-free"]
            }
        }

        allergies = {
            "Shellfish": {
                "api_diet_params": None,
                "api_health_params": ["&health=crustacean-free", "&health=mollusk-free", "&health=shellfish-free"]
            },
            "Nuts or Tree Nuts": {
                "api_diet_params": None,
                "api_health_params": ["&health=tree-nut-free", "&health=peanut-free"]
            },
            "Milk": {
                "api_diet_params": None,
                "api_health_params": ["&health=dairy-free"]
            },
            "Eggs": {
                "api_diet_params": None,
                "api_health_params": ["&health=egg-free"]
            }
        }

        for condition in self.health:
            if condition in health_conditions:
                api_diet_params = health_conditions[condition].get('api_diet_params')
                api_health_params = health_conditions[condition].get('api_health_params')
                diet, health = append_api_parameter(diet, health, api_diet_params, api_health_params)

        for allergy in self.allergies:
            if allergy in allergies:
                api_diet_params = allergies[allergy].get('api_diet_params')
                api_health_params = allergies[allergy].get('api_health_params')
                diet, health = append_api_parameter(diet, health, api_diet_params, api_health_params)

        number_meals = {
            "Two or less": ["&mealType=lunch", "&mealType=dinner"],
            "Three": ["&mealType=breakfast", "&mealType=lunch", "&mealType=dinner"],
            "Four": ["&mealType=breakfast", "&mealType=lunch", "&mealType=dinner", "&mealType=snack"]
        }
        for meals in number_meals[self.number_meals]:
            for food in self.food_item:
                url = f"https://api.edamam.com/search?q={food}&app_id={app_id}&app_key={app_key}&from=0&to={number_search_results - 1}" + health + diet + meals
                dishes_same_type = []
                try:
                    response = requests.get(url)
                    recipe = response.json()
                    def proportion_reformat(j):
                        number_meals = {
                            "Two or less": {
                                "&mealType=lunch": lambda: math.floor((1/2) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=dinner": lambda: math.floor((1/2) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"]
                            },  
                            "Three": {
                                "&mealType=breakfast": lambda: math.floor((1/4) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=lunch": lambda: math.floor((3/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=dinner": lambda: math.floor((3/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"]
                            },
                            "Four": {
                                "&mealType=breakfast": lambda: math.floor((1/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=lunch": lambda: math.floor((3/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=dinner": lambda: math.floor((3/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                                "&mealType=snack": lambda: math.floor((1/8) * total_calories * recipe["hits"][j]["recipe"]["yield"] / recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"]) / recipe["hits"][j]["recipe"]["yield"],
                            }
                        }
                        return number_meals[self.number_meals][meals]
                        
                    def ingredient_reformat(i, j):
                        quantity = recipe["hits"][j]["recipe"]["ingredients"][i]["quantity"] * proportion_reformat(j)
                        measure = recipe["hits"][j]["recipe"]["ingredients"][i]["measure"]
                        food = recipe["hits"][j]["recipe"]["ingredients"][i]["food"]

                        return " ".join(quantity, measure, food)

                    dishes = [{
                        "Dish Name": recipe["hits"][j]["recipe"]["label"],
                        "Dish Image": recipe["hits"][j]["recipe"]["image"],
                        "Dish Type": recipe["hits"][j]["recipe"]["mealType"],
                        "Contains": recipe["hits"][j]["recipe"]["cautions"],
                        "Dish Source": recipe["hits"][j]["recipe"]["url"],
                        "Ingredients": [ingredient_reformat(i, j) for i in range(len(recipe["hits"][j]["recipe"]["ingredientLines"]))],
                        "Quantity": recipe["hits"][j]["recipe"]["yield"] * proportion_reformat(j),
                        "Calories": recipe["hits"][j]["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"] * proportion_reformat(j),
                        "Carbohydrates": recipe["hits"][j]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"] * proportion_reformat(j),
                        "Protein": recipe["hits"][j]["recipe"]["totalNutrients"]["PROCNT"]["quantity"] * proportion_reformat(j),
                        "Fats": recipe["hits"][j]["recipe"]["totalNutrients"]["FAT"]["quantity"] * proportion_reformat(j)
                    } for j in range(number_search_results)]
                except requests.exceptions.RequestException as e:
                    raise e
                
                dishes_same_type += dishes
            self.Foodbase[meals.replace("&mealType=", "")] = dishes_same_type

    def optimise(self):
        
        total_calories = Algorithm.calories(self) * Algorithm.caloric_multiplier(self)
    
        if self.sex == "Male":
            protein = self.weight * (1 - self.fat_percent) * (3.7044 - 3.528 * self.fat_percent)
            fat = (total_calories * ((75 * self.fat_percent + 16.25)/100)) / 9
            carbohydrates = (total_calories - 4 * protein - 9 * fat) / 4
        elif self.sex == "Female":
            protein = self.weight * (1 - self.fat_percent) * (3.7485 - 2.75625 * self.fat_percent)
            fat = (total_calories * ((50 * self.fat_percent + 15)/100)) / 9
            carbohydrates = (total_calories - 4 * protein - 9 * fat) / 4
        
        number_meals = {
            "Two or less": ["lunch", "dinner"],
            "Three": ["breakfast", "lunch", "dinner"],
            "Four": ["breakfast", "lunch", "dinner", "snack"]
        }
        dietlist_calories = [self.Foodbase[meals][i]["Calories"] for meals in number_meals[self.number_meals] for i in range(len(self.Foodbase[meals]))]
        dietlist_carbohydrates = [self.Foodbase[meals][i]["Carbohydrates"] for meals in number_meals[self.number_meals] for i in range(len(self.Foodbase[meals]))]
        dietlist_protein = [self.Foodbase[meals][i]["Protein"] for meals in number_meals[self.number_meals] for i in range(len(self.Foodbase[meals]))]
        dietlist_fat = [self.Foodbase[meals][i]["Fats"] for meals in number_meals[self.number_meals] for i in range(len(self.Foodbase[meals]))]
        c = -np.array(dietlist_calories)
        bounds = Bounds([0] * len(dietlist_calories), [1] * len(dietlist_calories))
        integrality = np.ones_like(c)

        if self.number_meals == "Two or less":
            user_macros = np.array([total_calories, carbohydrates, protein, fat, (1 / 2) * total_calories, (1 / 2) * total_calories, 1, 1])
            calories_lunch = [self.Foodbase["lunch"][i]["Calories"] for i in range(len(self.Foodbase["lunch"]))] + [0] * len(self.Foodbase["dinner"])
            calories_dinner = [0] * len(self.Foodbase["lunch"]) + [self.Foodbase["dinner"][i]["Calories"] for i in range(len(self.Foodbase["dinner"]))]
            dietlist_lunch = [1] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"])
            dietlist_dinner = [0] * len(self.Foodbase["lunch"]) + [1] * len(self.Foodbase["dinner"])
            A = np.array(dietlist_calories, dietlist_carbohydrates, dietlist_protein, dietlist_fat, calories_lunch, calories_dinner, dietlist_lunch, dietlist_dinner)
            b_l = np.full_like(user_macros, 0)
            constraints = LinearConstraint(A, b_l, user_macros)

        elif self.number_meals == "Three":
            user_macros = np.array([total_calories, carbohydrates, protein, fat, (1 / 4) * total_calories, (3 / 8) * total_calories, (3 / 8) * total_calories, 1, 1, 1])
            calories_breakfast = [self.Foodbase["breakfast"][i]["Calories"] for i in range(len(self.Foodbase["breakfast"]))] + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"])
            calories_lunch = [0] * len(self.Foodbase["breakfast"]) + [self.Foodbase["lunch"][i]["Calories"] for i in range(len(self.Foodbase["lunch"]))] + [0] * len(self.Foodbase["dinner"])
            calories_dinner = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [self.Foodbase["dinner"][i]["Calories"] for i in range(len(self.Foodbase["dinner"]))]
            dietlist_breakfast = [1] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"])
            dietlist_lunch = [0] * len(self.Foodbase["breakfast"]) + [1] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"])
            dietlist_dinner = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [1] * len(self.Foodbase["dinner"])
            A = np.array(dietlist_calories, dietlist_carbohydrates, dietlist_protein, dietlist_fat, calories_breakfast, calories_lunch, calories_dinner, dietlist_breakfast, dietlist_lunch, dietlist_dinner)
            b_l = np.full_like(user_macros, 0)
            constraints = LinearConstraint(A, b_l, user_macros)

        else:
            user_macros = np.array([total_calories, carbohydrates, protein, fat, (1 / 8) * total_calories, (3 / 8) * total_calories, (3 / 8) * total_calories, (3 / 8) * total_calories, 1, 1, 1, 1])
            calories_breakfast = [self.Foodbase["breakfast"][i]["Calories"] for i in range(len(self.Foodbase["breakfast"]))] + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"]) + [0] * len(self.Foodbase["snack"])
            calories_lunch = [0] * len(self.Foodbase["breakfast"]) + [self.Foodbase["lunch"][i]["Calories"] for i in range(len(self.Foodbase["lunch"]))] + [0] * len(self.Foodbase["dinner"]) + [0] * len(self.Foodbase["snack"])
            calories_dinner = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [self.Foodbase["dinner"][i]["Calories"] for i in range(len(self.Foodbase["dinner"]))] + [0] * len(self.Foodbase["snack"])
            calories_snack = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"]) + [self.Foodbase["snack"][i]["Calories"] for i in range(len(self.Foodbase["snack"]))]
            dietlist_breakfast = [1] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"]) + [0] * len(self.Foodbase["snack"])
            dietlist_lunch = [0] * len(self.Foodbase["breakfast"]) + [1] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"]) + [0] * len(self.Foodbase["snack"])
            dietlist_dinner = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [1] * len(self.Foodbase["dinner"]) + [0] * len(self.Foodbase["snack"])
            dietlist_snack = [0] * len(self.Foodbase["breakfast"]) + [0] * len(self.Foodbase["lunch"]) + [0] * len(self.Foodbase["dinner"]) + [1] * len(self.Foodbase["snack"])
            A = np.array(dietlist_calories, dietlist_carbohydrates, dietlist_protein, dietlist_fat, calories_breakfast, calories_lunch, calories_dinner, calories_snack, dietlist_breakfast, dietlist_lunch, dietlist_dinner, dietlist_snack)
            b_l = np.full_like(user_macros, 0)
            constraints = LinearConstraint(A, b_l, user_macros)
        
        result = milp(c = c, constraints = constraints, bounds = bounds, integrality = integrality)
        combined_list = self.Foodbase["breakfast"] + self.Foodbase["lunch"] + self.Foodbase["dinner"] + self.Foodbase["snack"]
        selected_meals = [meal for i, meal in enumerate(combined_list) if result.x[i] == 1]
        return selected_meals


 