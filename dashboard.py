from db import Database


class Dashboard(object):
    def __init__(self):
        self.db = Database()

    def day_board(self, date):
        message = "Продано:\n"
        items = self.db.items_list()
        for item in items:
            message += f"{item.name} - {item.sales(date)} шт.\n"
        message += f"\nВыручка: {self.db.revenue(date)} р"
        return message
