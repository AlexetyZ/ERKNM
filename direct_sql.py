from sql import Database
from multiprocessing import Pool
import logging
from pathlib import Path
import traceback
from datetime import date
import json
from knm_status_kinds import completed


logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s',
                        filename=f'logging/reports/{date.today().strftime("%d.%m.%Y")}.log', encoding='utf-8',
                        level=logging.INFO)
logger = logging.getLogger(Path(traceback.StackSummary.extract(traceback.walk_stack(None))[0].filename).name)

d = Database()
exception_knm = []

# ter_upr_name = knm['controllingOrganization']
# controllingOrganizationID = knm['controllingOrganizationID']
# ter_upr_name_id = d.insert_terr_upr_with_return_id(name=ter_upr_name, controllingOrganizationID=controllingOrganizationID)


def formattig_str(text):
    text = str(text).replace("'", "").replace('"', '').replace("   ", " ").replace("  ", " ").replace('/"', ' ')
    return text


def create_knm_in_knms(knm):

    # for number, (key, value) in enumerate(knm.items()):
    #     print(key, value)
    terr_upr_id = d.create_terr_upr_returned_id(knm['controllingOrganization'], knm['controllingOrganizationId'], knm['district'])
    try:
        last_inspect_date = knm['reasonsList']['o']['date']
    except:
        last_inspect_date = '1990-01-01'

    desicion_date = knm['approveDocOrderDate']
    if desicion_date is None:
        desicion_date = '1900-01-01'

    date_end = knm['stopDateEn']
    if date_end is None:
        date_end = '1900-01-01'


    comment = str(knm['comment'])
    comment = formattig_str(comment)
    print(comment)

    insp_id = d.create_inspection_knd_returned_id(plan_id=knm['planId'],
                                                  knm_id=knm['id'],
                                                  kind=knm['kind'],
                                                  profilactic=knm['isPm'],
                                                  deleted=knm['deleted'],
                                                  date_start=knm['startDateEn'],
                                                  date_end=date_end,
                                                  desicion_number=knm['approveDocOrderNum'],
                                                  desicion_date=desicion_date,
                                                  last_inspection_date_end=last_inspect_date,
                                                  mspCategory=formattig_str(knm['mspCategory'][0]),
                                                  number=knm['erpId'],
                                                  status=formattig_str(knm['status']),
                                                  comment=comment,
                                                  year=knm['year'],
                                                  terr_upr_id=terr_upr_id)
    address = formattig_str(knm['addresses'][-1])
    # print(address)
    subject_id = d.create_subject_with_returned_id(

        name=formattig_str(knm['organizationName']),
        address=address,
        inn=knm['inn'],
        ogrn=knm['ogrn']
    )
    for address, risk in zip(knm['addresses'], knm['riskCategory']):
        address = formattig_str(address)
        object_id = d.create_object_with_returned_id(
            subject=subject_id,
            kind=formattig_str(knm['objectsKind'][0]),
            address=formattig_str(address),
            risk=formattig_str(risk)
        )
        d.insert_m_to_m_object_inspection(inspection_id=insp_id, object_id=object_id)


def database_inserts_conductor(list_knm: list):
    """
    Функция для внесения списка КНМ в базу данных с обработкой ошибок. Пробует просто запустить функцию и ожидает
        успешного выполнения, при неуспешном - пробует второй раз, но высталяет специальный параметр.
        При повторной неудаче умывает руки и выдает ошибку, с которой не удалось справиться.

    @param list_knm: Список КМН, как правило в формате json (список json-ов) для загрузки в базу данных
    @return:
    """
    logger.info('началась запись в базу данных...')
    print("началась запись")


    for knm in list_knm:


        result = new_insert_in_database(knm)
        if result is False:
            try:
                # result = insert_in_database(knm, special=True)
                result = new_insert_in_database(knm)
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

    result = new_insert_in_database(knm)
    if result is False:
        try:
            result = new_insert_in_database(knm)
            if result is False:
                logger.info('Возникла ошибка, с которой не удалось справиться...')
                logger.info('')
                exception_knm.append(knm)
        except Exception as ex:
            logger.info(f'Непредвиденная ошибка строка 90: {ex}')
            exception_knm.append(knm)


def multiple_inserts(processes: int, knm_list: list):
    logger.info('старт программы')
    pool = Pool(processes)
    pool.map(database_inserts_conductor_for_multiprocessing, knm_list)
    if exception_knm:
        with open('Exception_knm.json', 'w') as file:
            json.dump(exception_knm, file)
            result = f'По итогу внесения не было внесено {len(exception_knm)} проверок. Они упакованы в файл Exception_knm.json и их ошибки ожидают решений'
            logger.info(result)
        return result
    logger.info('Все проверки успешно занесены!')


