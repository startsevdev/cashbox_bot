import re
from db import Database

db = Database("/Users/alexander/code/bots/CashboxBot/data.db")


class Parser(object):
    def parse_mesage(self, string):
        string = string.lower()
        if "выручка" in string:
            return self.parse_revenue_message(string)
        elif "отчет" in string:
            return self.parse_report_message(string)
        else:
            return db.add_sale(string)

    def parse_revenue_message(self, string):
        search_date_result = re.search("\d{2}.\d{2}.\d{4}", string)
        if search_date_result:
            date = search_date_result.group(0)
            return db.revenue(date)
        elif "выручка" == string:
            return db.revenue()
        else:
            return "Ошибка! Неверный формат даты. Попробуй еше раз."

    def parse_report_message(self, string):
        search_date_result = re.search("\d{2}.\d{2}.\d{4}", string)
        if search_date_result:
            date = search_date_result.group(0)
            return "generate_csv(date)"
        elif "отчет" == string:
            return "generate_csv()"
        else:
            return "Ошибка! Неверный формат даты. Попробуй еше раз."
