import os.path
from sys import argv
from tqdm import tqdm
from pprint import pprint


def load_knm(year):
    from ERKNM_http import Erknm
    Erknm().get_all_knm_for_a_year(year=year)


def load_pm(year):
    from ERKNM_http import Erknm
    Erknm().get_all_pm_for_a_year(year=year)


def reportByObjects(pathFile, filters: str):
    from mongo_database import WorkMongo
    import xl
    import json

    filters = json.loads(filters.replace("'", '"')) if filters else {}
    wm = WorkMongo()
    _objects = wm.reportByObjects(**filters)
    results = wm.convertForsaving(list(_objects))
    xl.writeResultsInXL(title=results[0], results=results[1], pathFile=pathFile)


def mergeTu(path, col_number):
    import xl
    tu_list = xl.bringCol(path, col_number)
    return xl.merge_tu(tu_list)


def reportByRisks(pathFile, filters: str):
    from mongo_database import WorkMongo
    import xl
    import json

    filters = json.loads(filters.replace("'", '"')) if filters else {}
    wm = WorkMongo()
    _objects = wm.reportByRisk(**filters)
    results = wm.convertForsaving(list(_objects))
    xl.writeResultsInXL(title=results[0], results=results[1], pathFile=pathFile)


def reportByFreeCommand(pathFile, command):
    from mongo_database import WorkMongo
    import xl
    import json

    filters = json.loads(command.replace("'", '"')) if command else {}
    wm = WorkMongo()
    _objects = wm.free_command(filters)
    results = wm.convertForsaving(list(_objects))
    xl.writeResultsInXL(title=results[0], results=results[1], pathFile=pathFile)


def reportByProsecutorComments(pathFile):
    from mongo_database import WorkMongo
    import xl
    import json

    wm = WorkMongo()
    _objects = wm.reportFromDeniedKNMComment()
    results = wm.convertForsaving(list(_objects))
    xl.writeResultsInXL(title=results[0], results=results[1], pathFile=pathFile)
    return 'Причины исключений успешно выгружены!'


