import json
from datetime import datetime, date
import logging
from sql import Database
import os
from pathlib import Path
import traceback
from direct_pxl import Operation
from multiprocessing import Pool

logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s',
                        filename=f'logging/{date.today().strftime("%d.%m.%Y")}.log', encoding='utf-8',
                        level=logging.INFO)
logger = logging.getLogger(Path(traceback.StackSummary.extract(traceback.walk_stack(None))[0].filename).name)

d = Database()
exception_knm = []

def report():


    logger.info(f"старт программы, читаем файл")
    with open("Plan_knm_full_2023.json", 'r') as file:
        list = json.load(file)
    iskl = 0
    iskl_appealed = 0
    have_remark = 0
    wait_for_control = 0
    ready_to_apply = 0
    in_process = 0
    on_approval = 0
    else_status = []
    logger.info(f"файл прочитан, приступаем к анализу")
    for number, knm in enumerate(list):

        status = knm['status']
        if status == 'Исключена':
            iskl += 1
        elif status == 'Исключение обжаловано':
            iskl_appealed += 1
            wait_for_control += 1
        elif status == "Ожидает проведения":
            wait_for_control += 1
        elif status == "Есть замечания":
            have_remark += 1
            wait_for_control += 1
        elif status == 'Готово к согласованию':
            ready_to_apply += 1
        elif status == 'В процессе заполнения':
            else_status.append(knm)
            in_process += 1
        elif status == 'На согласовании':
            on_approval += 1
            else_status.append(knm)

        else:
            else_status.append(knm)
    logger.info(f"Анализ завершен, вывожу результаты...")

    logger.info(f'Всего внесенных проверок на 2023 г - {len(list)}')
    logger.info(f'проверок в строю, которые будут проводиться в 2023 г - {wait_for_control}')
    logger.info(f'исключено совсем проверок в 2023 г - {iskl}')
    logger.info(f'обжалованные проверок, кроме исключенных совсем в 2023 г (входят в те, что будут проводиться) - {iskl_appealed}')
    logger.info(f'количество проверок в 2023 г, имеющие замечания - (входят в те, что будут проводиться) - {have_remark}')
    logger.info(f'количество проверок в 2023 г, имеющие статус "Готово к согласованию" - {ready_to_apply}')
    logger.info(f'количество проверок в 2023 г, "В процессе заполнения" - {in_process}')
    logger.info(f'количество проверок в 2023 г, "На согласовании" - {on_approval}')


    len_else_status = len(else_status)
    logger.info(f'Имеющие другой статус: {len_else_status}')

    if len_else_status != 0:
        for number, else_knm in enumerate(else_status):
            logger.info(number)
            logger.info(else_knm)
            logger.info('')


def formatter(text: str):
    text = text.replace('"', '')
    return text


def main():

    with open('Exception_knm.json', 'r') as file:
        list_knm = json.load(file)


    multiple_inserts(list_knm)


def database_inserts_conductor(list_knm: list):
    """
    Функция для внесения списка КНМ в базу данных с обработкой ошибок. Пробует просто запустить функцию и ожидает
        успешного выполнения, при неуспешном - пробует второй раз, но высталяет специальный параметр.
        При повторной неудаче умывает руки и выдает ошибку, с которой не удалось справиться.

    @param list_knm: Список КМН, как правило в формате json (список json-ов) для загрузки в базу данных
    @return:
    """
    logger.info('началась запись в базу данных...')


    for knm in list_knm:

        result = insert_in_database(knm)
        if result is False:
            try:
                result = insert_in_database(knm, special=True)
                if result is False:
                    logger.info('Возникла ошибка, с которой не удалось справиться...')
                    exception_knm.append(knm)
            except Exception as ex:
                logger.info(f'Непредвиденная ошибка строка 90: {ex}')
                exception_knm.append(knm)
    if exception_knm:
        with open('Exception_knm.json', 'w') as file:
            json.dump(exception_knm, file)
            result = f'По итогу внесения не было внесено {len(exception_knm)} проверок. Они упакованы в файл Exception_knm.json и их ошибки ожидают решений'
            logger.info(result)
        return result
    logger.info('Все проверки успешно занесены!')


