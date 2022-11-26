import pandas as pd
import csv
import os

data = pd.read_csv("wines_full_1.csv", delimiter=';', low_memory=False)
number = data['Wine'].nunique()
data = data.drop_duplicates('Wine', keep ='first')
data=data[['Wine','link']]
data.to_csv('data1.csv', index=False, quoting=csv.QUOTE_NONNUMERIC, sep = ';')