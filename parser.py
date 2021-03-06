import re
from datetime import datetime
from db import Database
from dashboard import Dashboard
from csv_generator import CSVGenerator


class Parser(object):
    def __init__(self):
        self.db = Database()
        self.dashboard = Dashboard()
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
            if deleted_item_name:
                bot_message = "{} deleted.".format(deleted_item_name)
            else:
                bot_message = "Ошибка. Нечего удалять."
        else:
            added_item_name = self.db.add_sale(string.capitalize())
            if added_item_name:
                bot_message = "{} added.".format(added_item_name)
            else:
                bot_message = "Ошибка! Такого товара нет в меню. Попробуй еще раз."
        return bot_message

    def search_date(self, string):
        search_date_result = re.search("\d{2}.\d{2}.\d{4}", string)
        if search_date_result:
            date = search_date_result.group()
            return date

    def parse_revenue_message(self, string):
        date = self.search_date(string)

        if date and self.db.check_date(date):
            bot_message = self.dashboard.day_board(date)
        elif date:
            bot_message = "Нет данных за этот день."
        elif string == "выручка":
            today = datetime.strftime(datetime.now(), "%d.%m.%Y")
            bot_message = self.dashboard.day_board(today)
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
            today = datetime.strftime(datetime.now(), "%d.%m.%Y")
            csv_file = self.csv_generator.write_csv(today)
            bot_message = open(csv_file, 'rb')
        elif string == "отчет полный" or string == "отчёт полный":
            csv_file = self.csv_generator.write_csv("all")
            bot_message = open(csv_file, 'rb')
        else:
            bot_message = "Ошибка! Неверный формат даты."
        return bot_message
