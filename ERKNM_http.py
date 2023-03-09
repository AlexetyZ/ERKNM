import datetime
import json
from main_ERKNM import erknm
from direct_pxl import Operation
import logging
from direct_sql import multiple_inserts, database_inserts_conductor, new_insert_in_database, \
    database_inserts_conductor_for_multiprocessing
from Dates_manager import period_between_month, split_year_for_periods, split_period
from datetime import date
import traceback
from pathlib import Path
from create_doc import make_xl_from_kmns
from sql import Database
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s',
                    filename=f'logging/{date.today().strftime("%d.%m.%Y")}.log', encoding='utf-8',
                    level=logging.INFO)
logger = logging.getLogger(Path(traceback.StackSummary.extract(traceback.walk_stack(None))[0].filename).name)


class Erknm:

    def __init__(self, path_xl_table: str or bool = None):
        """

        :param path_xl_table: файл формата xlsx, содержащий анализируемы сведения.
                Должен содержать шапку в одну строчку, чтобы данные начиналисть со второй строки
                (НЕ Обязательный параметр, так как не все функции нуждаются в инициации экземпляря Operation для exel.)

        """
        if path_xl_table is None:
            self.o = path_xl_table
        else:
            self.o = Operation(path_xl_table)

        self.session = erknm(
            headless=True
        )
        self.session.autorize()
        self.result = []

    def get_knm_by_plan_list(self, count: int = 10000, year: int = 2023):
        result = []
        if self.o is None:
            raise Exception(
                'Эй! Так не пойдет. Эта функция анализирует только таблицу exel,'
                ' так что будь добр, передай в класс этой функции путь к файлу в path_xl_table, '
                'а сейчас:  path_xl_table is None')
        plan_list = self.o.get_column_values('A')

        for plan in plan_list:
            print(plan)
            print(f'сумма КНМ - {len(result)}')
            try:
                response = self.session.get_knm_list(
                    date_start=f'{year}-01-01',
                    date_end=f'{year}-12-31',
                    count=count,
                    year=year,
                    plan_number=plan
                )
            except Exception as ex:
                print(ex)
                with open(f'Part_plan_last_{plan}.json', 'wb') as file:
                    json.dump(result, file)
                break
            if response['totalCount'] > count:
                for month in range(1, 13):
                    between = period_between_month(year, month)
                    print(between)

                    subresponse = self.session.get_knm_list(
                        date_start=between['start'],
                        date_end=between['end'],
                        count=3000,
                        year=year,
                        plan_number=plan
                    )
                    for knm_in_month in subresponse['list']:
                        result.append(knm_in_month)
                        # try:
                        #     create_knm_in_knms(knm_in_month)
                        # except Exception as ex:
                        #     print(knm_in_month)
                        #     print(ex)

            else:
                for knm in response['list']:
                    result.append(knm)
                    # try:
                    #     create_knm_in_knms(knm)
                    # except Exception as ex:
                    #     print(knm)
                    #     print(ex)
        logger.info('Сбор результатов по планам завершен')

        try:
            make_xl_from_kmns(result)
        except:

            with open(f'Plan_knm_full_{str(year)}.json', 'w') as file:
                json.dump(result, file)

    def get_all_knm_for_a_year(self, count: int = 8000, year: int = 2023):
        year_periods = split_year_for_periods(year, 50)
        result = []

        for between in year_periods:

            print(f'{between} {len(result)}')

            response = self.session.get_knm_list(
                date_start=between['start'],
                date_end=between['end'],
                count=count,
                year=year,

            )
            # print(response)

            # break

            try:
                resp_count = response['totalCount']
            except Exception as ex:

                print(ex)
                break
            if resp_count > count:
                print(f"Запрос длинее {count} - {response['totalCount']}")

                cycle = round(resp_count / count)
                if cycle < 2:
                    cycle = 2
                while True:
                    subresponses_result = []
                    periods = split_period(between['start'], between['end'], parts=cycle)
                    for period in periods:
                        subresponse = self.session.get_knm_list(
                            date_start=period['start'],
                            date_end=period['end'],
                            count=count,
                            year=year,
                        )
                        try:
                            subresp_count = subresponse['totalCount']
                        except Exception as ex:
                            print(subresponse)
                            print(ex)
                            break
                        if subresp_count > count:
                            print(f"Подзапрос длинее {count} - {subresponse['totalCount']}")
                            cycle += 1
                            continue
                        for knm_month_parts in subresponse['list']:
                            subresponses_result.append(knm_month_parts)
                    for subresp in subresponses_result:
                        result.append(subresp)
                    break

            else:
                # print('запрос короче')
                print(len(response['list']))
                for knm_in_month in response['list']:
                    result.append(knm_in_month)

        # logger.info('сбор данных завершен, записываем для сохранения в json')
        # with open(f'Plan_knm_full_{str(year)}.json', 'w') as file:
        #     json.dump(result, file)

        logger.info('Запись в json завершена, заносим в базу данных')

        multiple_inserts(8, result)
        Database().conn.commit()
        # database_inserts_conductor(result)

        # try:
        #     make_xl_from_kmns(result)
        # except:
        #
        #     with open(f'Plan_knm_full_{str(year)}.json', 'w') as file:
        #         json.dump(result, file)

    def get_all_pm_for_a_year(self, count: int = 8000, year: int = 2023):
        year_periods = split_year_for_periods(year, 50)
        result = []

        for between in year_periods:

            print(f'{between} {len(result)}')

            response = self.session.get_pm_list(
                date_start=between['start'],
                date_end=between['end'],
                count=count,
                year=year,

            )
            # print(response)

            # break

            try:
                resp_count = response['totalCount']
            except Exception as ex:

                print(ex)
                break
            if resp_count > count:
                print(f"Запрос длинее {count} - {response['totalCount']}")

                cycle = round(resp_count / count)
                if cycle < 2:
                    cycle = 2
                while True:
                    subresponses_result = []
                    periods = split_period(between['start'], between['end'], parts=cycle)
                    for period in periods:
                        subresponse = self.session.get_pm_list(
                            date_start=period['start'],
                            date_end=period['end'],
                            count=count,
                            year=year,
                        )
                        try:
                            subresp_count = subresponse['totalCount']
                        except Exception as ex:
                            print(subresponse)
                            print(ex)
                            break
                        if subresp_count > count:
                            print(f"Подзапрос длинее {count} - {subresponse['totalCount']}")
                            cycle += 1
                            continue
                        for knm_month_parts in subresponse['list']:
                            subresponses_result.append(knm_month_parts)
                    for subresp in subresponses_result:
                        result.append(subresp)
                    break

            else:
                # print('запрос короче')
                print(len(response['list']))
                for knm_in_month in response['list']:
                    result.append(knm_in_month)

        logger.info('сбор данных завершен, записываем для сохранения в json')
        with open(f'pm_{str(year)}.json', 'w') as file:
            json.dump(result, file)

        logger.info('Запись в json завершена, заносим в базу данных')
        print(f'start {datetime.datetime.now()}')
        d = Database()

        # with ThreadPoolExecutor() as executor:
        #
        #     executor.map(stabilise_pm, result)

        for res in result:
            try:
                self.stabilise_pm(res)
                # print(f'проверка {res["id"]}')

            except Exception as ex:
                logger.exception('Не получилось ввести проф. мероприятие на основании элемента выгрузки')
                logger.info(res)
                # print(ex)
                # print(res)
        print(f'stabilize_ending {datetime.datetime.now()}')

        # multiple_inserts(4, result)
        # print(f'end {datetime.datetime.now()}')
        # database_inserts_conductor(result)

        # try:
        #     make_xl_from_kmns(result)
        # except:
        #
        #     with open(f'Plan_knm_full_{str(year)}.json', 'w') as file:
        #         json.dump(result, file)

    def stabilise_pm(self, res):
        try:
            if not Database().is_inspection_exists(res['erpId']):
                true_id = res['id']
                obj_address = res['addresses']
                objects_kinds = []
                objects_risks = []
                for n, ob_ad in enumerate(obj_address):
                    ob_kind = self.session.get_pm_object_kind(true_id, n)
                    # print(f'запрос прошел: {ob_kind}')
                    objects_kinds.append(ob_kind)
                    objects_risks.append('-')
                res['objectsKind'] = objects_kinds
                res['riskCategory'] = objects_risks
            try:
                Database().ultra_create_handler(res)
            except:
                new_insert_in_database(res)
        except:
            logger.exception('Не удалось включить элемент выгрузки в базу данных')
            logger.info(res)

    def get_knms_by_numbers(self):
        if self.o is None:
            raise Exception(
                'Эй! Так не пойдет. Эта функция анализирует только таблицу exel,'
                ' так что будь добр, передай в класс этой функции путь к файлу в path_xl_table, '
                'а сейчас:  path_xl_table is None')

        values = self.o.get_list_from_sh_column(
            'D',
            start_from_row=2
        )
        for n, value in enumerate(values):
            try:
                req = self.session.get_knm_by_number(value[0])['list'][0]
                # print(req)
                status = req['status']
                print(status)
                self.o.change_value_in_cell(n + 2, 9, status, saving=False)
            except Exception as ex:
                print(ex)
                try:
                    print(self.session.get_knm_by_number(value[0])['list'][0])
                except:
                    pass

        self.o.save_document()


if __name__ == '__main__':
    year = int(input('Enter the year, to reload datas knm (format: "YYYY")'))
    Erknm().get_all_knm_for_a_year(year=year)
    # Erknm("C:\\Users\zaitsev_ad\Documents\ЕРКНМ\Список_утвержденных_планов_2023.xlsx").get_knm_by_plan_list()
