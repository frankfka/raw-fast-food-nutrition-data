from tabula import read_pdf
import pandas as pd
import numpy as np
import re

import_file_name = "Orange Julius.csv"
starting_food_id = 369
menu_id = 16
export_file_name = "Orange Julius formatted"

source_dataframe = pd.read_csv(import_file_name)
# source_dataframe = read_pdf(import_file_name, pages='all')
source_dataframe = source_dataframe.dropna()
df_length = source_dataframe.shape[0]

food_names = list(source_dataframe.iloc[:, 0])
food_indexes = list(np.linspace(starting_food_id, starting_food_id + df_length - 1, df_length, dtype = int))
menu_values = list(np.linspace(menu_id, menu_id, df_length, dtype = int))
is_vegan = [0] * df_length
is_vegetarian = [0] * df_length
is_gf = [0] * df_length
# Find the necessary columns in the original dataframe
calories = []
total_fat = []
sat_fat = []
trans_fat = []
cholesterol = []
sodium = []
carbs = []
fiber = []
sugar = []
protein = []
vit_a = []
vit_c = []
calcium = []
iron = []

for column in source_dataframe:
    column_comparison_string = str(column).strip().lower()
    if "calories" in column_comparison_string and not calories:
        calories = list(source_dataframe[column])
    elif "fat" in column_comparison_string and not total_fat:
        total_fat = list(source_dataframe[column])
    elif "saturated" in column_comparison_string and not sat_fat:
        sat_fat = list(source_dataframe[column])
    elif "trans" in column_comparison_string and not trans_fat:
        trans_fat = list(source_dataframe[column])
    elif "cholesterol" in column_comparison_string and not cholesterol:
        cholesterol = list(source_dataframe[column])
    elif "sodium" in column_comparison_string and not sodium:
        sodium = list(source_dataframe[column])
    elif "carb" in column_comparison_string and not carbs:
        carbs = list(source_dataframe[column])
    elif "fiber" in column_comparison_string or "fibre" in column_comparison_string and not fiber:
        fiber = list(source_dataframe[column])
    elif "sugar" in column_comparison_string and not sugar:
        sugar = list(source_dataframe[column])
    elif "protein" in column_comparison_string and not protein:
        protein = list(source_dataframe[column])
    elif "vitamin a" in column_comparison_string and not vit_a:
        vit_a = list(source_dataframe[column])
        for index in range(0, len(vit_a)):
            value = str(vit_a[index])
            if "%" in value:
                vit_a[index] = re.sub('%', '', value)
    elif "vitamin c" in column_comparison_string and not vit_c:
        vit_c = list(source_dataframe[column])
        for index in range(0, len(vit_c)):
            value = str(vit_c[index])
            if "%" in value:
                vit_c[index] = re.sub('%', '', value)
    elif "calcium" in column_comparison_string and not calcium:
        calcium = list(source_dataframe[column])
        for index in range(0, len(calcium)):
            value = str(calcium[index])
            if "%" in value:
                calcium[index] = re.sub('%', '', value)
    elif "iron" in column_comparison_string and not iron:
        iron = list(source_dataframe[column])
        for index in range(0, len(iron)):
            value = str(iron[index])
            if "%" in value:
                iron[index] = re.sub('%', '', value)

output_df = pd.DataFrame(
    {'food_id': food_indexes, 'menu_id': menu_values,'food_name': food_names, 'calories': calories, 'fat': total_fat, 'saturated_fat': sat_fat,
     'trans_fat': trans_fat, 'cholesterol': cholesterol, 'sodium': sodium, 'carbohydrates': carbs, 'fiber': fiber, 'sugar': sugar,
     'protein': protein, 'vit_a': vit_a, 'vit_c': vit_c, 'calcium': calcium, 'iron': iron, 'is_vegetarian': is_vegetarian, 'is_vegan': is_vegan, "is_gf": is_gf })
output_df = output_df[['food_id', 'menu_id','food_name', 'calories', 'fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'carbohydrates', 'fiber', 'sugar',
     'protein', 'vit_a', 'vit_c', 'calcium', 'iron', 'is_vegetarian', 'is_vegan', 'is_gf']]

output_df.to_csv(export_file_name + ".csv", index=False)
print('Done!')
print('New starting food id: ' + str(starting_food_id + df_length))
print('New menu id: ' + str(menu_id + 1))