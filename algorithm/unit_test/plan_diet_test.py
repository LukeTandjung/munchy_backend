from plan_diet import Diet
from hypothesis import given, strategies as st
import random

# Creating a list of food items, excluding the general food category terms

food_items = [
    "Pinto Beans", "Snap Beans", "Black Beans", "White Beans",
    "Hash Browns", "Hamburger Bun", "Biscuits", "Pie Crust", "Hash Brown", "Panko Crumbs",
    "Feta Cheese", "Gruyere Cheese", "Eggs", "Cream Cheese", "Swiss Cheese Slices", 
    "Semi-skimmed Milk", "Macaroni & Cheese", "Ricotta Cheese", "Egg White", "Mozzarella Cheese",
    "Skimmed Milk", "Butter", "Whole Milk", "Greek Yogurt", "Sour Cream", "Monterey Cheese",
    "Cheddar Cheese", "Goat Cheese", "Protein Powder", "Parmesan Cheese",
    "Fish Sauce",
    "Baking Soda", "Baking Powder", "Honey", "Salad Dressing", "Olive Oil", "Barbecue Sauce",
    "Maple Syrup", "Molasses", "Salt", "Cream of Mushroom", "Ketchup", "White Vinegar", 
    "White Sugar", "Chili Sauce", "Teriyaki Sauce", "Brown Sugar", "Sesame Oil", "Soy Sauce",
    "Vanilla Extract", "Canola Oil", "Stevia", "Red Curry Paste", "Hummus", "White Wine",
    "Rice Wine Vinegar",
    "Applesauce", "Lemon Juice", "Lemon", "Applesuace", "Avocado", "Banana",
    "Oatmeal", "Chia Seeds", "Quinoa", "Brown Rice", "White Rice", "Wheat Flour", "Tortilla Flour",
    "Ground Beef", "Ham Steak", "Bacon", "Sirloin Beef", "Pork",
    "Macaroni", "Spaghetti",
    "Cashew Protein", "Flaxseed Powder", "Almond Protein", "Peanuts", "Chia Seeds", "Chocolate",
    "Peanut Butter", "Almond Extract", "Sesame Seeds", "Protein Powder", "Almond Milk",
    "Cocoa Powder", "Chocolate Chips", "Almond Butter", "Coconut Milk",
    "Beef or Chicken Broth", "Chicken Breast", "Turkey Bacon", "Ground Turkey", "Cream of Chicken",
    "Chicken Thigh", "Chicken Broth",
    "Seasoning Salt", "Pepper", "Red Pepper Flakes", "Cayenne Pepper", "Sage", "Onion Powder",
    "Italian Seasoning", "Dill", "Salt", "Cilantro", "Cinnamon", "Chives", "Dried Sage", "Dijon Mustard",
    "Paprika", "Mustard", "Tumeric", "Thyme", "Cinnamon Powder", "Chili Powder", "Garlic Powder",
    "Rosemary", "Oregano", "Lime juice", "Ground Cumin", "Parsley",
    "Baby Carrots", "Spinach", "Lettuce", "Salsa", "Corn", "Leeks", "Green Peas", "Sweet Potato",
    "Green Pepper", "Brussel Sprouts", "Ginger", "Red Cabbage", "Red Pepper", "Tomato", "Celery",
    "Green Chillis", "Mixed Vegetables", "Potato", "Mushroom", "Asparagus", "Garlic", "Broccoli",
    "Red Cabbage", "Green Onions", "Yellow Onions", "Garlic Salt"
]

user_strategy = st.fixed_dictionaries({
    "email": st.emails(),
    "uid": st.integers(min_value=1, max_value=10000),
    "age": st.integers(min_value=7, max_value=100),
    "sex": st.sampled_from(["Male", "Female"]),
    "height": st.integers(min_value=50, max_value=250),  # cm
    "weight": st.floats(min_value=25.0, max_value=200.0), # kg
    "fat_percent": st.floats(min_value=0.0, max_value=100.0),
    "goal": st.sampled_from(["Lose fat", "Gain muscle", "Lose fat and gain muscle", "Gain muscle and fat", "Maintain weight and health"]),
    "lifestyle": st.sampled_from(["Sedentary", "Lightly active", "Moderately active", "Highly active"]),
    "activity": st.sampled_from(["Light exercise", "Medium exercise", "Heavy exercise"]),
    "meals": st.integers(min_value=2, max_value=4),
    "cheat_meals": st.integers(min_value=0, max_value=3),
    "interval": st.integers(min_value=0, max_value=14),
    "excluded_food": st.sampled_from(food_items)
})

@given(user_strategy)
def test_mifflin_st_jeor_bmr_output_type(user_data):
    result = Diet.plan(user_data)

    # Replace 'float' with the expected type of BMR output.
    assert isinstance(result, list[str])
    
user = {
    "email": "lukelucus123@gmail.com",
    "uid": 999,
    "age": 23,
    "sex": "Male",
    "height": 175,  # cm
    "weight": 75, # kg
    "fat_percent": 20,
    "goal": "Lose fat",
    "lifestyle": "Sedentary",
    "activity": "Light exercise",
    "meals": 2,
    "cheat_meals": 2,
    "interval": 14,
    "excluded_food": random.choices(food_items, k = 5)
}
diet = Diet(user)
raw_data = diet.iterate()
user_diet_dict = {date.strftime("%d %B %Y"): value for date, value in raw_data.items()}
print(user_diet_dict)
    
