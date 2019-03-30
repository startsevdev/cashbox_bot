import re
from db import Database
from csv_generator import CSVGenerator


class Parser(object):
    def __init__(self):
        self.db = Database("/Users/alexander/code/bots/CashboxBot/data.db")
        self.csv_generator = CSVGenerator()

    def parse_message(self, string):
        string = string.lower()
        date = self.search_date(string)

        if "выручка" in string:
            if date and self.db.check_date(date):
                return self.db.revenue(date)
            elif date:
                return "Нет данных за этот день."
            else:
                return self.db.revenue()
        elif "отчет" in string:
            if date and self.db.check_date(date):
                return self.csv_generator.write_csv(date)
            elif date:
                return "Нет данных за этот день."
            else:
                return self.csv_generator.write_csv()
        else:
            return self.db.add_sale(string.capitalize())

    def search_date(self, string):
        search_date_result = re.search("\d{2}.\d{2}.\d{4}", string)
        if search_date_result:
            date = search_date_result.group()
            return date



    def parse_revenue_message(self, string, date):
        if date:
            return self.db.revenue(date)
        elif "выручка" == string:
            return self.db.revenue()
        else:
            return "Ошибка! Неверный формат даты. Попробуй еще раз."

    def parse_report_message(self, string, search_date_result):
        if search_date_result and self.db.check_date():
            date = search_date_result.group(0)
            return self.csv_generator.write_csv(date)
        elif "отчет" == string:
            return self.csv_generator.write_csv()
        else:
            return "Ошибка! Неверный формат даты. Попробуй еще раз."