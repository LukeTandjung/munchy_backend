questionOptions = {
    "<b>What is your goal?</b>\n\nMunchy accommodates a wide variety of goals!": [
        [{
            "text": "Lose fat",
            "callback_data": "Lose fat"
        }],
        [{
            "text": "Gain muscle",
            "callback_data": "Gain muscle"
        }],
        [{
            "text": "Lose fat and gain muscle",
            "callback_data": "Lose fat and gain muscle"
        }],
        [{
            "text": "Gain muscle and fat",
            "callback_data": "Gain muscle and fat"
        }],
        [{
            "text": "Maintain weight and health",
            "callback_data": "Maintain weight and health"
        }],
    ],
    "<b>Do you have any specific targets?</b>\n\nWhile each target is optional, this helps Munchy plan your diet with greater accuracy.\n\nType your answer in the following format:\n\nWeight: *** kg\nFat Percentage: *** %\n\nIf you only have goals for weight or fat percentage, put a '-' for the other entry you do not have a goal for. For example,\n\nWeight: 79 kg\nFat Percentage: - %.\n\n<b>If you do not have any specific targets, just type 'Skip'.</b>": 
    {
       "Weight": 0,
       "Fat percentage": 0
    },
    "<b>Do you have a goal deadline?</b>\n\nMunchy can plan diets subject to urgent time crunches!\n\n<b>Munchy does not advocate for crash dieting</b>. Our shortest diet length is 7 weeks. If you are not involved in bodybuilding, regular sports or combat sports, we highly recommend you type 'Skip'": 
    {
        "Deadline": 0
    },
    "<b>How many meals do you eat a day?</b>\n\nThis helps Munchy recommend recipes for you!\n\n<b>If you eat less than two meals a day, Munchy will choose to recommend two meals a day, as it is not built to recommend only one meal a day.</b>": [
        [{
            "text": "Two or less",
            "callback_data": "Two or less"
        }],
        [{
            "text": "Three",
            "callback_data": "Three"
        }],  
        [{
            "text": "Four",
            "callback_data": "Four"
        }]
    ],
    "<b>How many days do you prepare meals for ahead of time</b>?\n\nThis ensures diets planned remain fresh and convenient!\n\n<b>If you cook something different every day, just fill in '0' in your reply.</b>": 
    {
        "MealPrepInterval": 0
    },
    "<b>How many cheat meals do you want?</b>\n\nMunchy diets are always sustainable in the long term!\n\n<b>Only choose no cheat meals if you feel you can carry out such a diet in the long term!</b>": [
        [{
            "text": "No cheat meals",
            "callback_data": "No cheat meals"
        }],
        [{
            "text": "One cheat meal",
            "callback_data": "One cheat meal"
        }],
        [{
            "text": "Two cheat meals",
            "callback_data": "Two cheat meals" 
        }],
        [{
            "text": "Three cheat meals",
            "callback_data": "Three cheat meals" 
        }]
    ],
    "<b>What is your sex?</b>": [
        [{
            "text": "Male",
            "callback_data": "Male"
        }],
        [{
            "text": "Female",
            "callback_data": "Female"
        }],
    ],
    "<b>Do you have an active diagnosis of an eating disorder?</b>": [
        [{
            "text": "Yes",
            "callback_data": "Yes"
        }],
        [{
            "text": "No",
            "callback_data": "No"
        }]
    ],
    "<b>Which option best describes your lifestyle, excluding regular exercise?</b>": [
        [{
            "text": "Desk job, with little physical activity",
            "callback_data": "Sedentary"
        }],
        [{
            "text": "Desk job, with a light daily physical routine",
            "callback_data": "Lightly active"
        }],
        [{
            "text": "On the feet job, occassionally playing sports",
            "callback_data": "Moderately active"
        }],
        [{
            "text": "Physically intensive job, regularly playing sports",
            "callback_data": "Highly active"
        }],
    ],
    "<b>Which option best describes your level of activity?</b>": [
        [{
            "text": "Light exercise, 1 - 2 times a week",
            "callback_data": "Light exercise"
        }],
        [{
            "text": "Medium exercise, 3 - 4 times a week",
            "callback_data": "Medium exercise"
        }],
        [{
            "text": "Heavy exercise, 5 - 6 times a week",
            "callback_data": "Heavy exercise"
        }]
    ],
    "<b>Do you have any of these health conditions?</b>\n\n<b>Don't worry if you have any of these conditions! Munchy will just automatically make adjustments to your diet based on your conditions.</b>\n\nYou may select more than one health condition. Once you have selected your health conditions, type 'Next'.\n\nIf you have no health conditions, just type 'Skip'.": [
        [{
            "text": "Heart Disease or Stroke",
            "callback_data": "Heart Disease or Stroke"
        }],
        [{
            "text": "Diabetes",
            "callback_data": "Diabetes"
        }],
        [{
            "text": "Gout",
            "callback_data": "Gout"
        }],
        [{
            "text": "High Cholesterol",
            "callback_data": "High Cholesterol"
        }]
    ],
    "<b>Do you have any of these allergies?</b>\n\n<b>Again, don't worry if you have any of these allergies! Munchy will just automatically make adjustments to your diet based on your allergies.</b>\n\nYou may select more than one allergy. Once you have selected your allergies, type 'Next'.\n\nIf you have no allergies, just type 'Skip'.": [
        [{
            "text": "Shellfish",
            "callback_data": "Shellfish"
        }],
        [{
            "text": "Nuts or Tree Nuts",
            "callback_data": "Nuts or Tree Nuts"
        }],
        [{
            "text": "Milk",
            "callback_data": "Milk"
        }],
        [{
            "text": "Eggs",
            "callback_data": "Eggs"
        }]
    ]
  }