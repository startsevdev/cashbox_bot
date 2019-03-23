from datetime import datetime
import sqlite3


class Database(object):
    def __init__(self, path):
        self.path = path

    def add_item(self, name):
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM items WHERE name = '{}'".format(name))
        try:
            item_id = cursor.fetchone()[0]
        except TypeError:
            return "Ошибка! Такого товара нет в меню. Попробуй еще раз."
        else:
            cursor.execute("INSERT INTO sales VALUES (Null, {}, '{}')".format(item_id, date))
            conn.commit()
            return "{} added".format(name)
        finally:
            conn.close()