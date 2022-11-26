import csv

reader = csv.reader(open("GR0-5000_2.csv", "r"), delimiter=',')
writer = csv.writer(open("GR0-5000_2_semi.csv", 'w'), delimiter=';')
writer.writerows(reader)

print("Delimiter successfully changed")
