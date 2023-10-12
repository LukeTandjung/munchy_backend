class DietPlanner:
    def __init__(self, weight, fat_percentage, goal, target_weight=None, target_fat_percentage=None):
        self.weight = weight
        self.fat_percentage = fat_percentage
        self.goal = goal
        self.target_weight = target_weight
        self.target_fat_percentage = target_fat_percentage

    def calculate_current_masses(self):
        """Calculate current fat mass and lean mass."""
        current_fat_mass = self.weight * (self.fat_percentage / 100)
        current_lean_mass = self.weight - current_fat_mass
        return current_fat_mass, current_lean_mass

    def adjust_masses(self):
        """Determine adjusted fat mass and lean mass based on the health goal."""
        current_fat_mass, current_lean_mass = self.calculate_current_masses()
        
        if self.target_weight is not None and self.target_fat_percentage is not None:
            # If target weight is provided, adjust the masses to meet that weight
            # The logic can be expanded further based on more detailed requirements.
            return self.target_weight * (self.target_fat_percentage / 100), self.target_weight * (1 - (self.target_fat_percentage / 100))
        
        if self.goal == "gain_muscle":
            adjusted_lean_mass = current_lean_mass * 1.05
            adjusted_fat_mass = current_fat_mass
        elif self.goal == "lose_fat":
            adjusted_lean_mass = current_lean_mass
            adjusted_fat_mass = current_fat_mass * 0.90
        elif self.goal == "gain_muscle_lose_fat":
            adjusted_lean_mass = current_lean_mass * 1.05
            adjusted_fat_mass = current_fat_mass * 0.90
        elif self.goal == "gain_both":
            adjusted_lean_mass = current_lean_mass * 1.07
            adjusted_fat_mass = current_fat_mass * 1.07
        elif self.goal == "lose_both":
            adjusted_lean_mass = current_lean_mass * 0.95
            adjusted_fat_mass = current_fat_mass * 0.90
        else:  # maintain
            adjusted_lean_mass = current_lean_mass
            adjusted_fat_mass = current_fat_mass
            
        return adjusted_fat_mass, adjusted_lean_mass

    def calculate_targets(self):
        """Calculate target weight and fat percentage."""
        adjusted_fat_mass, adjusted_lean_mass = self.adjust_masses()
        target_weight = adjusted_fat_mass + adjusted_lean_mass
        target_fat_percentage = (adjusted_fat_mass / target_weight) * 100
        return target_weight, target_fat_percentage

    def determine_targets(self):
        """Main method to determine exact targets for weight and fat percentage."""
        return self.calculate_targets()

# Test the class for the same user scenario
planner = DietPlanner(70, 20, "gain_muscle")
planner.determine_targets()

