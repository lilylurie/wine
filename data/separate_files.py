import pandas as pd
import csv

data = pd.read_csv('/home/lily/Downloads/Wines.csv', delimiter=";", low_memory=False)
data_2 = data[500001:1000001]
data_2.to_csv("wines_part_2.csv",index=False, sep = ';')
