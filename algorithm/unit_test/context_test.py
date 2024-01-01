from context import BMRContext
from strategies.mifflin_strategy import MifflinStJeorStrategy
from hypothesis import given, strategies as st

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
    "excluded_food": st.lists(st.text())
})

@given(user_strategy)
def test_mifflin_st_jeor_bmr_output_type(user_data):
    mifflin_strategy = MifflinStJeorStrategy()
    bmr_context = BMRContext(mifflin_strategy)
    bmr = bmr_context.calculate_bmr(user_data)  

    # Replace 'float' with the expected type of BMR output.
    assert isinstance(bmr, float)
    