def reportByDienedObjects(countBy):
    from mongo_database import WorkMongo
    import xl
    from pathlib import Path
    import os
    import json
    from datetime import datetime
    import Dictionary as d
    from private_config import dayliProcessFile

    group_kinds = {
        'Деятельность в сфере здравоохранения': d.health_care_kinds,
        'Детские лагеря с дневным пребыванием': d.child_camps_kinds,
        'Деятельность организаторов детского питания': d.children_meal_kinds,
        'Деятельность общеобразовательных организаций': d.school_kinds,
        'Деятельность дошкольных образовательных организаций': d.preschool_kinds,
        'Торговля пищевыми продуктами': d.food_store_kind,
        'Объекты промышленности и транспорта': d.industry_kinds,
        'Производство пищевых продуктов': d.food_production,
        'Общественное питание населения': d.public_catering_kind,
        'Деятельность водоснабжения и водоотведения': d.water_supply_kinds,
        'Коммунальное обслуживание': d.communal_services,
        'Деятельность по предоставлению персональных услуг': d.personal_services,
        'Деятельность гостиниц и прочих мест для временного проживания': d.motels,
        'Предоставление социальных услуг': d.social_services,
    }

    t_data = datetime.now().strftime('%d.%m.%Y')

    wm = WorkMongo()
    _tus_kinds_counts = wm.reportFromDeniedKNMObjectCategory() if countBy == 'objects' else wm.reportFromDeniedKNMObjectCategoryKNM()

    results = {'Всего': {'Общее': 0}}
    value_list = []
    # print(results['Всего']['Общее'])
    otherKinds = []
    for tu_object_count in _tus_kinds_counts:
        recordId = tu_object_count['_id']
        count = tu_object_count['totalCount']
        tu = recordId['tu']
        kind = recordId['kind']
        isOther = True
        for groupName, groupRefs in group_kinds.items():
            if kind in groupRefs:
                kind = groupName
                isOther = False
        if isOther:
            otherKinds.append(kind)
            kind = 'Прочие виды деятельности'

        if tu in results:
            # print(results[tu])
            if kind in results[tu]:
                results[tu][kind] += count
            else:
                results[tu][kind] = count
            results[tu]['Общее'] += count

        else:
            results[tu] = {'Общее': count, kind: count}
        if kind in results['Всего']:
            results['Всего'][kind] += count
        else:
            results['Всего'][kind] = count
        # pprint(results)
        results['Всего']['Общее'] += count

    results = dict(sorted(results.items(), key=lambda x: x[1]['Общее'], reverse=True))
    # pprint(results)
    results['Всего'] = dict((sorted(results['Всего'].items(), key=lambda x: x[1], reverse=True)))

    value_list.append(['№', 'ТУ', *[key for key in results['Всего'].keys()]])
    # for main_kind in results['Всего'].keys():+

    # print(list(results['Всего'].keys()))
    for number, (tu, kinds) in enumerate(results.items()):
        # print(kinds)
        value_list.append([number if number else '', tu,
                           *[kinds[val] if val in kinds else 0 for val in list(results['Всего'].keys())]])

    pathFile = dayliProcessFile(f"отчет по отклоненным объектам {t_data} {countBy}.xlsx")

    xl.writeResultsInXL(results=value_list,
                        title=f'Структура по видам деятельности объектов, исключенных из плана прокуратурой на {t_data}' if countBy == 'objects' else f'Структура КНМ по видам деятельности объектов, исключенных из плана прокуратурой на {t_data}',
                        pathFile=pathFile)
    xl.writeResultsInXL(results=[kind for kind in set(otherKinds)], title=f'Прочие виды деятельности',
                        pathFile=pathFile, sheetTitle='прочие', sheetIndex=1)
    pathFileStr = str(pathFile).replace("\\\\", "\\")
    # pprint(otherKinds)
    return f'Отчет готов! Сохранен в {pathFileStr}'


def reportByAccepedObjects(countBy):
    from mongo_database import WorkMongo
    import xl
    from pathlib import Path
    import os
    import json
    from datetime import datetime
    import Dictionary as d
    from private_config import dayliProcessFile

    group_kinds = {
        'Деятельность в сфере здравоохранения': d.health_care_kinds,
        'Детские лагеря с дневным пребыванием': d.child_camps_kinds,
        'Деятельность организаторов детского питания': d.children_meal_kinds,
        'Деятельность общеобразовательных организаций': d.school_kinds,
        'Деятельность дошкольных образовательных организаций': d.preschool_kinds,
        'Торговля пищевыми продуктами': d.food_store_kind,
        'Объекты промышленности и транспорта': d.industry_kinds,
        'Производство пищевых продуктов': d.food_production,
        'Общественное питание населения': d.public_catering_kind,
        'Деятельность водоснабжения и водоотведения': d.water_supply_kinds,
        'Коммунальное обслуживание': d.communal_services,
        'Деятельность по предоставлению персональных услуг': d.personal_services,
        'Деятельность гостиниц и прочих мест для временного проживания': d.motels,
        'Предоставление социальных услуг': d.social_services,
    }

    t_data = datetime.now().strftime('%d.%m.%Y')

    wm = WorkMongo()
    _tus_kinds_counts = wm.reportFromAcceptKNMObjectCategory()

    results = {'Всего': {'Общее': 0}}
    value_list = []
    # print(results['Всего']['Общее'])
    otherKinds = []
    for tu_object_count in _tus_kinds_counts:
        recordId = tu_object_count['_id']
        count = tu_object_count['totalCount']
        tu = recordId['tu']
        kind = recordId['kind']
        isOther = True
        for groupName, groupRefs in group_kinds.items():
            if kind in groupRefs:
                kind = groupName
                isOther = False
        if isOther:
            otherKinds.append(kind)
            kind = 'Прочие виды деятельности'

        if tu in results:
            # print(results[tu])
            if kind in results[tu]:
                results[tu][kind] += count
            else:
                results[tu][kind] = count
            results[tu]['Общее'] += count

        else:
            results[tu] = {'Общее': count, kind: count}
        if kind in results['Всего']:
            results['Всего'][kind] += count
        else:
            results['Всего'][kind] = count
        # pprint(results)
        results['Всего']['Общее'] += count

    results = dict(sorted(results.items(), key=lambda x: x[1]['Общее'], reverse=True))
    # pprint(results)
    results['Всего'] = dict((sorted(results['Всего'].items(), key=lambda x: x[1], reverse=True)))

    value_list.append(['№', 'ТУ', *[key for key in results['Всего'].keys()]])
    # for main_kind in results['Всего'].keys():+

    # print(list(results['Всего'].keys()))
    for number, (tu, kinds) in enumerate(results.items()):
        # print(kinds)
        value_list.append([number if number else '', tu,
                           *[kinds[val] if val in kinds else 0 for val in list(results['Всего'].keys())]])

    pathFile = dayliProcessFile(f"отчет по согласованным объектам {t_data} {countBy}.xlsx")

    xl.writeResultsInXL(results=value_list,
                        title=f'Структура по видам деятельности объектов, согласованных прокуратурой на {t_data}' if countBy == 'objects' else f'Структура КНМ по видам деятельности объектов, согласованных прокуратурой на {t_data}',
                        pathFile=pathFile)
    xl.writeResultsInXL(results=[kind for kind in set(otherKinds)], title=f'Прочие виды деятельности',
                        pathFile=pathFile, sheetTitle='прочие', sheetIndex=1)
    pathFileStr = str(pathFile).replace("\\\\", "\\")
    # pprint(otherKinds)
    return f'Отчет готов! Сохранен в {pathFileStr}'


