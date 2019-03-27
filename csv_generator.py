import csv
from db import Database


class CSVGenerator(object):
    def __init__(self):
        self.db = Database("/Users/alexander/code/bots/CashboxBot/data.db")

    def all_data(self):
        with open('csv.txt', mode='w') as file:
            file_writer = csv.writer(file)

            file_writer.writerow(["id", "item", "date", "time"])
            for row in self.db.table():
                file_writer.writerow([row[0], self.db.item_name(row[1]), row[2], row[3]])
