import sqlite3


class TutorialPipeline:
    def __init__(self):
        self.cur = None
        self.con = None

    def open_spider(self, spider):
        self.con = sqlite3.connect('cricket.db')
        self.cur = self.con.cursor()
        self.cur.execute('''DROP TABLE IF EXISTS cricket''')
        self.cur.execute('''CREATE TABLE cricket
                       (title text, created text, a text, content text, image_url text)''')
        self.con.commit()
        
    def close_spider(self, spider):
        self.con.close()

    def process_item(self, item, spider):
        self.cur.execute(
            '''insert into cricket values (?, ?, ?, ?, ?)''',
            (
                item['title'], item['date'], item['a'], item['content'], item['image_url']
            )
        )
        self.con.commit()
        return item

