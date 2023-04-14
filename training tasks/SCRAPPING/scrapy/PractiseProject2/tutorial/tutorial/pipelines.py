import sqlite3
from sqlite3 import Error

from scrapy.exceptions import DropItem

from .sqlite_database import Sqlite3Database


class Quote1Pipeline:
    def process_item(self, item, spider):
        if not item.get('page'):
            raise DropItem('No page number is provided.')  # if this is hot, it will not pass to next pipeline
        return item


class QuotePipeline:
    db_file = 'quotes.db'

    def __init__(self):
        self.db = None

    def open_spider(self, spider):
        self.db = Sqlite3Database('_'.join([spider.name, self.db_file]))
        table_creation = """CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY,
            page INT NOT NULL,
            quote VARCHAR(500) NOT NULL
        )"""
        self.db.execute_query(table_creation)

    def process_item(self, item, spider):
        print(item, '>>>>>>>>>>>>>>>>>>>>>>>>')
        current_page = item['page']

        for value in [f'({current_page}, "{quote}")' for quote in item['name']]:
            query = f"""INSERT INTO quotes(page, quote) VALUES {value};"""
            self.db.execute_query(query)
        return item

    # def close_spider(self, spider):
    #     self.client.close()
