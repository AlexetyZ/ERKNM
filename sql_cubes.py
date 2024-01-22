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
            host='10.1.13.137',
            port=3308,
            database='cubes'
        )

    def create_table_RHS_tu_objectsKind_risk(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE rhs_tu_ObjectsKind_risk(
                id VARCHAR(255),
                controllingOrganization VARCHAR(255),
                objectsKind TEXT,
                codeRegion INT, 
                iso VARCHAR(255),
                groupKind TEXT,
                actualRisk VARCHAR(255),
                objectsCount INT                
            );"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_RHS_tu_okved_risk(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE rhs_tu_okved_risk(
                id VARCHAR(255),
                controllingOrganization VARCHAR(255),
                okved TEXT,
                codeRegion INT, 
                iso VARCHAR(255),
                actualRisk VARCHAR(255),
                objectsCount INT                 
            );"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_accepted_objects_kind_tu_day(self, year):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE acceptedObjects_kind_tu_day_{year}(
                id VARCHAR(255),
                objectsKind TEXT,
                controllingOrganization VARCHAR(255),
                codeRegion INT, 
                iso VARCHAR(255),
                status VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                objectsCount INT, 
                groupKind TEXT
            );"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_prosecutor_apply_period(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE prosecutorAply(
                id INT PRIMARY KEY AUTO_INCREMENT,
                difference INT,
                avgsumdate INT,
                codeRegion INT,
                controllingOrganization VARCHAR(255),
                iso VARCHAR(255),
                orderDate DATE,
                responceDate DATE,
                objectsCount INT,
                year INT
            );"""
            cursor.execute(request)
            self.conn.commit()


    def load_prosecutor_apply_period(self):
        _set = MS.make_prosecutor_apply_period()
        _set = [[cell['difference'], cell['avgsumdate'], cell['codeRegion'], cell['controllingOrganization'], cell['iso'], cell['orderDate'], cell['responceDate'],
                 cell['objectsCount'], cell['year']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO prosecutorAply(
                            difference,
                            avgsumdate,
                            codeRegion,
                            controllingOrganization,
                            iso,
                            orderDate,
                            responceDate,
                            objectsCount,
                            year
                         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()

    def create_table_diened_objects_kind_tu_day(self, year):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE dienedObjects_kind_tu_day_{year}(
                objectsKind TEXT,
                controllingOrganization VARCHAR(255), 
                codeRegion INT,
                iso VARCHAR(255),
                status VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                objectsCount INT, 
                groupKind TEXT
            );"""
            cursor.execute(request)
            self.conn.commit()

    def load_objects_kind_tu_day(self, year: int = 2024, status: str = 'accepted'):
        _set = MS.makeObjectsKindTuDateSet(year, status)
        _set = [[cell['objectsKind'], cell['controllingOrganization'], cell['codeRegion'], cell['iso'], cell['status'], cell['startDateEn'], cell['month'], cell['year'], cell['objectsCount'], cell['groupKind']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO {status}Objects_kind_tu_day_{year}(
                objectsKind, 
                controllingOrganization,
                codeRegion, 
                iso, 
                status, 
                startDateEn, 
                month,
                year,
                objectsCount,
                groupKind
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()

    def load_RHS_tu_objectsKind_risk(self):
        _set = MS.makeRHStuobjectsKindriskSet()
        _set = [[cell['id'], cell['controllingOrganization'], cell['objectsKind'], cell['codeRegion'], cell['iso'],
                 cell['groupKind'], cell['actualRisk'], cell['objectsCount']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO rhs_tu_ObjectsKind_risk(
                id,
                controllingOrganization,
                objectsKind,
                codeRegion, 
                iso,
                groupKind,
                actualRisk,
                objectsCount  
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()
            print('заполнена таблица РХС ТУ вид_объекта риск')

    def load_RHS_tu_okved_risk(self):
        _set = MS.makeRHStuOkvedKindriskSet()
        _set = [[cell['id'], cell['controllingOrganization'], cell['okvedName'], cell['codeRegion'], cell['iso'],
                 cell['actualRisk'], cell['objectsCount']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO rhs_tu_okved_risk(
                id,
                controllingOrganization,
                okved,
                codeRegion, 
                iso,
                actualRisk,
                objectsCount   
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()
            print('заполнена таблица РХС ТУ вид_объекта риск')

    def truncateCube(self):
        with self.conn.cursor() as cursor:
            tables = "SHOW TABLES;"
            cursor.execute(tables)
            existedTables = [table[0] for table in cursor.fetchall()]
            print(f"{existedTables=}")
            request = f"""DROP TABLE {', '.join([table for table in existedTables])}"""
            print(f"{request=}")
            cursor.execute(request)
            self.conn.commit()


def _help():
    text = ("load_cube: [год: int] загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "")
    print(text)

def main(year):
    if len(str(year)) == 4:

        d = Database()
        d.create_table_accepted_objects_kind_tu_day(year)
        d.create_table_diened_objects_kind_tu_day(year)

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