def reportByAggreedProcess(pathFile, today, count_by='knm'):
    from mongo_database import WorkMongo
    import xl
    from pathlib import Path
    import os
    import json

    parentDir = Path(pathFile).parent
    previewsResultFile = os.path.join(parentDir, f'preview_results {count_by}.json')
    value_list = []
    results = {}
    statusses = []
    wm = WorkMongo()
    if count_by == 'knm':
        _objects = wm.reportByAggreedProcessKNM()
    elif count_by == 'objects':
        _objects = wm.reportByAggreedProcessObjects()
    else:
        return 'Не удалось распознать дополнительный аттрибут, по которому будет подсчет!'
    for _object in _objects:
        id_part = _object['_id']
        name = id_part['tu']
        status = id_part['status']
        count = _object['totalCount']
        statusses.append(status)
        if name in results:
            results[name][status] = count  # ТУ с определенным статусом попадается только 1 раз
        else:
            results[name] = {status: count}
    statusses = set(statusses)
    onApplyKinds = ['Есть замечания', 'На согласовании', 'Исключена', 'Готово к согласованию', 'Ожидает проведения',
                    'Не согласована']
    registredExcludedKnm = []
    totalExcluded = {'total': 0, 'excluded': 0, 'persentExcludedTotal': 0, 'onApply': 0, 'applied': 0,
                     'increaseExcluded': 0,
                     'persentExcludedOnDate': 0}
    if not os.path.exists(previewsResultFile):

        for tu, values in results.items():
            tuIncreaseExcluded = 0
            v = []
            onApplyCount = 0
            for s in statusses:
                if s in values:
                    if s in onApplyKinds:
                        onApplyCount += values[s]
                    v.append(values[s])

                    v.append(0)
                else:
                    v.append(0)
                    v.append(0)
            totalExcluded['total'] += onApplyCount
            isNotes = values['Есть замечания'] if 'Есть замечания' in values else 0
            waitForStarting = values['Ожидает проведения'] if 'Ожидает проведения' in values else 0
            totalExcluded['applied'] += isNotes + waitForStarting
            onApply = values['На согласовании'] if 'На согласовании' in values else 0
            totalExcluded['onApply'] += onApply
            if 'Исключена' in values:
                excluded = values['Исключена']
                if excluded:
                    existExcluded = [tu, onApplyCount, excluded]
                    totalExcluded['excluded'] += excluded
                    persentExcludedTotal = excluded / onApplyCount
                    existExcluded.append(persentExcludedTotal)
                    existExcluded.append(onApply)
                    applied = isNotes + waitForStarting
                    existExcluded.append(applied)
                    existExcluded.append(tuIncreaseExcluded)
                    totalExcluded['increaseExcluded'] += tuIncreaseExcluded
                    persentExcludedOnDate = tuIncreaseExcluded / onApplyCount
                    existExcluded.append(persentExcludedOnDate)
                    registredExcludedKnm.append(existExcluded)

            value_list.append([tu, *v, onApplyCount])

    else:
        with open(previewsResultFile, 'r', encoding='utf-8') as previewsFile:
            previewsResult = json.load(previewsFile)

        for tu, values in results.items():
            tuIncreaseExcluded = 0
            v = []
            onApplyCount = 0

            for s in statusses:
                if s in values:
                    if s in onApplyKinds:
                        onApplyCount += values[s]

                    v.append(values[s])

                    tuIncrease = values[s] - previewsResult[tu][s] if s in previewsResult[tu] else values[s]
                    if s == "Исключена":
                        tuIncreaseExcluded = tuIncrease

                    v.append(tuIncrease)
                else:
                    v.append(0)
                    v.append(0)
            totalExcluded['total'] += onApplyCount
            isNotes = values['Есть замечания'] if 'Есть замечания' in values else 0
            waitForStarting = values['Ожидает проведения'] if 'Ожидает проведения' in values else 0
            totalExcluded['applied'] += isNotes + waitForStarting
            onApply = values['На согласовании'] if 'На согласовании' in values else 0
            totalExcluded['onApply'] += onApply

            if 'Исключена' in values:
                excluded = values['Исключена']
                if excluded:
                    existExcluded = [tu, onApplyCount, excluded]
                    totalExcluded['excluded'] += excluded
                    persentExcludedTotal = excluded / onApplyCount
                    existExcluded.append(persentExcludedTotal)
                    existExcluded.append(onApply)
                    applied = isNotes + waitForStarting
                    existExcluded.append(applied)
                    existExcluded.append(tuIncreaseExcluded)
                    totalExcluded['increaseExcluded'] += tuIncreaseExcluded
                    persentExcludedOnDate = tuIncreaseExcluded / onApplyCount
                    existExcluded.append(persentExcludedOnDate)
                    registredExcludedKnm.append(existExcluded)
            value_list.append([tu, *v, onApplyCount])

    excludedReportTitle = [
        '',
        'ТУ',
        "Всего КНМ в проекте плана" if count_by == 'knm' else "Всего объектов в проекте плана",
        "Исключено прокуратурой",
        '% исключенных всего',
        'Осталось на согласовании',
        'Согласовано',
        f'Прирост исключенных за {today}',
        f'% исключенных всего за {today}'
    ]

    totalExcluded['persentExcludedTotal'] = totalExcluded['excluded'] / totalExcluded['total']
    totalExcluded['persentExcludedOnDate'] = totalExcluded['increaseExcluded'] / totalExcluded['total']
    registredExcludedKnm = sorted(registredExcludedKnm, key=lambda x: x[3], reverse=True)
    registredExcludedKnm.insert(0, ['', 'Всего', *[val for val in totalExcluded.values()]])
    registredExcludedKnm.insert(0, excludedReportTitle)
    title = []
    title.append('ТУ')
    for s in statusses:
        title.append(s)
        title.append('прирост')
    title.append('Всего на согласовании')
    xl.writeResultsInXL(results=value_list, title=title, pathFile=pathFile, sheetTitle='Общий отчет')
    xl.writeResultsInXL(results=registredExcludedKnm,
                        title=f'Регионы, в которых зарегистрированы исключения КНМ органами прокуратуры на {today}',
                        pathFile=pathFile, sheetIndex=1, sheetTitle='Исключенные')
    with open(previewsResultFile, 'w', encoding='utf-8') as file:
        json.dump(results, file)