def database_inserts_conductor_for_multiprocessing(knm):

    result = insert_in_database(knm)
    if result is False:
        try:
            result = insert_in_database(knm, special=True)
            if result is False:
                logger.info('Возникла ошибка, с которой не удалось справиться...')
                exception_knm.append(knm)
        except Exception as ex:
            logger.info(f'Непредвиденная ошибка строка 90: {ex}')
            exception_knm.append(knm)


def multiple_inserts(processes: int, knm_list: list):
    logger.info('старт программы')
    pool = Pool(processes)
    pool.map(database_inserts_conductor_for_multiprocessing, knm_list)
    if len(exception_knm) > 0:
        with open('Exception_knm.json', 'w') as file:
            json.dump(exception_knm, file)
            result = f'По итогу внесения не было внесено {len(exception_knm)} проверок. Они упакованы в файл Exception_knm.json и их ошибки ожидают решений'
            logger.info(result)
        return result
    logger.info('Все проверки успешно занесены!')


def insert_in_database(knm: dict, special: bool = False) -> bool:
    """
    Функция непосредственного внесения в базу данных
    @param knm: словарь сведений о кнм, как правило в формате json (список json-ов) для загрузки в базу данных
    @param special: параметр, включаемый для повторного включения, является более медленным, так как при значении  True
        заменяет значения в адресах субъектов
    @return: значение True или False при успешном выполнении инсёрта, и соответственно, ошибке при выполнении инсёрта

    """
    data = str(knm).replace('"', '').replace('None', "'None'").replace('False', "'False'")\
        .replace('True', "'True'").replace("'", '"').replace('\n', '').replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\\p', '').replace("\\", "/")
    try:
        id = int(knm['erpId'])

        kind = knm['kind']
        type = knm['knmType']
        status = knm['status']
        year = int(knm['year'])
        start_date = knm['startDateEn']
        stop_date = knm['stopDateEn']
        if stop_date is None:
            stop_date = '1900-01-01'
        inn = knm['inn']
        ogrn = knm['ogrn']
        try:
            risk = knm['riskCategory'][0]
        except:
            risk = 'NULL'

        try:
            object_kind = knm['objectsKind'][0]
        except:
            object_kind = 'NULL'
        controll_organ = knm['controllingOrganization']
        if special is True:
            addresses = []
            for address in knm['addresses']:
                address = str(address).replace("'", "").replace('"', '').replace("''", "")
                addresses.append(str(address))
            knm['addresses'] = addresses
        Database().create_json_formate_knm_in_raw_knm(id, kind, type, status, year, start_date, stop_date, inn, ogrn, risk, object_kind, controll_organ, data)
        return True

    except Exception as ex:
        logger.error(ex)
        logger.info(data)
        logger.info(knm)
        logger.info('')
        return False


def request_db(targets: list, table: str = 'erknm', **params):
    target_text = ''
    if target_text:
        print('yt gecnjq')
    for target in targets:
        if target_text:
            target_text += f', {target}'
        else:
            target_text += target
    params_text = ''
    for db_column, value in params.items():

        if isinstance(value, type(list)):
            values_text = ''
            for v in value:
                if values_text:
                    values_text += f", '{v}'"
                else:
                    values_text += f"'{v}'"
            if params_text:
                params_text += f" AND {db_column} IN ({values_text})"
            else:
                params_text += f" WHERE {db_column} IN ({values_text})"
        else:
            if params_text:
                params_text += f" AND {db_column}='{value}'"
            else:
                params_text += f" WHERE {db_column}='{value}'"
    if params_text:
        text = f"""SELECT {target_text} FROM {table}{params_text};"""
    else:
        text = f"""SELECT {target_text} FROM {table};"""
    return text

def binary_analys_from_db() -> dict:
    text_request = """SELECT risk FROM erknm WHERE year='2023' AND status IN ('Исключение обжаловано', 'Есть замечания', 'Ожидает проведения');"""
    request = d.take_request_from_database(text_request)


