import pandas as pd
import csv
import os
#
# data = pd.read_csv("wines_full_1.csv", delimiter=';', low_memory=False)
# number = data['Wine'].nunique()
# data = data.drop_duplicates('Wine', keep ='first')
# data=data[['Wine','link']]

data = pd.read_csv("data1.csv", delimiter=';', low_memory=False)
list = []
#data.to_csv('data1.csv', index=False, quoting=csv.QUOTE_NONNUMERIC, sep = ';')
for row in data.itertuples():
    string = row[2]
    string = string.replace('-', '+')
    lens = len(string)
    string = string[29:lens - 4]
    index_of = string.rfind('/')
    string = string[0:index_of-2]
    lens = len(string)

    year = string[lens-4:lens]
    print(year)
    string = string[0:lens - 5]

    new_string = 'https://www.wine-searcher.com/find/' + string + '/' + year + '/' + "#t4"
    list.append(new_string)
    print (new_string)