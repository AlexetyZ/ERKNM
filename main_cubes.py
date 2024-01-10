from sys import argv
from sql_cubes import Database
from cubeOpeartion import makeSet as MS


def loadCube(year):
    if len(str(year)) == 4:
        d = Database()
        d.create_table_accepted_objects_kind_tu_day()
        d.create_table_diened_objects_kind_tu_day()

        d.load_objects_kind_tu_day(year, status='accepted')
        d.load_objects_kind_tu_day(year, status='diened')
    else:
        print("year (второй аргумент) должен быть четырехзначным")


def _help():
    text = ("load_cube: [год: int] загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "truncate_cube: удалить все таблицы кубов\n"
            "reload_cube: перезалить кубы - удалить существующие и залить новые")
    print(text)


def main():
    command = argv[1]
    print(command)
    match command:
        case 'load_cube':
            loadCube(int(argv[2]))

        case 'truncate_cube':
            Database().truncateCube()

        case 'reload_cube':
            Database().truncateCube()
            loadCube(int(argv[2]))

        case 'help':
            _help()


if __name__ == '__main__':
    main()
