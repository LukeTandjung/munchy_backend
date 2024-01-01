import numpy as np

def process_age_category(row, function_dict, bmi = False, age_list = None):
        age_category = None
        for category in (list(function_dict[row['sex']].keys()) if bmi == False else age_list):
            if '-' in category:
                lower, upper = category.split('-')
                if int(lower) <= row['age'] <= int(upper):
                    age_category = category
                    break
            elif category.startswith('<') and row['age'] < int(category[1:]):
                age_category = category
                break
            elif category.startswith('>') and row['age'] > int(category[1:]):
                age_category = category
                break

        if bmi == False:
            selected_function = function_dict[row['sex']][age_category]
            if callable(selected_function):
                return selected_function(row)
            else:
                return np.nan
        else:
            return age_category

def process_age_category_index(row, function_dict, bmi = False, age_list = None):
    age_category = None
    for i, category in enumerate((list(function_dict[row['sex']].keys()) if bmi == False else age_list)):
        if '-' in category:
            lower, upper = category.split('-')
            if int(lower) <= row['age'] <= int(upper):
                age_category = i
                break
        elif category.startswith('<') and row['age'] < int(category[1:]):
            age_category = i
            break
        elif category.startswith('>') and row['age'] > int(category[1:]):
            age_category = i
            break
    return age_category

        
def process_bmi_category(row, function_dict):
    bmi_category = None
    for category in list(function_dict[row['sex']].keys()):
        if '-' in category:
            lower, upper = category.split('-')
            if float(lower) <= row['bmi'] <= float(upper):
                bmi_category = category
                break
        elif category.startswith('<') and row['bmi'] < float(category[1:]):
            bmi_category = category
            break
        elif category.startswith('>') and row['bmi'] > float(category[1:]):
            bmi_category = category
            break
    
    return bmi_category