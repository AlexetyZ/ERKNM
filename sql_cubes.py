import pymysql
from pprint import pprint
from Dates_manager import getListDaysFromYear


class Database:
    def __init__(self):

        self.conn = pymysql.connect(
            user='root',
            password='ntygazRPNautoz',
            host='127.0.0.1',
            port=3310,
            database='cubes'
        )

    def create_table_accepted_kmn_kind_tu_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE acceptedKnm_kind_tu_day(
                kind VARCHAR(255),
                tu_name VARCHAR(255), 
                tu_iso VARCHAR(255), 
                date DATE
            );"""
            cursor.execute(request)
            self.conn.commit()


if __name__ == '__main__':
    year = '2024'
    d = Database()


    # d.create_table_accepted_kmn_kind_tu_day()
