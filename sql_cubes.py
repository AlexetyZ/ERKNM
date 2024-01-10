import pymysql
from pprint import pprint
from Dates_manager import getListDaysFromYear
from cubeOpeartion import makeSet as MS
from sys import argv


class Database:
    def __init__(self):

        self.conn = pymysql.connect(
            user='root',
            password='ntygazRPNautoz',
            host='localhost',
            port=3308,
            database='cubes'
        )

    def create_table_accepted_objects_kind_tu_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE acceptedObjects_kind_tu_day(
                objectsKind TEXT,
                controllingOrganization VARCHAR(255), 
                iso VARCHAR(255),
                status VARCHAR(255),
                startDateEn DATE,
                objectsCount INT, 
                groupKind TEXT
            );"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_diened_objects_kind_tu_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE dienedObjects_kind_tu_day(
                objectsKind TEXT,
                controllingOrganization VARCHAR(255), 
                iso VARCHAR(255),
                status VARCHAR(255),
                startDateEn DATE,
                objectsCount INT, 
                groupKind TEXT
            );"""
            cursor.execute(request)
            self.conn.commit()

    def load_objects_kind_tu_day(self, year: int = 2024, status: str = 'accepted'):
        _set = MS.makeObjectsKindTuDateSet(year, status)
        _set = [[cell['objectsKind'], cell['controllingOrganization'], cell['iso'], cell['status'], cell['startDateEn'], cell['objectsCount'], cell['groupKind']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO {status}Objects_kind_tu_day(
                objectsKind, 
                controllingOrganization, 
                iso, 
                status, 
                startDateEn, 
                objectsCount,
                groupKind
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()

    def truncateCube(self):
        tablesToTruncate = ['acceptedObjects_kind_tu_day', "dienedObjects_kind_tu_day"]
        with self.conn.cursor() as cursor:
            tables = "SHOW TABLES"
            cursor.execute(tables)
            existedTables = [table[0] for table in cursor.fetchall()]
            request = f"""DROP TABLE {', '.join([table for table in tablesToTruncate if table in existedTables])}"""
            print(request)
            cursor.execute(request)
            self.conn.commit()


def _help():
    text = ("load_cube: [год: int] загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "")
    print(text)

def main(year):
    if len(str(year)) == 4:

        d = Database()
        d.create_table_accepted_objects_kind_tu_day()
        d.create_table_diened_objects_kind_tu_day()

        d.load_objects_kind_tu_day(year, status='accepted')
        d.load_objects_kind_tu_day(year, status='diened')


    else:
        print("year (второй аргумент) должен быть четырехзначным")


if __name__ == '__main__':
    command = argv[1]
    match command:
        case 'load_cube':
            main(int(argv[2]))

        case 'truncate_cube':
            Database().truncateCube()

        case 'reload_cube':
            Database().truncateCube()
            main(int(argv[2]))

        case 'help':
            _help()



