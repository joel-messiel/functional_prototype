import pymysql
import pymysql.cursors

DB_URL = '127.0.0.1'
DB_NAME = 'prototype_db'
DB_PORT = 3306
DB_USER = 'joelm12pr'
DB_PASSWORD = '03M0nch!tOMl'

# Use this to access database
class Dbconnect:
    def __init__(self) -> None:
        # This is the DB we are using for testing from home must change it to given DB
        self.connection = pymysql.connect(host=DB_URL,
                                          database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def select(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)

        result = self.cursor.fetchall()
        return result

    def execute(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.connection.commit()