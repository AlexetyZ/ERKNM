from sys import argv
from sql_cubes import Database
from cubeOpeartion import makeSet as MS


def loadCube():
    d = Database()
    try:
        d.create_table_RHS_tu_objectsKind_risk()
        d.create_table_RHS_tu_okved_risk()
    except:
        pass

    d.load_RHS_tu_objectsKind_risk()
    d.load_RHS_tu_okved_risk()


def loadCubeYear(year):
    if len(str(year)) == 4:
        d = Database()
        try:
            d.create_table_accepted_objects_kind_tu_day(year)
            d.create_table_diened_objects_kind_tu_day(year)
        except:
            pass

        d.load_objects_kind_tu_day(year, status='accepted')
        d.load_objects_kind_tu_day(year, status='diened')
    else:
        print("year (второй аргумент) должен быть четырехзначным")


def _help():
    text = ("load_cube: [год YYYY или года в формате YYYY-YYYY] загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "truncate_cube: удалить все таблицы кубов\n"
            "reload_cube: перезалить кубы - удалить существующие и залить новые")
    print(text)


def mainLoad(arg2: str):
    # for year in [int(year) for year in arg2.split('-')]:
    #     loadCubeYear(year)
    loadCube()


def main():
    command = argv[1]
    print(command)
    match command:
        case 'load_cube':
            mainLoad(argv[2])

        case 'truncate_cube':
            Database().truncateCube()

        case 'reload_cube':
            Database().truncateCube()
            mainLoad(argv[2])

        case 'help':
            _help()


if __name__ == '__main__':
    main()
