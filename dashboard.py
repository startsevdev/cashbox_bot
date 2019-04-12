from db import Database


class Dashboard(object):
    def __init__(self):
        self.db = Database()

    def day_board(self):
        message = "Продано:\n"
        items = self.db.items_list()
        for item in items:
            message += f"{item.name} - {item.sales} шт.\n"
        message += f"\nВыручка: {self.db.revenue()} р"
        return message

d = Dashboard()
r = d.day_board()
print(r)