def reportDayliAggreedProcess(count_attribute='knm'):
    from datetime import datetime
    from private_config import dayliProcessFile
    import os
    today = str(datetime.now().strftime('%d.%m.%Y'))
    reportByAggreedProcess(dayliProcessFile(f"ежедневный {today} {count_attribute}.xlsx"), today,
                           count_by=count_attribute)
    isklListPath = dayliProcessFile(f"Исключения {today}.xlsx")
    if not os.path.exists(isklListPath):
        reportByProsecutorComments(isklListPath)
    return 'Отчет готов!'


def findIsklInfo(dirPath):
    import openpyxl
    wb = openpyxl.load_workbook(dirPath)
    sh = wb['причины исключений']
    tu = sh['A1'].value
    iskl_list = []
    for row in sh.iter_rows(min_row=3, values_only=True):
        iskl_list.append([tu, row[1], row[2]])
    return iskl_list


def mergeIskl(pathDir):
    import os
    import xl
    from private_config import dayliProcessFile
    from tqdm import tqdm

    iskl_list = []
    for file in tqdm(os.listdir(pathDir)):
        dirPath = os.path.join(pathDir, file)
        iskl_list.extend(findIsklInfo(dirPath))
    newFile = dayliProcessFile('все причины исключений.xlsx')
    xl.writeResultsInXL(results=iskl_list, pathFile=newFile, title='Совокупность исключений')


