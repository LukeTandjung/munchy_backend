from hypothesis import given, strategies as st
from protein_weight import ProteinWeight

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
user_bmr = st.floats(min_value=1000, max_value=4000)

@given(user_strategy, user_bmr)
def test_activity_lifestyle_multiply_bmr(user_data, bmr):
    # Call the function to test
    result = ProteinWeight.compute(user_data, bmr)
    # Check that the result is a float
    assert isinstance(result, float), "The function should return a float."