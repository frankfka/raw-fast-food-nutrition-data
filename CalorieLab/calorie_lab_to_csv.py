# Necessary imports
import pandas as pd
import requests
import numpy as np
import os
import re
from collections import OrderedDict
import bs4 as bs

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
no_link = "no_link"
domain_name = 'http://calorielab.com'
dir_path = os.getcwd()
# These should be unused at the start
food_id = 100000
menu_id = 20000
restaurant_id = 1000

def makeRequest(link):
    return requests.get(link, headers=header)

# Returns 0 if NaN or invalid
def get_number_from_string(original_string):
    string_to_search = str(original_string)
    extracted_string = re.search(re.compile('[0-9]+,*[0-9]*\.*[0-9]*'), string_to_search).group(0)
    return re.sub(",","", extracted_string)

# Returns a dictionary with nutritional values for the food
def parse_food_object(link_to_food):
    item_html = bs.BeautifulSoup(makeRequest(link_to_food).content, 'lxml')
    item_name = item_html.select('span[class="fn"]')[0].text
    item_serving = ""
    if item_html.select('span[class="heading_serving"]'):
        item_serving = re.sub( '\s+', ' ', re.sub('Serving: ','',item_html.select('span[class="heading_serving"]')[0].text).strip())
    nutrition_table = item_html.find('table')
    parsed_nutrition_table = pd.read_html(str(nutrition_table),encoding='utf-8', header=0)[0]
    parsed_nutrition_table.fillna(0, inplace=True)

    food_dict = OrderedDict()
    food_dict['food_name'] = item_name
    food_dict['serving_size'] = item_serving
    for index, row in parsed_nutrition_table.iterrows():
        if 'Calories (%DV' in row['Nutrient'] and not 'calories' in food_dict:
            food_dict['calories'] = get_number_from_string(row['Value'])
        elif 'Total Fat' in row['Nutrient'] and not 'fat' in food_dict:
            food_dict['fat'] = get_number_from_string(row['Value'])
        elif 'Saturated Fat' in row['Nutrient'] and not 'saturated_fat' in food_dict:
            food_dict['saturated_fat'] = get_number_from_string(row['Value'])
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

sp = bs.BeautifulSoup(makeRequest(domain_name).content, 'lxml')
valid_restaurants = sp.select('div[id="food_directory_right"]')[0].select('dd[class=""]')
restaurants = []

for restaurant in valid_restaurants:
    restaurants.append(domain_name + str(restaurant.find('a', href=True)['href']))

# First few restaurants have been parsed
# restaurants = restaurants[11:-1]

for restaurant_link in restaurants:
    ###
    ### THIS PART GETS TABLE FOR EACH RESTAURANT AND ITS CORRESPONDING NAME
    ###
    # Assumes one table per page (true for calorielab)
    sp = bs.BeautifulSoup(makeRequest(restaurant_link).content, 'lxml')

    restaurant_name = sp.select('div[id="results_heading"]')[0].select('span[class="label"]')[0].text
    tb = sp.find('table')
    parsed_food_item_table = pd.read_html(str(tb),encoding='utf-8', header=0)[0]

    links = []
    for row in tb.find_all('tr'):
        if row.find_all('a'):
            links.append(domain_name + row.find('a').get('href'))
        else:
            links.append(no_link)
    # Pop first row because pandas uses first row as index
    links.pop(0)
    parsed_food_item_table['href'] = links

    # Creates a dictionary of menu names and links to items 
    menus = dict()
    for index, row in parsed_food_item_table.iterrows():
        if "Menu Category:" in row['Food']:
            menu_name = re.sub('Menu Category: ', '', row['Food'])
            current_menu = menu_name
            menus[current_menu] = []
        else:
            menus[current_menu].append(row['href'])


    food_dataframe = pd.DataFrame(columns=['food_id', 'menu_id','food_name', 'serving_size', 'calories', 'fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'carbohydrates', 'fiber', 'sugar', 'protein', 'vit_a', 'vit_c', 'calcium', 'iron', 'is_vegetarian', 'is_vegan', 'is_gf'])
    menu_dataframe = pd.DataFrame(columns=['menu_id', 'menu_name', 'restaurant_id'])
    for menu_name in menus:
        link_list = menus[menu_name]
        menu_entry = dict({'menu_id': menu_id, 'menu_name': menu_name, 'restaurant_id': restaurant_id})
        menu_dataframe = menu_dataframe.append(menu_entry, ignore_index=True)
        for link in link_list:
            food_details_dict = parse_food_object(link) 
            food_details_dict['food_id'] = food_id
            food_id += 1
            food_details_dict['menu_id'] = menu_id
            food_details_dict['is_vegetarian'] = 0
            food_details_dict['is_vegan'] = 0
            food_details_dict['is_gf'] = 0
            food_dataframe = food_dataframe.append(food_details_dict, ignore_index=True)
        menu_id += 1         

    food_dataframe.to_csv(re.sub(re.compile('[\\/:"*?<>|]+'), "", str(str(restaurant_id) + "_" + restaurant_name + "_foods.csv")), index=False)
    menu_dataframe.to_csv(re.sub(re.compile('[\\/:"*?<>|]+'), "", str(str(restaurant_id) + "_" + restaurant_name + "_menus.csv")), index=False)
    restaurant_id += 1