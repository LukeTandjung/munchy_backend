# The list corresponds to calories (kcal), protein (g), carbohydrates (g), fats (g)

recipes = {
    'Quinoa Taco Bowl': {
        'ingredients': ['White Rice', 'Beef Broth', 'Black Beans', 'Pinto Beans', 'Chicken Breast', 'Corn', 'Lime Juice', 'Chili Powder', 'Cayenne Pepper', 'Ground Cumin'],
        'info': [353.0, 2.0, 63.0, 20.0]
    },
    'Mac and Cheese': {
        'ingredients': ['Macaroni & Cheese', 'Semi-skimmed Milk', 'Butter', 'Cheddar Cheese'],
        'info': [1283.0, 63.0, 142.0, 35.0]
    },
    'Chocolate Peanut Butter and Cream Overnight Oats': {
        'ingredients': ['Egg White', 'Peanut Butter', 'Banana', 'Oatmeal', 'Protein Powder', 'Almond Milk', 'Vanilla Extract'],
        'info': [631.0, 23.0, 66.0, 44.0]
    }, 
    'Peppers With Fit Grits, Egg Whites And Pico De Gallo': {
        'ingredients': ['Eggs', 'Egg White', 'Spinach', 'Brown Rice', 'Green Pepper', 'Salsa'],
        'info': [375.0, 11.0, 42.0, 24.0]
    },
    'White Chili Beans and Egg Stack': {
        'ingredients': ['White Beans', 'Egg White', 'Lettuce', 'Salsa', 'Cheddar Cheese', 'Sour Cream', 'Eggs'],
        'info': [891.0, 31.0, 81.0, 54.0]
    }, 
    'Custom Overnight Oats': {
        'ingredients': ['Oatmeal', 'Almond Butter', 'Chia Seeds', 'Maple Syrup', 'Egg White', 'Cinnamon Powder', 'Cashew Protein', 'Almond Protein', 'Flaxseed Powder'],
        'info': [469.0, 14.0, 57.0, 28.0]}, 
    'Cheesy Chicken and Rice Casserole': {
        'ingredients': ['Chicken Breast', 'White Rice', 'Mixed Vegetables', 'Cheddar Cheese', 'Cream of Chicken'],
        'info': [878.0, 13.0, 91.0, 85.0]
    }, 
    'Slow Cooker Chicken and Biscuits': {
        'ingredients': ['Chicken Breast', 'Yellow Onions', 'Celery', 'Mixed Vegetables', 'Cream of Chicken', 'Chicken Broth', 'Biscuits', 'Parmesan Cheese', 'Pepper', 'Salt', 'Garlic', 'Italian Seasoning'], 
        'info': [617.0, 13.0, 60.0, 57.0]
    }, 
    'Brownie Batter Protein Shake': {
        'ingredients': ['Protein Powder', 'Avocado', 'Banana', 'Maple Syrup', 'Almond Milk', 'Cocoa Powder', 'Salt'],
        'info': [516.0, 21.0, 43.0, 51.0]
    }, 
    'Twice Baked Sweet Potato and Broccoli': {
        'ingredients': ['Sweet Potato', 'Broccoli', 'Greek Yogurt', 'Butter', 'Cheddar Cheese', 'Garlic'],
        'info': [551.0, 18.0, 71.0, 21.0]
    },
    'Sugar-Free Double Chocolate Protein Frozen Yogurt': {
        'ingredients': ['Greek Yogurt', 'Almond Milk', 'Protein Powder', 'Cocoa Powder', 'Egg White', 'Chocolate', 'Vanilla Extract', 'Stevia'],
        'info': [1274.0, 22.0, 140.0, 136.0]
    }, 
    'Baked Protein Oatmeal Cups': {
        'ingredients': ['Banana', 'Honey', 'Egg White', 'Protein Powder', 'Oatmeal', 'Cinnamon Powder'],
        'info': [1476.0, 19.0, 254.0, 83.0]
    }, 
    'Fried Rice - Custom': {
        'ingredients': ['Chicken Thigh', 'White Rice', 'Eggs', 'Egg White', 'Mixed Vegetables', 'Sirloin Beef'],
        'info': [544.0, 10.0, 55.0, 51.0]
    }, 
    'Turkey Bacon & Spinach Frittata': {
        'ingredients': ['Turkey Bacon', 'Spinach', 'Eggs', 'Egg White', 'Semi-skimmed Milk', 'Yellow Onions'], 
        'info': [787.0, 32.0, 16.0, 96.0]
    }, 
    'Custom Lunch': {
        'ingredients': ['White Rice', 'Ground Turkey', 'Black Beans', 'Green Pepper', 'Baby Carrots', 'Olive Oil'],
        'info': [490.0, 14.0, 60.0, 32.0]
    }, 
    'No-Bake Oatmeal Protein Energy Balls': {
        'ingredients': ['Oatmeal', 'Chia Seeds', 'Peanut Butter', 'Maple Syrup', 'Almond Milk', 'Protein Powder', 'Chocolate Chips', 'Cinnamon Powder', 'Vanilla Extract'],
        'info': [768.0, 24.0, 106.0, 48.0]
    },
    'Protein-Packed Banana Bread': {
        'ingredients': ['Banana', 'Wheat Flour', 'Protein Powder', 'Greek Yogurt', 'Egg White', 'Applesauce', 'White Sugar', 'Vanilla Extract', 'Baking Soda', 'Salt'],
        'info': [216.0, 1.0, 36.0, 16.0]
    }, 
    'Roasted Sweet Potatoes and Brussels Sprouts': {
        'ingredients': ['Brussel Sprouts', 'Sweet Potato', 'Olive Oil', 'Garlic', 'Ground Cumin', 'Garlic Salt', 'Salt'],
        'info': [1081.0, 58.0, 135.0, 25.0]
    }, 
    'Roasted Lemon Parmesan Garlic Asparagus': {
        'ingredients': ['Asparagus', 'Olive Oil', 'Parmesan Cheese', 'Garlic', 'Lemon Juice'],
        'info': [306.0, 17.0, 22.0, 15.0]
    },
    'Egg and Cheese Stuffed Potato': {
        'ingredients': ['Potato', 'Eggs', 'Egg White', 'Cheddar Cheese', 'Seasoning Salt', 'Garlic Powder', 'Onion Powder', 'Olive Oil'],
        'info': [486.0, 17.0, 41.0, 34.0]
    },
    'Slow Cooker Lemon Garlic Chicken': {
        'ingredients': ['Chicken Breast', 'Butter', 'Lemon Juice', 'Beef Broth', 'Oregano', 'Salt', 'Pepper', 'Garlic'],
        'info': [1222.0, 35.0, 6.0, 209.0]
    }, 
    'Feta Cheese and Bacon Stuffed Chicken': {
        'ingredients': ['Olive Oil', 'Chicken Breast', 'Bacon', 'Feta Cheese', 'Garlic', 'Lemon Juice', 'Oregano'],
        'info': [1233.0, 50.0, 9.0, 173.0]
    }, 
    'Chicken Cordon Bleu with Dijon Cream Sauce': {
        'ingredients': ['Chicken Breast', 'Swiss Cheese Slices', 'Ham Steak', 'Butter', 'Wheat Flour', 'Whole Milk', 'Dijon Mustard', 'Parmesan Cheese'],
        'info': [1290.0, 32.0, 7.0, 204.0]
    },
    'Chicken, Potato, and Leek Pie': {
        'ingredients': ['Pork', 'Potato', 'Baby Carrots', 'Chicken Thigh', 'Wheat Flour', 'Leeks', 'Chicken Broth', 'Pie Crust', 'Salt', 'Pepper', 'Semi-skimmed Milk', 'Eggs'],
        'info': [511.0, 24.0, 50.0, 26.0]
    }, 
    'Baked Oatmeal - Original': {
        'ingredients': ['Olive Oil', 'White Sugar', 'Oatmeal', 'Semi-skimmed Milk', 'Eggs', 'Maple Syrup', 'Cinnamon Powder', 'Baking Powder'],
        'info': [634.0, 28.0, 90.0, 9.0]
    }, 
    'Baked Asparagus & Cheese Frittata': {
        'ingredients': ['Asparagus', 'Olive Oil', 'Yellow Onions', 'Red Pepper', 'Eggs', 'Egg White', 'Ricotta Cheese', 'Gruyere Cheese', 'Panko Crumbs', 'Garlic', 'Salt', 'Pepper'],
        'info': [1256.0, 48.0, 78.0, 93.0]
    },
    'Greek Potato & Feta Omelet': {
        'ingredients': ['Olive Oil', 'Hash Browns', 'Eggs', 'Feta Cheese', 'Egg White'],
        'info': [730.0, 42.0, 45.0, 36.0]
    },
    'Tuscan Chicken & White Bean Soup': {
        'ingredients': ['Olive Oil', 'Leeks', 'Beef Broth', 'White Beans', 'Chicken Breast', 'Dried Sage'],
        'info': [1297.0, 22.0, 86.0, 179.0]
    },
    'Barbecue Bean Salad': {
        'ingredients': ['Barbecue Sauce', 'Molasses', 'Pinto Beans', 'Green Onions'],
        'info': [618.0, 3.0, 124.0, 24.0]
    }, 
    'Black Bean Burritos': {
        'ingredients': ['Olive Oil', 'Green Pepper', 'Tomato', 'Black Beans', 'Tortilla Flour', 'Cheddar Cheese', 'Garlic', 'Oregano', 'Ground Cumin', 'Green Chilis', 'Monterey Cheese'],
        'info': [282.0, 9.0, 37.0, 12.0]
    },
    'Turkey Cutlets with Sage & Lemon': {
        'ingredients': ['Wheat Flour', 'Chicken Breast', 'Olive Oil', 'Beef Broth', 'Butter', 'Salt', 'Pepper', 'Garlic', 'White Wine', 'Lemon Juice', 'Sage'],
        'info': [801.0, 24.0, 21.0, 109.0]
    },
    'Pampered Chicken': {
        'ingredients': ['Chicken Breast', 'Monterey Cheese', 'Egg White', 'Parmesan Cheese', 'Olive Oil', 'Panko Crumbs', 'Parsley', 'Salt', 'Pepper', 'Lemon'],
        'info': [992.0, 38.0, 16.0, 133.0]
    },
    'Chicken Paprikash': {
        'ingredients': ['Chicken Breast', 'Olive Oil', 'Yellow Onions', 'Wheat Flour', 'Beef Broth', 'Sour Cream', 'Salt', 'Pepper', 'Garlic', 'Paprika', 'Red Pepper', 'Dill'],
        'info': [985.0, 27.0, 66.0, 113.0]
    },
    'Lemony Sugar Snap & Chicken Stir-Fry': {
        'ingredients': ['Chicken Breast', 'Wheat Flour', 'Olive Oil', 'Snap Beans', 'Beef Broth', 'Salt', 'Pepper', 'Garlic', 'Parsley', 'Lemon', 'Lemon Juice'],
        'info': [974.0, 22.0, 71.0, 121.0]
    },
    'Honey-Mustard Turkey Burgers': {
        'ingredients': ['Mustard', 'Honey', 'Ground Turkey', 'Canola Oil', 'Hamburger Bun', 'Salad Dressing', 'Ketchup'],
        'info': [422.0, 17.0, 40.0, 26.0]
    },
    'Healthy Granola': {
        'ingredients': ['Oatmeal', 'Protein Powder', 'Peanut Butter', 'Maple Syrup', 'Olive Oil', 'Cocoa Powder', 'Almond Extract'],
        'info': [1286.0, 22.0, 233.0, 56.0]
    }, 
    'Yaki Soba': {
        'ingredients': ['Chicken Breast', 'Teriyaki Sauce', 'Spaghetti', 'Mushroom', 'Green Pepper', 'Red Pepper', 'Red Cabbage'],
        'info': [450.0, 3.0, 42.0, 61.0]
    }, 'Hamburger Hash': {
        'ingredients': ['Ground Beef', 'Hash Browns', 'Cream of Mushroom', 'Yellow Onions', 'Semi-skimmed Milk', 'Wheat Flour', 'Cheddar Cheese', 'Almond Milk'],
        'info': [429.0, 22.0, 36.0, 17.0]
    },
    'Skinny General Taos Chicken': {
        'ingredients': ['Chicken Breast', 'Soy Sauce', 'White Sugar', 'Chicken Broth', 'Garlic Powder', 'Garlic', 'Sesame Seeds', 'Honey', 'White Vinegar', 'Rice Wine Vinegar', 'Red Pepper Flakes'], 
        'info': [1127.0, 14.0, 126.0, 112.0]
    },
    'Quinoa Fried Rice': {
        'ingredients': ['Quinoa', 'Chicken Broth', 'Yellow Onions', 'Baby Carrots', 'Olive Oil', 'Teriyaki Sauce', 'Sesame Oil', 'Eggs', 'Green Peas', 'Egg White', 'Garlic', 'Green Onions', 'Ginger', 'Soy Sauce'],
        'info': [761.0, 30.0, 87.0, 33.0]
    },
    'Chicken Bacon Wrap': {
        'ingredients': ['Chicken Breast', 'Bacon', 'Cream Cheese', 'Feta Cheese', 'Parmesan Cheese', 'Mushroom'],
        'info': [399.0, 13.0, 3.0, 64.0]
    }, 'Cheesy Broccoli, Chicken and Rice Stuffed Peppers': {
        'ingredients': ['Chicken Breast', 'White Rice', 'Olive Oil', 'Yellow Onions', 'Dijon Mustard', 'Broccoli', 'Mozzarella Cheese', 'Cheddar Cheese', 'Greek Yogurt', 'Green Pepper', 'Garlic'],
        'info': [466.0, 9.0, 31.0, 57.0]
    },
    'Mushroom Risotto': {
        'ingredients': ['Mushroom', 'White Rice', 'Olive Oil', 'Butter', 'Chicken Broth', 'Parmesan Cheese', 'Garlic', 'Yellow Onions', 'White Wine', 'Parsley'],
        'info': [375.0, 6.0, 53.0, 14.0]
    },
    'Chicken Satay with Spicy Peanut Sauce': {
        'ingredients': ['Coconut Milk', 'Brown Sugar', 'Chicken Breast', 'Chicken Broth', 'Peanut Butter', 'Soy Sauce', 'Honey', 'Fish Sauce', 'Red Curry Paste', 'Cilantro', 'Tumeric', 'Salt', 'Pepper', 'Peanuts', 'Chili Sauce', 'Ginger', 'Garlic'],
        'info': [1099.0, 42.0, 39.0, 140.0]
    },
    'Turkey Mac and Cheese': {
        'ingredients': ['Bacon', 'Macaroni', 'Greek Yogurt', 'Goat Cheese', 'Mozzarella Cheese', 'Garlic', 'Chives', 'Salt', 'Pepper', 'Cream Cheese'],
        'info': [1233.0, 66.0, 84.0, 59.0]
    },
    'Slow Cooker Creamy Chicken, Broccoli & Rice Casserole': {
        'ingredients': ['Olive Oil', 'Garlic', 'Yellow Onions', 'White Rice', 'Thyme', 'Rosemary', 'Chicken Broth', 'Chicken Breast', 'Greek Yogurt', 'Cheddar Cheese', 'Broccoli'],
        'info': [371.0, 8.0, 36.0, 32.0]
    }, 
    'Steak and Muchroom Sandwhich': {
        'ingredients': ['Sirloin Beef', 'Mushroom', 'Cheddar Cheese', 'Cream Cheese', 'Sweet Potato'],
        'info': [563.0, 30.0, 26.0, 45.0]
    }, 
    'Baked Oatmeal - Modified': {
        'ingredients': ['Olive Oil', 'White Sugar', 'Oatmeal', 'Skimmed Milk', 'Egg White', 'Applesauce', 'Maple Syrup', 'Cinnamon Powder', 'Baking Powder'],
        'info': [548.0, 18.0, 91.0, 10.0]
    },
    'Baked Potato with Hummus': {
        'ingredients': ['Potato', 'Olive Oil', 'Hummus', 'Cucumber', 'Red Cabbage ', 'Lemon Juice', 'Salt'],
        'info': [367.0, 20.0, 42.0, 9.0]
    }
}