def simple_analys_from_db(targets: list, table: str = 'erknm', **params) -> dict:
    text_request = request_db(targets, table, **params)

    request = d.take_request_from_database(text_request)
    result = {}
    responce = []
    if len(request) > 0:
        for req in request:
            responce.append(req[0])
        result['количество результатов'] = len(responce)
        result['мощность выборки'] = len(set(responce))
        details = {}
        for kind in set(responce):
            details[kind] = responce.count(kind)
        result['details'] = dict(sorted(details.items(), key=lambda item: item[1], reverse=True))
        logger.info(f'{text_request}, {result}')

        for key, values in result.items():
            if key == 'details':
                for obj, value in values.items():
                    print(f'    {obj}: {value}')
            else:
                print(f'{key}: {values}')
        return result

def where_is_error_in_string_by_index(index: int, text: str):
    print(text)


if __name__ == '__main__':
    # knm = {"actCreateDate": "None", "actCreateDateEn": "None", "addresses": ["Кемеровская область - Кузбасс, г. Прокопьевск,  ул. Крупской 1"], "admLevelId": 50001, "appealed": "False", "approveDocOrderDate": "17.05.2022", "approveDocOrderNum": "297-ВН", "approveDocRequestDate": "None", "approveDocRequestNum": "None", "approveDocs": [], "approveRequired": "False", "approved": "None", "approvedErknm": "None", "chlistCount": 0, "chlistFilledCount": 0, "chlistFillingIndicationTypeId": [], "collaboratingOrganizations": [], "collaboratingOrganizationsIds": [], "comment": "None", "controllingOrganization": "Управление Роспотребнадзора по Кемеровской области ", "controllingOrganizationId": 10001011723, "createPlanDate": "None", "createPlanDateLong": "None", "createdByErpDb": "False", "createdById": 196458, "dataNotEqualEGRUL": "False", "dataSetNotInTime": "True", "deleted": "False", "directDurationDays": "None", "disapprove": "False", "district": "Кемеровская область", "districtId": 1035320000000001, "durationDays": "None", "durationHours": 15, "erknmActViolationIds": [3], "erknmResultKindDecisionIds": [], "erpId": "42220041000102077940", "events": [{"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Осмотр"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Получение письменных объяснений"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Истребование документов"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Отбор проб (образцов)"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Инструментальное обследование"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Испытание"}, {"startDate": "18.05.2022", "stopDate": "31.05.2022", "title": "Экспертиза"}], "federalLaw": "248", "federalLawId": 3, "fullFieldViolationKnm": "False", "hasViolations": "False", "id": 12150060, "inn": "4223077332", "inspectorFullName": ["Ворожцова О.С.", "Суханицкая Я.А."], "isFromSmev": "False", "isHasApproveDocs": "False", "isHasCollaboratingOrganization": "False", "isHasRequirements": "True", "isHasViolationTerm": "False", "isPm": "False", "kind": "Выездная проверка", "knmAnnulled": "False", "knmRejected": "False", "knmType": "Внеплановое КНМ", "knmTypeId": 5, "legalBasisDocName": [], "links": [], "mspCategory": ["Микропредприятие"], "noPunishment": "False", "notifyLate": "False", "objectsKind": ["прочие "], "objectsSubKind": ["прочие "], "objectsType": ["Деятельность и действия"], "ogrn": "1154223001338", "oldKnm": "None", "oldPlan": "None", "orderDone": "False", "organizationName": "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ ТРАНСИБ-ФРУКТ", "organizationsInn": ["4223077332"], "organizationsName": ["ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ ТРАНСИБ-ФРУКТ"], "organizationsOgrn": ["1154223001338"], "planId": "None", "prosecutorOrganization": "Прокуратура Кемеровской области", "prosecutorOrganizationId": 2282, "publishedStatus": "PUBLISHED", "reasons": [309], "reasonsList": [{"assignmentDate": "None", "assignmentDateEn": "None", "assignmentNumber": "None", "date": "None", "dateEn": "None", "requirementDetails": "None", "text": "(Постановление 336) Поручение Президента Российской Федерации"}], "recEmptyOrLate": "False", "regDateEgrul": "17.05.2022", "regDateEgrulEn": "2022-05-17", "regLate": "False", "regTypes": ["MSP"], "requirements": 8, "requirementsList": [{"nameNpa": " Федерального закона «О санитарно-эпидемиологическом благополучии населения» ", "numberNpa": "30.03.1999", "title": "Главы I - VIII Федерального закона «О санитарно-эпидемиологическом благополучии населения» от 30.03.1999 № 52-ФЗ"}, {"nameNpa": "Федерального закона от 17.09.1998 № 157-ФЗ «Об иммунопрофилактике инфекционных болезней»", "numberNpa": "17.09.1998", "title": "Главы I, II, IV Федерального закона от 17.09.1998 № 157-ФЗ «Об иммунопрофилактике инфекционных болезней»;"}, {"nameNpa": "Постановления Правительства РФ от 15.07.99 № 825 «Об утверждении перечня работ, выполнение которых связано с высоким риском заболевания инфекционными болезнями и требует обязательного проведения профилактических прививок»", "numberNpa": "15.07.1999", "title": "Постановления Правительства РФ от 15.07.99 № 825 «Об утверждении перечня работ, выполнение которых связано с высоким риском заболевания инфекционными болезнями и требует обязательного проведения профилактических прививок»;"}, {"nameNpa": "СП 2.3.6.3668-20 от 20.11.20г «Санитарно-эпидемиологические требования к условиям деятельности торговых объектов и рынков, реализующих пищевую продукцию»", "numberNpa": "20.11.2020", "title": "Разделы с 2 по 11 СП 2.3.6.3668-20 от 20.11.20г «Санитарно-эпидемиологические требования к условиям деятельности торговых объектов и рынков, реализующих пищевую продукцию»"}, {"nameNpa": "Технический регламент таможенного союза ТР ГС 021/2011 от 01.07.201Зг «О безопасности пищевых продуктов»", "numberNpa": "01.07.2013", "title": "Главы I - II Технический регламент таможенного союза ТР ГС 021/2011 от 01.07.201Зг «О безопасности пищевых продуктов»"}, {"nameNpa": "Технический регламент таможенного союза ТР ТС 022/2011 от 01.07.201Зг «Пищевая продукция в части ее маркировки»", "numberNpa": "01.07.2013", "title": "Статьи 4-5 Технический регламент таможенного союза ТР ТС 022/2011 от 01.07.201Зг «Пищевая продукция в части ее маркировки»"}, {"nameNpa": "Технический регламент таможенного союза ТР ТС 023/2011 от 01.07.2013 «Технический регламент на соковую продукцию из фруктов и овощей»", "numberNpa": "01.07.2013", "title": "Статьи 3-5, ст. 7-8 Технический регламент таможенного союза ТР ТС 023/2011 от 01.07.2013 «Технический регламент на соковую продукцию из фруктов и овощей»"}, {"nameNpa": "Технический регламент таможенного союза ТР СТ 024/2011 от 01.07.201Зг «Технический регламент на масложировую продукцию»", "numberNpa": "01.07.2013", "title": "Главы III - VII Технический регламент таможенного союза ТР СТ 024/2011 от 01.07.201Зг «Технический регламент на масложировую продукцию»"}], "resolved": "False", "resultEmpty": "False", "resultEmptyOrLate": "False", "resultInfoTypeCodes": [], "resultViolationKnm": "False", "riskCategory": [], "riskCategoryAndDangerClass": [], "sezRegistryExists": "False", "signed": "True", "smevInfoType": "None", "smevMessageType": "None", "smevReceivedAt": "None", "smevReceivedAtEn": "None", "smevReceivedAtMonth": "None", "smevReceivedAtYear": "None", "spvRegistryExists": "False", "startDate": "18.05.2022", "startDateEn": "2022-05-18", "status": "Завершено", "statusEgrul": "Найден", "statusId": 7, "stopDate": "31.05.2022", "stopDateEn": "2022-05-31", "subjectTypeId": 0, "supervisionType": "Федеральный государственный санитарно-эпидемиологический контроль (надзор)", "supervisionTypeId": 4, "torRegistryExists": "False", "updatePlanDate": "None", "updatePlanDateLong": "None", "version": "ERKNM", "violationLawsuitTypeCodes": [], "violationTypeCodes": [], "year": 2022}
    # data = str(knm).replace('"', '').replace('None', "'None'").replace('False', "'False'")\
    #         .replace('True', "'True'").replace("'", '"').replace('\\n', '').replace('\\t', '').replace('\\p', '')
    # print(data)
    # for key, value in knm.items():
    #     print(f'{key} - {value}')

    # print(main())
    result = simple_analys_from_db(['status'], year=2023)
    print(result)


