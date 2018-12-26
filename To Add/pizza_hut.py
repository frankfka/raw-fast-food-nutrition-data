import numpy as np
import pandas as pd


source_dataframe = pd.read_csv("pizza_hut_pizzas.csv")
listofstrings = []
pizza_name = ""

for index, row in source_dataframe.iterrows():
    if np.isnan(row['iron']):
        pizza_name = str(row['food_name']).replace('®','')
        listofstrings.append(pizza_name)
    else:
        listofstrings.append(str(row['food_name']).replace('®','') + " (" + pizza_name +")")

pd.DataFrame({"Test":listofstrings}).to_csv("pizza_test.csv", index=False)