import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.types import ParseMode
from aiogram.utils import executor

from aiogram.dispatcher.filters.state import State, StatesGroup

from questions import questionOptions
from foodoptions import foodMenu, foodOptions
from datetime import datetime, date
from algorithm import Algorithm

logging.basicConfig(level = logging.INFO)

API_TOKEN = '6122057463:AAH9twSDFuGIgalwknXfMJHmslyYGO-4904'

bot = Bot(token = API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
dp.middleware.setup(LoggingMiddleware())



# Define states
class Form(StatesGroup):

    name = State()
    goal = State()
    target = State()
    deadline = State()
    num_meals = State()
    interval = State()
    num_cheat_meals = State()
    sex = State()
    age = State()
    weight = State()
    height = State()
    fat_percent = State()
    disorder = State()
    lifestyle = State()
    activity = State()
    health = State()
    allergy = State()
    food_menu = State()
    food_item = State()

async def send_question(message, question_text, questionOptions):
    options = questionOptions.get(question_text)
    if options:
        markup = InlineKeyboardMarkup()
        for option_group in options:
            buttons = [InlineKeyboardButton(option['text'], callback_data=option['callback_data']) for option in option_group]
            markup.add(*buttons)
        await message.reply(question_text, reply_markup = markup, parse_mode = ParseMode.HTML)
    else:
        await message.reply("Invalid question.", parse_mode=ParseMode.HTML)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Nice to know you! What is your name?")

@dp.message_handler(lambda message: not message.text.isalpha(), state = Form.name)
async def process_name_invalid(message: types.Message):
    await message.reply("Please enter a valid name.")

@dp.message_handler(lambda message: message.text.isalpha(), state = Form.name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name = user_name)
    await message.reply(f"<b>Welcome to Munchy, {user_name}</b>.\n\nBefore we get started, we want to know more about you.", parse_mode = ParseMode.HTML)
    await Form.goal.set()
    question_text = "<b>What is your goal?</b>\n\nMunchy accommodates a wide variety of goals!"
    await send_question(message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Lose fat", "Gain muscle", "Lose fat and gain muscle", "Gain muscle and fat", "Maintain weight and health"], state = Form.goal)
async def process_goal_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.")

@dp.callback_query_handler(lambda c: c.data in ["Lose fat", "Gain muscle", "Lose fat and gain muscle", "Gain muscle and fat", "Maintain weight and health"], state = Form.goal)
async def process_goal(callback_query: types.CallbackQuery, state: FSMContext):
    user_goal = callback_query.data
    await state.update_data(goal = user_goal)
    await bot.answer_callback_query(callback_query.id)
    await Form.target.set() 
    await callback_query.message.reply("<b>Do you have any specific targets?</b>\n\nWhile each target is optional, this helps Munchy plan your diet with greater accuracy.", parse_mode = ParseMode.HTML)
    await callback_query.message.reply("Type your answer in the following format. For example,\n\nWeight: 65 kg\nFat Percentage: 15 %", parse_mode = ParseMode.HTML)
    await callback_query.message.reply("If you only have goals for weight or fat percentage, put a '-' for the other entry you do not have a goal for. For example,\n\nWeight: 79 kg\nFat Percentage: - %.\n\n<b>If you do not have any specific targets, just type 'Skip'.</b>", parse_mode = ParseMode.HTML)

@dp.message_handler(state = Form.target)
async def process_target(message: types.Message, state: FSMContext):
    input_text = message.text.strip()
    lines = input_text.split('\n')
    
    # Check if the user typed "Skip"
    if input_text == 'Skip':
        user_targets = {'Weight': "-", 'Fat Percentage': "-"}
        await state.update_data(target = user_targets)
        await Form.deadline.set()
        await message.reply("<b>Do you have a goal deadline?</b>\n\nMunchy can plan diets subject to urgent time crunches!\n\n<b>Munchy does not advocate for crash dieting</b>. Our shortest diet length is 7 weeks. If you are not involved in bodybuilding, regular sports or combat sports, we highly recommend you type 'Skip'", parse_mode = ParseMode.HTML)
        await message.reply("Type your answer in a DD/MM/YYYY format. \n\n<b>If you do not have any deadlines, just type 'Skip'.</b>", parse_mode = ParseMode.HTML)
        return
        
    # Check if the input has the expected format
    if len(lines) != 2 or not lines[0].startswith('Weight:') or not lines[1].startswith('Fat Percentage:'):
        await message.reply("Please enter your targets in the expected format.")
        return

    # Extract the weight and fat percentage
    weight = lines[0].split(':')[1].strip()
    fat_percentage = lines[1].split(':')[1].strip()

    # Check if the weight and fat percentage are valid
    if (not weight.endswith(' kg') and weight != '-') or (not fat_percentage.endswith(' %') and fat_percentage != '-'):
        await message.reply("Please enter valid targets.")
        return

    # Process the targets
    user_targets = {'Weight': weight, 'Fat Percentage': fat_percentage}
    await state.update_data(target = user_targets)
    await Form.deadline.set()
    await message.reply("<b>Do you have a goal deadline?</b>\n\nMunchy can plan diets subject to urgent time crunches!\n\n<b>Munchy does not advocate for crash dieting</b>. Our shortest diet length is 7 weeks. If you are not involved in bodybuilding, regular sports or combat sports, we highly recommend you type 'Skip'", parse_mode = ParseMode.HTML)
    await message.reply("Type your answer in a DD/MM/YYYY format. \n\n<b>If you do not have any deadlines, just type 'Skip'.</b>", parse_mode = ParseMode.HTML)

@dp.message_handler(state = Form.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    input_string = message.text.strip()
    
    if input_string == "Skip":
        await state.update_data(deadline = "-")
        await Form.num_meals.set()
        question_text = "<b>How many meals do you eat a day?</b>\n\nThis helps Munchy recommend recipes for you!\n\n<b>If you eat less than two meals a day, Munchy will choose to recommend two meals a day, as it is not built to recommend only one meal a day.</b>"
        await send_question(message, question_text, questionOptions)

    else:
        start_date = datetime.now().date()
        date_info = input_string.split("/")
        
        try:
            end_date = date(int(date_info[2]), int(date_info[1]), int(date_info[0]))
            difference = end_date - start_date
            
            if difference.days < 0:
                await message.reply("Your chosen date predates today. Please try again.")
            elif difference.days < 49:
                await message.reply("Diets planned by Munchy must be at least 7 weeks long. Please try again.")
            else:
                await state.update_data(deadline = input_string) # storing the selected goal
                await Form.num_meals.set()
                question_text = "<b>How many meals do you eat a day?</b>\n\nThis helps Munchy recommend recipes for you!\n\n<b>If you eat less than two meals a day, Munchy will choose to recommend two meals a day, as it is not built to recommend only one meal a day.</b>"
                await send_question(message, question_text, questionOptions)

        except ValueError:
            await message.reply("The date you have given is an invalid date. Please try again.")
            return 

@dp.callback_query_handler(lambda c: c.data not in ["Two or less", "Three", "Four"], state = Form.num_meals)
async def process_num_meals_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.")

@dp.callback_query_handler(lambda c: c.data in ["Two or less", "Three", "Four"], state = Form.num_meals)
async def process_num_meals(callback_query: types.CallbackQuery, state: FSMContext):
    user_num_meals = callback_query.data
    await state.update_data(num_meals = user_num_meals)
    await bot.answer_callback_query(callback_query.id)
    await Form.interval.set() 
    await callback_query.message.reply("<b>How many days do you prepare meals for ahead of time</b>?\n\nThis ensures diets planned remain fresh and convenient!\n\n<b>If you cook something different every day, just fill in '0' in your reply.</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda message: not message.text.isdigit() or int(message.text) < 0, state = Form.interval)
async def process_interval_invalid(message: types.Message):
    await message.reply("Meal preparation interval must be positive whole numbers. Please try again.")

@dp.callback_query_handler(lambda message: message.text.isdigit() and int(message.text) >= 0, state = Form.interval)
async def process_interval(message: types.Message, state: FSMContext):
    user_interval = int(message.text)
    await state.update_data(interval = user_interval)
    await Form.num_cheat_meals.set() 
    question_text = "<b>How many cheat meals do you want?</b>\n\nMunchy diets are always sustainable in the long term!\n\n<b>Only choose no cheat meals if you feel you can carry out such a diet in the long term!</b>"
    await send_question(message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["No cheat meals", "One cheat meal", "Two cheat meals", "Three cheat meals"], state = Form.num_cheat_meals)
async def process_num_cheat_meals_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.")

@dp.callback_query_handler(lambda c: c.data in ["No cheat meals", "One cheat meal", "Two cheat meals", "Three cheat meals"], state = Form.num_cheat_meals)
async def process_num_cheat_meals(callback_query: types.CallbackQuery, state: FSMContext):
    user_num_cheat_meals = callback_query.data
    await state.update_data(num_cheat_meals = user_num_cheat_meals)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.reply("You're halfway there! Next, we will need to ask you for some basic health information.")
    await Form.sex.set() 
    question_text = "<b>What is your sex?</b>"
    await send_question(callback_query.message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Male", "Female"], state = Form.sex)
async def process_sex_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.")

@dp.callback_query_handler(lambda c: c.data in ["Male", "Female"], state = Form.sex)
async def process_sex(callback_query: types.CallbackQuery, state: FSMContext):
    user_sex = callback_query.data
    await state.update_data(sex = user_sex)
    await bot.answer_callback_query(callback_query.id)
    await Form.age.set() 
    await callback_query.message.reply("<b>How old are you, in years?</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda message: not message.text.isdigit() or int(message.text) <= 0, state = Form.age)
async def process_age_invalid(message: types.Message):
    await message.reply("Please give a valid age.")

@dp.callback_query_handler(lambda message: message.text.isdigit() and int(message.text) > 0, state = Form.age)
async def process_age(message: types.Message, state: FSMContext):
    user_age = int(message.text)
    await state.update_data(age = user_age)
    await Form.weight.set() 
    await message.reply("<b>How much do you weigh, in kg?</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda message: float(message.text) <= 0, state = Form.weight)
async def process_weight_invalid(message: types.Message):
    await message.reply("Please give a valid weight.")

@dp.callback_query_handler(lambda message: float(message.text) > 0, state = Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    user_weight = float(message.text)
    await state.update_data(weight = user_weight)
    await Form.height.set() 
    await message.reply("<b>How tall are you, in cm?</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda message: float(message.text) <= 0, state = Form.height)
async def process_height_invalid(message: types.Message):
    await message.reply("Please give a valid height.")

@dp.callback_query_handler(lambda message: float(message.text) > 0, state = Form.height)
async def process_height(message: types.Message, state: FSMContext):
    user_height = float(message.text)
    await state.update_data(height = user_height)
    await Form.fat_percent.set() 
    await message.reply("<b>What is your fat percentage, in %?</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda message: float(message.text) <= 0 or float(message.text) >= 100, state = Form.fat_percent)
async def process_fat_percent_invalid(message: types.Message):
    await message.reply("Please give a valid fat percentage.")

@dp.callback_query_handler(lambda message: 0 < float(message.text) < 100, state = Form.fat_percent)
async def process_fat_percent(message: types.Message, state: FSMContext):
    user_fat_percent = float(message.text)
    await state.update_data(fat_percent = user_fat_percent)
    await Form.disorder.set() 
    question_text = "<b>Do you have an active diagnosis of an eating disorder?</b>"
    await send_question(message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Yes", "No"], state = Form.disorder)
async def process_disorder_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.")

@dp.callback_query_handler(lambda c: c.data in ["Yes"], state = Form.disorder)
async def process_disorder_yes(callback_query: types.CallbackQuery, state: FSMContext):
    user_disorder = callback_query.data
    await state.update_data(disorder = user_disorder)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.reply("<b>Unfortunately, Munchy is not currently designed to support those with an active eating disorder. We recommend seeking the advice of trained medical professionals instead if you have an active eating disorder.</b>", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ["No"], state = Form.disorder)
async def process_disorder_no(callback_query: types.CallbackQuery, state: FSMContext):
    user_disorder = callback_query.data
    await state.update_data(disorder = user_disorder)
    await bot.answer_callback_query(callback_query.id)
    await Form.lifestyle.set() 
    question_text = "<b>Which option best describes your lifestyle, excluding regular exercise?</b>"
    await send_question(callback_query.message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Sedentary", "Lightly active", "Moderately active", "Highly active"], state = Form.lifestyle)
async def process_lifestyle_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ["Sedentary", "Lightly active", "Moderately active", "Highly active"], state = Form.lifestyle)
async def process_lifestyle(callback_query: types.CallbackQuery, state: FSMContext):
    user_lifestyle = callback_query.data
    await state.update_data(disorder = user_lifestyle)
    await bot.answer_callback_query(callback_query.id)
    await Form.activity.set() 
    question_text = "<b>Which option best describes your level of activity?</b>"
    await send_question(callback_query.message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Light exercise", "Medium exercise", "Heavy exercise"], state = Form.activity)
async def process_activity_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose one of the valid options.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ["Light exercise", "Medium exercise", "Heavy exercise"], state = Form.activity)
async def process_activity(callback_query: types.CallbackQuery, state: FSMContext):
    user_activity = callback_query.data
    await state.update_data(disorder = user_activity)
    await bot.answer_callback_query(callback_query.id)
    await Form.health.set() 
    question_text = "<b>Do you have any of these health conditions?</b>\n\n<b>Don't worry if you have any of these conditions! Munchy will just automatically make adjustments to your diet based on your conditions.</b>\n\nYou may select more than one health condition. Once you have selected your health conditions, type 'Next'.\n\nIf you have no health conditions, just type 'Skip'." 
    await send_question(callback_query.message, question_text, questionOptions)

@dp.callback_query_handler(lambda c: c.data not in ["Heart Disease or Stroke", "Diabetes", "Gout", "High Cholesterol", "Next", "Skip"], state=Form.health)
async def process_health_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose valid options.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ["Heart Disease or Stroke", "Diabetes", "Gout", "High Cholesterol", "Next", "Skip"], state=Form.health)
async def process_health(callback_query: types.CallbackQuery, state: FSMContext):
    selection = callback_query.data
    
    # Retrieve existing health conditions
    user_data = await state.get_data()
    health_conditions = user_data.get("health", [])
    
    # Process the selection
    if selection == "Next":
        await Form.allergy.set()
        question_text = "<b>Do you have any of these allergies?</b>\n\n<b>Again, don't worry if you have any of these allergies! Munchy will just automatically make adjustments to your diet based on your allergies.</b>\n\nYou may select more than one allergy. Once you have selected your allergies, type 'Next'.\n\nIf you have no allergies, just type 'Skip'."
        await send_question(callback_query.message, question_text, questionOptions)
    elif selection == "Skip":
        await state.update_data(health = [])
        await Form.allergy.set()
        question_text = "<b>Do you have any of these allergies?</b>\n\n<b>Again, don't worry if you have any of these allergies! Munchy will just automatically make adjustments to your diet based on your allergies.</b>\n\nYou may select more than one allergy. Once you have selected your allergies, type 'Next'.\n\nIf you have no allergies, just type 'Skip'."
        await send_question(callback_query.message, question_text, questionOptions)
    else:
        if selection not in health_conditions:
            health_conditions.append(selection)
        else:
            health_conditions.remove(selection)
        await state.update_data(health = health_conditions)
        await callback_query.message.reply(f"You have selected {', '.join(health_conditions)}.")

@dp.callback_query_handler(lambda c: c.data not in ["Shellfish", "Nuts or Tree Nuts", "Milk", "Eggs", "Next", "Skip"], state=Form.allergy)
async def process_allergy_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose valid options.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ["Shellfish", "Nuts or Tree Nuts", "Milk", "Eggs", "Next", "Skip"], state=Form.allergy)
async def process_allergy(callback_query: types.CallbackQuery, state: FSMContext):
    selection = callback_query.data
    
    # Retrieve existing health conditions
    user_data = await state.get_data()
    allergy_conditions = user_data.get("allergy", [])
    
    # Process the selection
    if selection == "Next":
        await Form.food_menu.set()
        callback_query.message.reply("<b>You're almost done!</b>\n\nNow, here comes the last step: choosing your diet foods!", parse_mode = ParseMode.HTML)
        await send_question(callback_query.message, "<b>Food Menu</b>", foodMenu)
    elif selection == "Skip":
        await state.update_data(allergy = [])
        await Form.food_menu.set()
        callback_query.message.reply("<b>You're almost done!</b>\n\nNow, here comes the last step: choosing your diet foods!", parse_mode = ParseMode.HTML)
        await send_question(callback_query.message, "<b>Food Menu</b>", foodMenu)
    else:
        if selection not in allergy_conditions:
            allergy_conditions.append(selection)
        else:
            allergy_conditions.remove(selection)
        await state.update_data(allergy = allergy_conditions)
        await callback_query.message.reply(f"You have selected {', '.join(allergy_conditions)}.")

@dp.callback_query_handler(lambda c: c.data not in ['Bread and Bakery', 'Grains', 'Noodles', 'Fruits', 'Vegetable', 'Nuts', 'Poultry', 'Eggs and Dairy', 'Livestock', 'Fish', 'Shellfish', "Next"], state = Form.food_menu)
async def process_food_menu_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose or type a valid option.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in ['Bread and Bakery', 'Grains', 'Noodles', 'Fruits', 'Vegetable', 'Nuts', 'Poultry', 'Eggs and Dairy', 'Livestock', 'Fish', 'Shellfish', "Next"], state = Form.food_menu)
async def process_food_menu(callback_query: types.CallbackQuery, state: FSMContext):
    selection = callback_query.data
    
    # Retrieve existing health conditions
    user_data = await state.get_data()
    
    # Process the selection
    if selection == "Next":

        # Start the algorithm
        selected_dishes = Algorithm().optimise()
    else:
        food_menu_key_list = [item['text'] for sublist in foodOptions[selection] for item in sublist] + ["Next", "Back"]
        await state.update_data(food_menu = food_menu_key_list)
        await Form.food_item.set()
        await send_question(callback_query.message, selection, foodOptions)

@dp.callback_query_handler(lambda c: c.data not in FSMContext.storage.get(c.from_user.id, Form.food_item)["food_menu_list"], state=Form.food_item)
async def process_food_item_invalid(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Please choose or type a valid option.", parse_mode = ParseMode.HTML)

@dp.callback_query_handler(lambda c: c.data in FSMContext.storage.get(c.from_user.id, Form.food_item)["food_menu_list"], state=Form.food_item)
async def process_food_item(callback_query: types.CallbackQuery, state: FSMContext):
    selection = callback_query.data
    
    # Retrieve existing food items
    user_data = await state.get_data()
    selected_food_items = user_data.get("food_item", [])
    
    # Process the selection
    if selection == "Next":
        # Start the algorithm
        selected_dishes = Algorithm().optimise()
    elif selection == "Back":
        await Form.food_menu.set()
        await send_question(callback_query.message, "<b>Food Menu</b>", foodMenu)
    else:
        if selection not in selected_food_items:
            selected_food_items.append(selection)
        else:
            selected_food_items.remove(selection)
        await state.update_data(food_item = selected_food_items)
        await callback_query.message.reply(f"You have selected {', '.join(selected_food_items)}.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)



