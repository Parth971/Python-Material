import sqlite3
from sqlite3 import Error


class Sqlite3Database:
    def __init__(self, database_file):
        self.db_file = database_file

    @classmethod
    def get_cursor(cls, connection):
        return connection.cursor()

    def get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def execute_query(self, query):
        connection = self.get_connection()
        cursor = self.get_cursor(connection)
        try:
            cursor.execute(query)
            connection.commit()
        except Error as err:
            connection.rollback()
            print(f'Failed! {err}')
            return 0
        finally:
            cursor.close()
            connection.close()
        return 1

    def read_query(self, query):
        result = None
        connection = self.get_connection()
        cursor = self.get_cursor(connection)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except Error as err:
            print(f'Failed! {err}')
        finally:
            cursor.close()
            connection.close()
        return result
