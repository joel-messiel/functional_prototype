import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()


DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME') 
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

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