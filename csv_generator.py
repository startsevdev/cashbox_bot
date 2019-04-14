import csv
from db import Database, Item


class CSVGenerator(object):
    def __init__(self):
        self.db = Database()

    def write_csv(self, date):
        table = self.db.sales(date)

        with open("sales.txt", mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(["id", "item", "price", "date", "time"])
            for row in table:
                item = Item(row[1])

                csv_writer.writerow([row[0], item.name, item.price, row[2], row[3]])
        return "sales.txt"
