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
            bot_message = None
        else:
            cursor.execute("INSERT INTO sales VALUES (Null, {}, '{}', '{}')".format(item_id, date, time))
            conn.commit()
            bot_message = name
        finally:
            conn.close()
        return bot_message

    def revenue(self, date=datetime.strftime(datetime.now(), "%d.%m.%Y")):
        prices = []

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("SELECT item_id FROM sales WHERE date = '{}'".format(date))
        item_ids = cursor.fetchall()
        for item_id in item_ids:
            cursor.execute("SELECT price FROM items WHERE id = {}".format(item_id[0]))
            prices.append(cursor.fetchone()[0])
        conn.close()
        return sum(prices)

    def all_sales(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        table_cursor = cursor.execute("SELECT * FROM sales")
        return table_cursor

    def date_sales(self, date):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        table_cursor = cursor.execute("SELECT * FROM sales WHERE date = '{}'".format(date))
        return table_cursor

    def item_name(self, item_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM items WHERE id = {}".format(item_id))
        item_name = cursor.fetchone()[0]

        conn.close()
        return item_name

    def item_price(self, item_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("SELECT price FROM items WHERE id = {}".format(item_id))
        item_price = cursor.fetchone()[0]

        conn.close()
        return item_price

    def check_date(self, date):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM sales WHERE date = '{}'".format(date))
        try:
            sale = cursor.fetchone()[0]
        except TypeError:
            date_exists = False
        else:
            date_exists = True
        finally:
            conn.close()
        return date_exists

    def items_list(self):
        items = []
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM items ORDER BY id")
        for name_tuple in cursor.fetchall():
            items.append(name_tuple[0])
        return items

    def del_last_sale(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_id FROM sales ORDER BY id DESC")
        sale = cursor.fetchone()
        try:
            sale_id, item_id = sale[0], sale[1]
        except TypeError:
            deleted_item_name = None
        else:
            cursor.execute("DELETE FROM sales WHERE id = {}".format(sale_id))
            conn.commit()
            deleted_item_name = self.item_name(item_id)
        finally:
            conn.close()
        return deleted_item_name
