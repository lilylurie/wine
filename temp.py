import csv
from datetime import datetime
import json

import pandas as pd
import openpyxl

# class PRICES:
#     def init(self, price, data):
#         self.price = price
#         self.data = data
#
#     def get_price(self):
#         return self.price
#
#     def get_data(self):
#         return self.data




file = pd.read_excel('table.xlsx')
print(file['Wine'].iloc[0])


table = []
for i in range(0, 10):
    print(i)
    mas_obj = []
    d = {'Name': file['Wine'].iloc[i], 'Link_vivino': file['Link_vivino'].iloc[i], 'History' : mas_obj}
    string = str(file['data'].iloc[i])
    if string[0] == 'v':
        index = string.find("\"data\"")
        len_one = len("\"data\"")
        string = string[index+len_one+1:]
        index_end = string.find("\"color\"")
        string = string[:index_end-1]
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace(' ', '')
        mas = string.split(',')
        print(datetime.fromtimestamp(int(mas[0])/1000).strftime('%Y-%m'))
        for j in range(0, len(mas)//2, 2):
            mas_obj.append({'date': datetime.fromtimestamp(int(mas[j])/1000).strftime('%Y-%m'),'price': mas[j+1]})
        table.append(d)
        continue
    if string[0] == 'w':
        print('Check the wine ', i)
        continue
    if string[0] == '\n':
        print('Check the wine ', i)
        continue
    if string[0] == '-':
        print('C\'est la vie')
        table.append(d)
        continue
    else:
        index = string.find('[[')
        index_end = string.rfind(']')
        string = string[index: index_end + 2]
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace(' ', '')
        mas = string.split(',')
        print(datetime.fromtimestamp(int(mas[0]) / 1000).strftime('%Y-%m'))
        for j in range(0, len(mas) // 2,2):
            mas_obj.append({'date': datetime.fromtimestamp(int(mas[j])/1000).strftime('%Y-%m'),'price': mas[j+1]})
        table.append(d)
        continue
with open("wines.json", 'w') as f:
    json.dump(table, f)
#917, 1136, 1156 --- ?