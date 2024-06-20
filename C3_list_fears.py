import csv

# get the csv file
fear_list = 'fear_list.csv'

# open the csv file
with open("fear_list.csv", 'r',) as file:
    all_fears = list(csv.reader(file, delimiter=","))
    file.close()
    # removes first row of the csv
    all_fears.pop(0)

    # Read the rest of the data
    for row in all_fears:
        print(row)
