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
        item_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO sales VALUES (Null, {}, '{}')".format(item_id, date))
        conn.commit()
        conn.close()