def insert_in_database(result: dict, special: bool = False) -> bool:
    def insert_in_database(knm: dict, special: bool = False) -> bool:
        """
        Функция непосредственного внесения в базу данных. Как правило должна управляться кондуктором
        или функцией мультипроцесса, так как не имеет обработчика исключений, в качестве исключения лишь делает запись в
        логгере и то тольно при специальном параметре.
        @param knm: словарь сведений о кнм, как правило в формате json (список json-ов) для загрузки в базу данных
        @param special: параметр, включаемый для повторного введения значений, является более медленным, так как при значении  True
            заменяет значения в адресах субъектов. ПРИ ВЫКЛЮЧЕННОМ ЗНАЧЕНИИ (ПО ДЕФОЛТУ) ВОЗВРАЩАЕТ ТОЛЬКО bool, без записи в логгере
        @return: значение True или False при успешном выполнении инсёрта, и соответственно, ошибке при выполнении инсёрта
        """
        if special is True:
            addresses = []
            for address in knm['addresses']:
                address = formattig_str(address)
                addresses.append(str(address))
            knm['addresses'] = addresses

            organizationName = knm['organizationName']
            knm['organizationName'] = formattig_str(organizationName)

            organizations = []
            for organization in knm['organizationsName']:
                organization = formattig_str(organization)
                organizations.append(str(organization))
            knm['organizationsName'] = organizations

            requirementsList = []
            for requirement in knm['requirementsList']:
                requirement['nameNpa'] = formattig_str(requirement['nameNpa'])
                requirement['numberNpa'] = formattig_str(requirement['numberNpa'])
                requirement['title'] = formattig_str(requirement['title'])
                requirementsList.append(requirement)

            knm['requirementsList'] = requirementsList

        data = str(knm).replace('"', '').replace('None', "'None'").replace('False', "'False'") \
            .replace('True', "'True'").replace("', ',", "', '").replace("'", '"').replace('""', '"').replace('": ", "',
                                                                                                             '": "", "').replace(
            '\n', '').replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\\p', '').replace("\\", "/")
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

            Database().create_json_formate_knm_in_raw_knm(id, kind, type, status, year, start_date, stop_date, inn,
                                                          ogrn, risk, object_kind, controll_organ, data)

            return True

        except Exception as ex:
            if special:
                logger.error(ex)
                logger.info(data)
                logger.info(knm)
                logger.warning('Проведена повторная попытка внесения с параметром special, результат неудачный.')
            return False


def new_insert_in_database(result: dict, special: bool = False):
    print("записываю")
    try:
        if special:
            print("теперь со специальным параметром")
            if special is True:
                addresses = []
                for address in result['addresses']:
                    address = formattig_str(address)
                    addresses.append(str(address))
                result['addresses'] = addresses

                organizationName = result['organizationName']
                result['organizationName'] = formattig_str(organizationName)

                organizations = []
                for organization in result['organizationsName']:
                    organization = formattig_str(organization)
                    organizations.append(str(organization))
                result['organizationsName'] = organizations

                requirementsList = []
                for requirement in result['requirementsList']:
                    requirement['nameNpa'] = formattig_str(requirement['nameNpa'])
                    requirement['numberNpa'] = formattig_str(requirement['numberNpa'])
                    requirement['title'] = formattig_str(requirement['title'])
                    requirementsList.append(requirement)

                result['requirementsList'] = requirementsList
        Database().ultra_create_handler(result)

    except Exception as ex:
        print(ex)

        logger.error(ex)
        logger.info(result)
        logger.warning('Проведена повторная попытка внесения с параметром special, результат неудачный.')
        return False


def create_tables_for_knms(knm):
    code = ''
    for key, value in knm.items():


        if isinstance(value, list):
            types = 'TEXT'
            code += f'{key} {types}, '
            continue

        elif value is None or isinstance(value, str):
            types = 'VARCHAR(255)'
            code += f'{key} {types}, '
            continue



        elif value is True or value is False:
            print('bool')
            types = 'BOOL'
            code += f'{key} {types}, '
            continue

        elif isinstance(value, int):

            types = 'INT'
            code += f'{key} {types}, '
            continue

    print(str(code).strip())


def insert_exceptions():
    with open('Exception_knm.json', 'r') as file:
        list_knm = json.load(file)
    print('файл открыт')
    database_inserts_conductor(list_knm)


def insert_from_json_with_multiple():
    with open('Plan_knm_full_2022.json', 'r') as file:
        list_knm = json.load(file)
    multiple_inserts(4, list_knm)


if __name__ == '__main__':
    # pass
    insert_exceptions()

