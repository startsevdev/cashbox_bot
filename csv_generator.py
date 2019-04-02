import csv
from db import Database


class CSVGenerator(object):
    def __init__(self):
        self.db = Database("/home/startsevdev/ccbot/data.db")

    def write_csv(self, date):
        if date == "all":
            table = self.db.all_sales()
        else:
            table = self.db.date_sales(date)

        with open("sales.txt", mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(["id", "item", "price", "date", "time"])
            for row in table:
                csv_writer.writerow([row[0], self.db.item_name(row[1]), self.db.item_price(row[1]), row[2], row[3]])
        return "sales.txt"
