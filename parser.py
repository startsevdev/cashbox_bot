import re
from datetime import datetime
from db import Database
from csv_generator import CSVGenerator


class Parser(object):
    def __init__(self):
        self.db = Database("/Users/alexander/code/bots/CashboxBot/data.db")
        self.csv_generator = CSVGenerator()

    def parse_message(self, string):
        # sql-injection protection
        string = re.sub("'", "", string)
        string = re.sub('"', '', string)

        string = string.lower()

        if "выручка" in string:
            bot_message = self.parse_revenue_message(string)
        elif "отчет" in string or "отчёт" in string:
            bot_message = self.parse_report_message(string)
        elif string == "отмена":
            deleted_item_name = self.db.del_last_sale()
            bot_message = "{} deleted.".format(deleted_item_name)
        else:
            added_item_name = self.db.add_sale(string.capitalize())
            bot_message = "{} added.".format(added_item_name)
        return bot_message

    def search_date(self, string):
        search_date_result = re.search("\d{2}.\d{2}.\d{4}", string)
        if search_date_result:
            date = search_date_result.group()
            return date

    def parse_revenue_message(self, string):
        date = self.search_date(string)

        if date and self.db.check_date(date):
            bot_message = self.db.revenue(date)
        elif date:
            bot_message = "Нет данных за этот день."
        elif string == "выручка":
            bot_message = self.db.revenue()
        else:
            bot_message = "Ошибка! Неверный формат даты."
        return bot_message

    def parse_report_message(self, string):
        date = self.search_date(string)

        if date and self.db.check_date(date):
            csv_file = self.csv_generator.write_csv(date)
            bot_message = open(csv_file, 'rb')
        elif date:
            bot_message = "Нет данных за этот день."
        elif string == "отчет" or string == "отчёт":
            csv_file = self.csv_generator.write_csv(date=datetime.strftime(datetime.now(), "%d.%m.%Y"))
            bot_message = open(csv_file, 'rb')
        elif string == "отчет полный" or string == "отчёт полный":
            csv_file = self.csv_generator.write_csv("all")
            bot_message = open(csv_file, 'rb')
        else:
            bot_message = "Ошибка! Неверный формат даты."
        return bot_message