def useDatabase():
    from sql import Database
    d = Database(init_erknm=False)
    d.exec_it_database()
    return 'Работа с базой данных завершена!'


def groupByRegions(pathFile):
    import openpyxl
    import xl
    import os
    from datetime import datetime
    from pathlib import Path

    t_date = datetime.now().strftime('%d.%m.%Y')

    parentDir = Path(pathFile).parent

    todayDir = os.path.join(parentDir, f'на {t_date}')
    isklAnalysDir = os.path.join(todayDir, 'анализ исключений')
    if not os.path.exists(todayDir):
        os.mkdir(todayDir)
    if not os.path.exists(isklAnalysDir):
        os.mkdir(isklAnalysDir)

    datas = {}
    wb = openpyxl.load_workbook(pathFile)
    sh = wb.worksheets[0]
    for row in sh.iter_rows(min_row=2, values_only=True):
        tu = row[1]
        if row[1] in datas:
            datas[tu].append(row)
        else:
            datas[tu] = [row]
    for region, rows in datas.items():
        xl.writeResultsInXL([['', 'Причины', 'Встречается в КНМ'], *rows], title=region,
                            pathFile=os.path.join(isklAnalysDir, f'{region}.xlsx'), sheetTitle='Исключения')


def reportByIsklReasons(pathDir):
    import os
    import xl
    from fts import Fts
    from pathlib import Path
    from tqdm import tqdm
    from Dictionary import topIsklReasons
    from private_config import dayliProcessFile

    f = Fts()
    full_dict = {}
    value_list = []
    for file in tqdm(os.listdir(pathDir)):

        if 'xlsx' in file:
            tuName = Path(file).stem
            print(tuName)
            pathFile = os.path.join(pathDir, file)
            cols = xl.bringCol(pathFile, minRow=3, minCol=2, sheetIndex=1, colNumber='0:3')
            rows = dict([reas for reas in zip(cols[0], cols[1])])

            full_dict[tuName] = f.mapInTop(rows)

    # pprint(dict(sorted(full_dict.items(), key=lambda x: sum(x[1].values()), reverse=True)))
    topValues = topIsklReasons.values()

    for tu, value in full_dict.items():
        value_list.append([tu, *[full_dict[tu][val] for val in topValues]])

    xl.writeResultsInXL(results=value_list, title=['', *list(topValues)],
                        pathFile=dayliProcessFile("все.xlsx"))


