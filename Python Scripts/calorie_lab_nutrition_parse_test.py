# Necessary imports
import pandas as pd
import requests
import numpy as np
import os
import re
import bs4 as bs
from collections import OrderedDict

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
no_link = "no_link"
domain_name = 'http://calorielab.com'
restaurant_link = 'http://calorielab.com/restaurants/tim-hortons/22'
# restaurant_link = 'http://calorielab.com/restaurants/tim-hortons/ham-and-swiss/22/2618'

def makeRequest(link):
    return requests.get(link, headers=header)

link = 'http://calorielab.com/restaurants/tim-hortons/ham-and-swiss/22/2618'

def get_number_from_string(original_string):
    return re.search(re.compile('[0-9]+,*[0-9]*\.*[0-9]*'), original_string).group(0)

# Returns a dictionary with nutritional values for the food
def parse_food_object(link_to_food):
    item_html = bs.BeautifulSoup(makeRequest(link_to_food).content, 'lxml')
    item_name = item_html.select('span[class="fn"]')[0].text
    nutrition_table = item_html.find('table')
    parsed_nutrition_table = pd.read_html(str(nutrition_table),encoding='utf-8', header=0)[0]
    parsed_nutrition_table.fillna(0, inplace=True)

    food_dict = OrderedDict()
    food_dict['food_name'] = item_name
    for index, row in parsed_nutrition_table.iterrows():
        if 'Calories (%DV' in row['Nutrient'] and not 'calories' in food_dict:
            food_dict['calories'] = get_number_from_string(row['Value'])
        elif 'Total Fat' in row['Nutrient'] and not 'total_fat' in food_dict:
            food_dict['total_fat'] = get_number_from_string(row['Value'])
        elif 'Saturated Fat' in row['Nutrient'] and not 'sat_fat' in food_dict:
            food_dict['sat_fat'] = get_number_from_string(row['Value'])
        elif 'Trans Fat' in row['Nutrient'] and not 'trans_fat' in food_dict:
            food_dict['trans_fat'] = get_number_from_string(row['Value'])
        elif 'Cholesterol' in row['Nutrient'] and not 'cholesterol' in food_dict:
            food_dict['cholesterol'] = get_number_from_string(row['Value'])
        elif 'Sodium' in row['Nutrient'] and not 'sodium' in food_dict:
            food_dict['sodium'] = get_number_from_string(row['Value'])
        elif 'Total Carbohydrate' in row['Nutrient'] and not 'carbohydrates' in food_dict:
            food_dict['carbohydrates'] = get_number_from_string(row['Value'])
        elif 'Dietary Fiber' in row['Nutrient'] and not 'fiber' in food_dict:
            food_dict['fiber'] = get_number_from_string(row['Value'])
        elif 'Sugars (WHO' in row['Nutrient'] and not 'sugar' in food_dict:
            food_dict['sugar'] = get_number_from_string(row['Value'])
        elif 'Protein' in row['Nutrient'] and not 'protein' in food_dict:
            food_dict['protein'] = get_number_from_string(row['Value'])
        elif 'Vitamin A' in row['Nutrient'] and not 'vit_a' in food_dict:
            food_dict['vit_a'] = get_number_from_string(row['%DV'])
        elif 'Vitamin C' in row['Nutrient'] and not 'vit_c' in food_dict:
            food_dict['vit_c'] = get_number_from_string(row['%DV'])
        elif 'Calcium' in row['Nutrient'] and not 'calcium' in food_dict:
            food_dict['calcium'] = get_number_from_string(row['%DV'])
        elif 'Iron' in row['Nutrient'] and not 'iron' in food_dict:
            food_dict['iron'] = get_number_from_string(row['%DV'])

    return food_dict