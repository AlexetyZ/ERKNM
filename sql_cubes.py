import datetime

import pymysql
from pprint import pprint
from Dates_manager import getListDaysFromYear
from cubeOpeartion import makeSet as MS
from sys import argv
from Dictionary import group_kinds, risk_categories


class Database:
    def __init__(self):

        self.conn = pymysql.connect(
            user='root',
            password='ntygazRPNautoz',
            host='0.0.0.0',
            port=3308,
            database='cubes'
        )

    def create_table_RHS_tu_objectsKind_risk(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE rhs_tu_ObjectsKind_risk(
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

    def create_table_KNM_by_objects_kind(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE knm_by_objects_kins(
                controllingOrganization VARCHAR(255),
                codeRegion INT, 
                iso VARCHAR(255),
                groupName VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                risk VARCHAR(255),
                kind VARCHAR(255),
                knmType VARCHAR(255),
                status VARCHAR(255),
                objectsCount INT                 
            );"""
            cursor.execute(request)
            self.conn.commit()


    def load_knm_by_kind_objects(self):
        def getLoad(_set):
            _set = [[cell['controllingOrganization'],
                     cell['codeRegion'],
                     cell['risk'],
                     cell['iso'],
                     cell['groupName'],
                     cell['startDateEn'], cell['month'], cell['year'], cell['kind'], cell['knmType'], cell['status'],
                     cell['objectsCount']] for cell in _set]

            with self.conn.cursor() as cursor:
                request = f"""INSERT INTO knm_by_objects_kins(
                                controllingOrganization,
                                codeRegion, 
                                risk,
                                iso,
                                groupName,
                                startDateEn,
                                month,
                                year,
                                kind,
                                knmType,
                                status,
                                objectsCount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                cursor.executemany(request, _set)
            self.conn.commit()

        for risk in risk_categories:
            for groupName, kinds in group_kinds.items():
                _set = MS.makeKNMByObjectsKind(groupName, kinds, str(risk).lower(), notIn=False)
                getLoad(_set)
            else:
                allKinds = []
                [allKinds.extend(a) for a in group_kinds.values()]
                _set = MS.makeKNMByObjectsKind('Иные виды деятельности', allKinds, str(risk).lower(),  notIn=True)
                try:
                    getLoad(_set)
                except Exception as ex:
                    raise Exception(ex)

        print(f'заполнена таблица проверок в отношении разных групп объектов контроля- {datetime.datetime.now()}')

    def create_table_accepted_objects_kind_tu_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE acceptedObjects_kind_tu_day(
                id VARCHAR(255),
                objectsKind TEXT,
                controllingOrganization VARCHAR(255),
                codeRegion INT, 
                iso VARCHAR(255),
                status VARCHAR(255),
                knmtype VARCHAR(255),
                kind VARCHAR(255),
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
        print(f'заполнена таблица период согласования с прокуратурой внеплановых проверок - {datetime.datetime.now()}')

    def create_table_denied_objects_kind_tu_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE deniedObjects_kind_tu_day(
                objectsKind TEXT,
                controllingOrganization VARCHAR(255), 
                codeRegion INT,
                iso VARCHAR(255),
                status VARCHAR(255),
                knmtype VARCHAR(255),
                kind VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                objectsCount INT, 
                groupKind TEXT
            );"""
            cursor.execute(request)
            self.conn.commit()

    def load_objects_kind_tu_day(self, status: str = 'accepted'):
        _set = MS.makeObjectsKindTuDateSet(status)
        _set = [[cell['objectsKind'], cell['controllingOrganization'], cell['codeRegion'], cell['iso'], cell['status'], cell['knmtype'], cell['kind'], cell['startDateEn'], cell['month'], cell['year'], cell['objectsCount'], cell['groupKind']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO {status}Objects_kind_tu_day(
                objectsKind, 
                controllingOrganization,
                codeRegion, 
                iso, 
                status, 
                knmtype,
                kind,
                startDateEn, 
                month,
                year,
                objectsCount,
                groupKind
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()
        print(f'заполнена таблица объект ТУ вид_объекта - {datetime.datetime.now()}')

    def load_RHS_tu_objectsKind_risk(self):
        _set = MS.makeRHStuobjectsKindriskSet()
        _set = [[cell['controllingOrganization'], cell['objectsKind'], cell['codeRegion'], cell['iso'],
                 cell['groupKind'], cell['actualRisk'], cell['objectsCount']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO rhs_tu_ObjectsKind_risk(
                controllingOrganization,
                objectsKind,
                codeRegion, 
                iso,
                groupKind,
                actualRisk,
                objectsCount  
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()
        print(f'заполнена таблица РХС ТУ вид_объекта риск - {datetime.datetime.now()}')

    def load_RHS_tu_okved_risk(self):
        _set = MS.makeRHStuOkvedKindriskSet()
        _set = [[cell['controllingOrganization'], cell['okvedName'], cell['codeRegion'], cell['iso'],
                 cell['actualRisk'], cell['objectsCount']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO rhs_tu_okved_risk(
                controllingOrganization,
                okved,
                codeRegion, 
                iso,
                actualRisk,
                objectsCount   
            ) VALUES (%s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()
            print(f'заполнена таблица РХС ТУ ОКВЭД риск - {datetime.datetime.now()}')


    def truncateCube(self):
        with self.conn.cursor() as cursor:
            tables = "SHOW TABLES;"
            iskl = ['rhs_tu_ObjectsKind_risk', 'rhs_tu_okved_risk']
            cursor.execute(tables)
            existedTables = [table[0] for table in cursor.fetchall()]
            request = f"""DROP TABLE {', '.join([table for table in existedTables if table not in iskl])}"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_accepted_knm_type_tu_kind_reason_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE acceptedKnm_type_tu_kind_reason_day(
                controllingOrganization VARCHAR(255), 
                iso VARCHAR(255),
                codeRegion INT,
                status VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                knmType VARCHAR(255),
                kind VARCHAR(255),
                reason VARCHAR(512),
                objectsCount INT 
            );"""
            cursor.execute(request)
            self.conn.commit()

    def create_table_denied_knm_type_tu_kind_reason_day(self):
        with self.conn.cursor() as cursor:
            request = f"""CREATE TABLE deniedKnm_type_tu_kind_reason_day(
                controllingOrganization VARCHAR(255), 
                iso VARCHAR(255),
                codeRegion INT,
                status VARCHAR(255),
                startDateEn DATE,
                month INT,
                year INT,
                knmType VARCHAR(255),
                kind VARCHAR(255),
                reason VARCHAR(512),
                objectsCount INT 
            );"""
            cursor.execute(request)
            self.conn.commit()

    def knm_type_tu_kind_reason_day(self, year: int = 2024, status: str = 'accepted'):
        _set = MS.makeKnmTypeTuDateSet(status)
        _set = [[cell['controllingOrganization'], cell['iso'], cell['codeRegion'], cell['status'], cell['startDateEn'], cell['month'], cell['year'], cell['knmtype'],
                 cell['kind'], cell['reason'], cell['objectsCount']] for cell in _set]
        with self.conn.cursor() as cursor:
            request = f"""INSERT INTO {status}Knm_type_tu_kind_reason_day(
                controllingOrganization, 
                iso,
                codeRegion,
                status,
                startDateEn,
                month,
                year,
                knmType,
                kind,
                reason,
                objectsCount 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.executemany(request, _set)
            self.conn.commit()


def _help():
    text = ("load_cube: [год: int] загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "")
    print(text)

def main(year):
    if len(str(year)) == 4:

        d = Database()
        d.create_table_accepted_objects_kind_tu_day(year)
        d.create_table_denied_objects_kind_tu_day(year)

        d.load_objects_kind_tu_day(status='accepted')
        d.load_objects_kind_tu_day(status='denied')


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



