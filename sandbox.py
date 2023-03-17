import traceback
from main_ERKNM import erknm
import operator
from direct_pxl import Operation
import os
import re
from pathlib import Path
from difflib import SequenceMatcher


def main():
    e = erknm()
    e.get_okved()


def main2():
    list_1 = [{'terr_upr': '1', 'number': '123456'}, {'terr_upr': '2', 'number': '1234567'}, {'terr_upr': '1', 'number': '12345678'}, {'terr_upr': '2', 'number': '123456789'}]
    sort_list = sorted(list_1, key=lambda x: x['terr_upr'])
    print(sort_list)

def get_indicator(o, column: int):
    """
    Используется для формулировки показателя методом поиска в шапке исследуемой таблицей (где и указаны некие показатели), с учетом сложных связей таблицы и объединенных ячеек
    обусловлен поиск показателя в шапке таблицы в интервале от 3 до 7 строки

    @param o: передается инициализированный класс Operation  с подготовленными параметрами
    @param column: передается номер столбца, в котором указывается показатель
    @return:
    """
    indicator = ''
    searching_col = column
    searching_row = 3
    border = 0
    while True:
        if searching_row == 7:
            break
        # print(f'{searching_row=} {searching_col=}')
        text = o.get_cell_value(searching_row, column=searching_col)
        if text:

            border = searching_col
            # print(f'{border=}')
            indicator += f'{text} '
            # print(indicator)
            if searching_row < 6:
                searching_col = column
                searching_row += 1
                continue
            else:
                break
        else:
            if searching_col < 1:
                break

            if searching_col > border:
                searching_col -= 1
                continue
            if searching_col == border:
                searching_col = column
                searching_row += 1
                continue




    # print(f'{border=}')
    indicator = str(indicator).replace('-', '').strip()
    return indicator


def main3():
    file_22_path = "S:\\_Public_\! СТАТИСТИКА\Статистика-2022\\3 КВАРТАЛ\\1-22\Свод РФ_1-22_3 кв. 2022.xlsx" #80

    file_21_path = "S:\\_Public_\! СТАТИСТИКА\Статистика-2021\\2021 годовые\СВОДЫ РФ_2021\Форма № 1-21_2021\Свод РФ_1-21_2021 исправленный 07.06.2022.xlsx" #80

    file_20_path = "S:\\_Public_\! СТАТИСТИКА\Статистика-2020\Годовые\Форма № 1-20\Свод РФ _1-20_2020.xlsx"  # 61

    file_19_path = "S:\\_Public_\! СТАТИСТИКА\Статистика-2019\Сводные отчеты 2019 окончательные\Форма № 1-19\ф 1-19_свод РФ_17.03.2020.xlsx"  # 61

    file_18_path = "S:\\_Public_\! СТАТИСТИКА\Статистика-2018\ИТОГОВЫЕ ФОРМЫ за 2018 г\Форма № 1-18_07.02.2019\Свод РФ_предварительный_07.02.2019_.xlsx"  # 61


    o = Operation(
        wb_path=file_18_path,
        sh_name='Таблица_2_0'
    )

    last_col = o.detect_last_column()



    activity_type = o.get_cell_value(61, 1)
    print(activity_type)
    for col in range(4, last_col-1):
        indicator = get_indicator(o, col)

        if re.findall(r'число.*наруш', str(indicator).lower()):
            value = o.get_cell_value(80, col)
            print(f'    {indicator} - {value}')


def main4():
    path = 'C:\\Users\zaitsev_ad\PycharmProjects\ERKNM\logging\\20.01.2023.log'
    parts = Path(path).parts
    print(f'{parts[-2]}\{parts[-1]}')


def main5():
    str1 = '298300, Республика Крым, г. Керчь, Сенная площадь, 16'
    str2 = '298405, Республика Крым, г Керчь, ул Сенная, 17'
    difference = SequenceMatcher(None, str1, str2).ratio()
    print(difference)


def main6():
    print(Path(traceback.StackSummary.extract(traceback.walk_stack(None))[0].filename).name)


def main7():
    try_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    print(try_list[3:11])

def main8():
    pass


if __name__ == '__main__':
    main7()
