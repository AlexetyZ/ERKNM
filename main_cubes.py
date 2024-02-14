from sys import argv
from sql_cubes import Database
from datetime import datetime
from cubeOpeartion import makeSet as MS


def loadCube():
    print(f'начало операции - {datetime.now()}')
    d = Database()
    funcs = [
        d.create_table_prosecutor_apply_period,
        d.create_table_RHS_tu_objectsKind_risk,
        d.create_table_RHS_tu_okved_risk,
        d.create_table_denied_knm_type_tu_kind_reason_day,
        d.create_table_accepted_knm_type_tu_kind_reason_day,
        d.create_table_accepted_objects_kind_tu_day,
        d.create_table_denied_objects_kind_tu_day,
        d.create_table_KNM_by_objects_kind,
        d.create_table_KNM_by_ordinary,

    ]
    for func in funcs:
        try:
            func()
        except Exception as ex:
            print(func.__name__, ex)

    # d.load_RHS_tu_objectsKind_risk()
    # d.load_RHS_tu_okved_risk()
    d.load_prosecutor_apply_period()

    d.load_objects_kind_tu_day(status='accepted')
    d.load_objects_kind_tu_day(status='denied')

    d.knm_type_tu_kind_reason_day(status='accepted')
    d.knm_type_tu_kind_reason_day(status='denied')

    d.load_knm_by_kind_objects()
    d.load_knm_by_ordinary()


def _help():
    text = ("load_cube: загрузить куб, при условии, что есть чистая база данных без предыдущих кубов\n"
            "truncate_cube: удалить все таблицы кубов\n"
            "reload_cube: перезалить кубы - удалить существующие и залить новые")
    print(text)


def main():
    command = argv[1]
    print(command)
    match command:
        case 'load_cube':
            loadCube()

        case 'truncate_cube':
            Database().truncateCube()

        case 'reload_cube':
            Database().truncateCube()
            loadCube()

        case 'help':
            _help()


if __name__ == '__main__':
    main()
