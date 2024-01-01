from algorithm.calculate_nutrition.carbohydrates_weight import CarbohydratesWeight
from algorithm.calculate_nutrition.fats_weight import FatsWeight
from algorithm.calculate_nutrition.protein_weight import ProteinWeight
from algorithm.strategies.mifflin_strategy import MifflinStJeorStrategy
from algorithm.context import BMRContext
from datetime import datetime, timedelta
import math

from algorithm.activity_lifestyle_multiply_bmr import activity_lifestyle_multiply_bmr
from algorithm.goal_multiply_bmr import goal_multiply_bmr
from algorithm.recipes import recipes

import numpy as np
from ortools.linear_solver import pywraplp


class Diet:
    def __init__(self, user: dict):
        self.user = user
        
    def filter(self) -> dict:
        # Filters our recipes with food ingredients that users don't want to eat
        recipe_choice = dict()
        for key, val in recipes.items():
            if not set(val["ingredients"]) & set(self.user['excluded_food']):
                recipe_choice[key] = val
        
        return recipe_choice
    
    def calculate(self) -> list[float]:
        # Using Mifflin St Jeor formula to calculate base_bmr
        mifflin_strategy = MifflinStJeorStrategy()
        bmr_context = BMRContext(mifflin_strategy)
        base_bmr: float = bmr_context.calculate_bmr(self.user)
        
        # Applying bmr multipliers to base_bmr
        goal_adjusted_bmr: float = goal_multiply_bmr(self.user, base_bmr)
        adjusted_bmr: float = activity_lifestyle_multiply_bmr(self.user, goal_adjusted_bmr)
        
        # Calculating each nutritional weight.
        protein_weight = ProteinWeight()
        protein: float = protein_weight.compute(user_data = self.user, user_bmr = adjusted_bmr)
        carbohydrates_weight = CarbohydratesWeight()
        carbohydrates: float = carbohydrates_weight.compute(user_data = self.user, user_bmr = adjusted_bmr)
        fats_weight = FatsWeight()
        fats: float = fats_weight.compute(user_data = self.user, user_bmr = adjusted_bmr)
        
        return [adjusted_bmr, protein, carbohydrates, fats]
        
    def define_constraints(self, meals: int, recipe_choice: dict, nutrition_weights: list[float]) -> tuple[np.array, np.array, np.array]:
        # Define the constraint matrix, including the number of recipes and number of meals
        recipe_constraint = np.array([val["info"] for key, val in recipe_choice.items()]).transpose()
        meals_constraint = np.ones((1, recipe_constraint.shape[1]))
        
        # Binding both arrays row-wise to get the complete constraint matrix
        constraint = np.concatenate((recipe_constraint, meals_constraint), axis = 0)
        
        # Defines the cost matrix, include the nutrition weights and the number of meals
        nutrition_resource = np.array(nutrition_weights)
        meals_resource = np.array([meals])
        
        # Binding both arrays to get the complete cost matrix
        cost = np.concatenate((nutrition_resource, meals_resource), axis = None)
        
        # Creating the objective function array
        objective = np.array([val["info"][0] for key, val in recipe_choice.items()])
        
        return constraint, cost, objective
    
    def compute(self, constraint: np.array, cost: np.array, objective_values: np.array) -> list[str]:
        num_vars = constraint.shape[1]
        num_constraints = constraint.shape[0]

        # Create the solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            return None

        # Define binary variables
        x = [solver.IntVar(0, 1, f'x{i}') for i in range(num_vars)]

        # Add constraints using matrix A and vector b
        for i in range(num_constraints - 1):
            constraint_expr = sum(constraint[i, j] * x[j] for j in range(num_vars))
            solver.Add(constraint_expr <= cost[i])
            
        # Add the last constraint as ==
        last_constraint_expr = sum(constraint[-1, j] * x[j] for j in range(num_vars))
        solver.Add(last_constraint_expr == cost[-1])

        # Define the objective function
        objective = solver.Objective()
        for i in range(num_vars):
            objective.SetCoefficient(x[i], objective_values[i])
        objective.SetMaximization()

        # Solve the problem
        status = solver.Solve()

        # Check the solution
        if status == pywraplp.Solver.OPTIMAL:
            solution = [var.solution_value() for var in x]
            max_value = solver.Objective().Value()
            return solution, max_value
        else:
            raise ValueError("Your diet was too strict! No optimal solutions found.")

        
    def plan(self, recipe_choice: dict, exclusions: list = None) -> list[str]: 
        
        # Putting everything together now!
        for key in exclusions:
            recipe_choice.pop(key, None)
            
        nutrition_weights = self.calculate()
        meals = self.user["meals"]
        constraint, cost, objective = self.define_constraints(meals, recipe_choice, nutrition_weights)
        variables, max_value = self.compute(constraint, cost, objective_values=objective)
        
        # Generating a list of recipes, and retrieving only the entry that corresponds to 1.0
        recipe_choice_list = list(recipe_choice.keys())
        return [recipe_name for recipe_index, recipe_name in zip(variables, recipe_choice_list) if recipe_index == 1.0]
    
    def iterate(self) -> dict[str: str]:
        # We set a three month dieting limit for now - so 90 days.
        if self.user["interval"] == 2:
            number_iterations = math.floor(90 / self.user["interval"])
        elif self.user["interval"] == 3:
            number_iterations = math.floor(30 / self.user["interval"])
            
        dieting_output = dict()
        last_date = datetime.now()
        next_date = last_date
        
        recipe_choice = self.filter()
        exclusions = []
        
        for i in range(number_iterations):
            result = self.plan(recipe_choice=recipe_choice, exclusions=exclusions)
            if result is not None:
                dieting_output[last_date] = result
                
                # Update the last_date for the next iteration
                last_date = next_date
                
                # Calculate the next date and store it in a temporary variable
                next_date = last_date + timedelta(days=self.user["interval"])

                exclusions.extend(result)

            else:
                break
        
        return dieting_output
        
     
