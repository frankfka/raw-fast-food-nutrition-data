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

def makeRequest(link):
    return requests.get(link, headers=header)

domain_name = 'http://calorielab.com'


sp = bs.BeautifulSoup(makeRequest(domain_name).content, 'lxml')
valid_restaurants = sp.select('div[id="food_directory_right"]')[0].select('dd[class=""]')
restaurants = []
for restaurant in valid_restaurants:
    restaurants.append(domain_name + str(restaurant.find('a', href=True)['href']))

print(restaurants)