def reportByIndicators():
    from private_config import dayliProcessFile
    import xl
    from mongo_database import WorkMongo
    wm = WorkMongo()
    knms = wm.convertForsaving(wm.reportByRiskIndicatorKNM())
    pathFile = dayliProcessFile('выгрузка по индикаторным проверкам.xlsx')
    xl.writeResultsInXL(results=knms[1], title=knms[0], pathFile=pathFile)

    print(pathFile)
    return f'Выгрузка по индикаторам риска готова!'


def countIsklByReasons(pathDir):
    import xl
    from Nat import get_reasons, get_reasons_multy
    import os
    from pathlib import Path

    for file in os.listdir(pathDir):
        print(file)
        pathFile = os.path.join(pathDir, file)
        comments = xl.bringCol(pathFile, minRow=3)
        categories = get_reasons(comments)
        results = [['', 'причины исключений', 'Найдено в КНМ'], *sorted(
            [[n + 1, str(value['explanation']), int(value['count'])] for n, value in enumerate(categories.values())],
            key=lambda x: x[2], reverse=True)]
        # pprint(results)
        xl.writeResultsInXL(results=results, title=Path(pathFile).stem, pathFile=pathFile, sheetIndex=1,
                            sheetTitle='причины исключений')
    return 'Причины исключений собраны!'


def reportByVk():
    import xl
    from mongo_database import WorkMongo
    from private_config import dayliProcessFile
    from datetime import datetime

    now = datetime.now().strftime('%d.%m.%Y %H.%M')

    wm = WorkMongo()
    vkKinds = wm.reportByProductionConsist()
    finalList = []

    allProductionKinds = []
    results = {}
    # results = {'tu': {'prod1': 'count', 'prod2': 'count'}}

    for vkkind in vkKinds:
        tu = vkkind['_id']['tu']
        production = vkkind['_id']['production']
        totalCount = vkkind['totalCount']
        if not production in allProductionKinds:
            allProductionKinds.append(production)
        if tu in results:
            results[tu][production] = totalCount
        else:
            results[tu] = {production: totalCount}

    for n, (tu, productions) in enumerate(results.items()):
        finalList.append([n+1, tu, *[productions[kind] if kind in productions else 0 for kind in allProductionKinds]])

    pathFile = dayliProcessFile(f'выгрузка по составу согласованных объектов выборочного контроля {now}.xlsx')
    xl.writeResultsInXL(results=finalList, title=['', '', *allProductionKinds], pathFile=pathFile)
    print(len(allProductionKinds))
    return 'Выгрузка по составу согласованных объектов выборочного контроля готова!'


