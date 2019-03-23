from datetime import datetime
import sqlite3


class Database(object):
    def __init__(self, path):
        self.path = path

    def add_sale(self, name):
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")
        time = datetime.strftime(datetime.now(), "%H:%M:%S")

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM items WHERE name = '{}'".format(name))
        try:
            item_id = cursor.fetchone()[0]
        except TypeError:
            return "Ошибка! Такого товара нет в меню. Попробуй еще раз."
        else:
            cursor.execute("INSERT INTO sales VALUES (Null, {}, '{}', '{}')".format(item_id, date, time))
            conn.commit()
            return "{} added".format(name)
        finally:
            conn.close()

    def revenue(self):
        prices = []
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT item_id FROM sales WHERE date = '{}'".format(date))
        item_ids = cursor.fetchall()
        for item_id in item_ids:
            cursor.execute("SELECT price FROM items WHERE id = {}".format(item_id[0]))
            prices.append(cursor.fetchone()[0])
        return sum(prices)
