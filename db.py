from datetime import datetime
import sqlite3


class Database(object):
    def __init__(self):
        self.path = "/Users/alexander/code/bots/CashboxBot/cashbox_bot.db"

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

    def revenue(self, date):
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

    def sales(self, date):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        if date == "all":
            table_cursor = cursor.execute("SELECT * FROM sales")
        elif date:
            table_cursor = cursor.execute("SELECT * FROM sales WHERE date = '{}'".format(date))
        else:
            table_cursor = cursor.execute("SELECT * FROM sales WHERE date = '{}'"
                                          .format(datetime.strftime(datetime.now(), "%d.%m.%Y")))
        return table_cursor

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
        cursor.execute("SELECT id FROM items ORDER BY name")
        for id_tuple in cursor.fetchall():
            items.append(Item(id_tuple[0]))
        conn.close()
        return items

    def del_last_sale(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_id FROM sales ORDER BY id DESC")
        sale = cursor.fetchone()
        try:
            sale_id, item = sale[0], Item(sale[1])
        except TypeError:
            deleted_item_name = None
        else:
            cursor.execute("DELETE FROM sales WHERE id = {}".format(sale_id))
            conn.commit()
            deleted_item_name = item.name
        finally:
            conn.close()
        return deleted_item_name


class Item(object):
    def __init__(self, id):
        self.id = id
        self.db = Database()
        self.name = self.name()
        self.price = self.price()

    def name(self):
        conn = sqlite3.connect(self.db.path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM items WHERE id = {}".format(self.id))
        item_name = cursor.fetchone()[0]

        conn.close()
        return item_name

    def price(self):
        conn = sqlite3.connect(self.db.path)
        cursor = conn.cursor()

        cursor.execute("SELECT price FROM items WHERE id = {}".format(self.id))
        item_price = cursor.fetchone()[0]

        conn.close()
        return item_price

    def sales(self, date):
        conn = sqlite3.connect(self.db.path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales WHERE date = '{}' AND item_id = {}".
                       format(date, self.id))
        number_of_sales = len(cursor.fetchall())
        conn.close()
        return number_of_sales