if __name__ == '__main__':
    functions = {
        'count_iskl': {'action': countIsklByReasons,
                       'desc': 'Делает отчет, по причинам исключений проверок прокуратурой',
                       'args': ["путь до папки Анализ исключений"]},
        'group_iskl_by_regions': {'action': groupByRegions,
                                  'desc': 'Сортирует нарушения по регионам',
                                  'args': ["путь до файла"]},
        'report_by_reasons_iskl': {'action': reportByIsklReasons,
                                   'desc': 'Сводит в таблицу анализ исключений по регионам',
                                   'args': ["путь до папки Анализ исключений"]},
        'load_knm': {'action': load_knm, 'desc': 'загружает проверки из ЕРКМН',
                     'args': ["Год, за который нужно выгрузить проверки"]},
        'load_pm': {'action': load_pm, 'desc': 'загружает профилактические мероприятия из ЕРКМН',
                    'args': ["Год, за который нужно выгрузить профилактические мероприятия"]},
        'merge_iskl_reason': {'action': mergeIskl,
                              'desc': 'сводит в одну таблицу результаты после анализа причин исключений',
                              'args': [
                                  "путь до папки, где хранятся результаты анализа по причинам исключений (у файлов на листе 'причины исключений' должен быть анализ нарушение - количество)"]},
        'merge_tu': {'action': mergeTu,
                     'desc': 'забирает столбец из файла exel c ТУ и по регурялке проверяет, кто есть в списке и сколько раз, а кого нет',
                     'args': ["путь до файла с ТУ в столбце А", 'номер столбца, который берем']},
        'report_by_diened_objects': {'action': reportByDienedObjects,
                                     'desc': 'отчет по объектам, исключенным в ходе проверки плана прокуратурой',
                                     'args': ['аттрибут, по которому будем считать: "knm" или "objects"']},
        'report_by_accept_objects': {'action': reportByAccepedObjects,
                                     'desc': 'отчет по объектам, исключенным в ходе проверки плана прокуратурой',
                                     'args': ['аттрибут, по которому будем считать: "knm" или "objects"']},
        'report_by_objects': {'action': reportByObjects, 'desc': 'делает отчет о количестве видов деятельности',
                              'args': ["Путь до файла, куда вносятся данные/если такого файла нет-создадим",
                                       """фильтры для поиска, в формате "{'k': 'v'}"""]},
        'report_by_aggreed': {'action': reportByAggreedProcess, 'desc': 'делает отчет о ходе согласования по регионам',
                              'args': ["Путь до файла, куда вносятся данные/если такого файла нет-создадим"]},
        'report_daily_aggreed': {'action': reportDayliAggreedProcess,
                                 'desc': 'делает ежедневный отчет о ходе согласования по регионам в папке C:\\Users\zaitsev_ad\Documents\ЕРКНМ\План 2024\этап планирования\ежедневный мониторинг процесса согласования',
                                 'args': ['аттрибут, по которому будем считать: "knm" или "objects"']},
        'report_by_risks': {'action': reportByRisks, 'desc': 'делает отчет о количестве категорий риска объектов',
                            'args': ["Путь до файла, куда вносятся данные/если такого файла нет-создадим",
                                     """фильтры для поиска, в формате "{'k': 'v'}"""]},
        'report_by_consists_vk': {'action': reportByVk,
                                  'desc': 'делает отчет о составе продукции выборочного контроля',
                                  'args': []},
        'report_by_risksIndicators': {'action': reportByIndicators,
                                      'desc': 'делает выгрузку по проверкам, основаниями для которых стали срабатывания индикаторов риска',
                                      'args': []},
        'report_by_fk': {'action': reportByFreeCommand, 'desc': 'выгружает отчет по введенной команде',
                         'args': ["Путь до файла, куда вносятся данные/если такого файла нет-создадим",
                                  """команда для поиска, в формате "{'k': 'v'}"""]},
        'report_by_iskl': {'action': reportByProsecutorComments,
                           'desc': 'выгружает причины исключений с номерами проверок',
                           'args': ["Путь до файла, куда вносятся данные/если такого файла нет-создадим"]},

        'use_database': {'action': useDatabase, 'desc': 'Дает интерактивный доступ в базу данных doc/knd', 'args': []},

    }

    arg1 = argv[1] if len(argv) >= 2 else None
    if arg1 in functions:
        # print([None if len(argv) < n+1 else 1 for n in range(functions[arg1]['args'])])
        args = [argv[n + 2] if len(argv) > n + 2 else None for n in range(len(functions[arg1]['args']))]
        if args:
            pprint(functions[arg1]['action'](*args))
        else:
            pprint(functions[arg1]['action']())

    if arg1 == 'help' or not arg1:
        print('------------------------------')
        for name, info in functions.items():
            lenName = len(name)
            middleTire = f"{' ' * (lenName + 2)}{'-' * (30 - lenName)}"
            print(f'{name}  |  {info["desc"]}')
            print(middleTire)
            print(f"{' ' * (lenName + 2)}Аргументы:")
            print(middleTire)

            for n, _arg in enumerate(info["args"]):
                print(f"{' ' * (lenName + 5)}{n + 1}.) {_arg}")
                print(middleTire)
            print('------------------------------')
