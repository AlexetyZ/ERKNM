import json
import os.path


from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from tqdm import tqdm

import logging
import datetime




def standartingString(string: str):
    try:
        string = re.sub(r'\d{5,}', '', string)
        return string.strip().lower().replace('\t', '').replace(' д ', '').replace(' д. ', '').replace(' город ', 'г').replace(' район ', '').replace(' р-н. ', '').replace(' р-н ', '').replace(" ", "").replace('"', '').replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace("'", '')
    except:
        raise Exception(string)


def merge_both(string1: str, string2: str, lastetski: bool = False, limitWeight: int = 60, returnWeight: bool = False):
    string1 = standartingString(string1)
    string2 = standartingString(string2)
    fuzz_ratio = fuzz.token_sort_ratio(string1, string2)
    weight = fuzz.token_sort_ratio(string1, string2)
    if weight >= limitWeight:
        return weight if returnWeight else True
    if lastetski:
        # print(f'{string1}  not equal  {string2}')
        return False
    if 70 <= fuzz_ratio <= 90:
        return merge_both(string1[:7], string2[:7], lastetski=True)
    return False


def in_one_of(string, _list, limitWeight: int = 60):
    """Возвращает значение из списка, соответствующее строке на 60 % и более"""



    if not _list:
        return False
    matched = {}
    for elem in _list:
        weight = merge_both(string, elem, limitWeight=limitWeight, returnWeight=True)
        if weight:

            matched[elem] = weight


    if not matched:
        return False
    else:
        return max(matched, key=matched.get)



def get_weight(string1: str, string2: str):
    string1 = standartingString(string1)
    string2 = standartingString(string2)
    return fuzz.token_sort_ratio(string1, string2)


def merge_both_addresses(string1: str, string2: str, lastetski: bool = False) -> bool:
    string1 = standartingString(string1)
    string2 = standartingString(string2)

    return False


if __name__ == "__main__":
    from Nat import KnowHow
    # text1 = 'rfrf'
    text1 = 'Несоблюдение установленного ст 72 Закона № 248 - ФЗ срока проведения документарной проверки'
    text2 = [
        'раздел требование включить подраздел объем неверно отразить единица '
        'свидетельствовать расширение предмет проверка',
        'перечень документ указать излишний док-т др',
        'ЕРВК не содержит сведений об объекте контроля',
        'сстрока место нахождение осуществление деятельность лицо адрес не заполнить '
        'сведение',
        'кнм исключить план сила пункт 113 постановление правительство рф от 10 '
        '03.2022 n 336',
        'нарушение срок проведение проверка взаимодействи',
        'ошибка заполнение место проведение мероприятие',
        'некорректный внесение нпа число наименование дата',
        'дублирование объект контроль',
        'неверно выбрать основание проведение',
        'действие подлежать осуществление в рамка менее обременительный для '
        'контролировать лицо иной контрольный надзорный мероприятие , предусмотреть п '
        '70 положение № 1100 , что не отвечать требование п . 2 ч . 3 ст 73 '
        'федеральный закон № 248-фз',
        'сила постановление ввести мораторий проверка субъект бизнес малый',
        'категория риск не подтвердить отнести'
    ]
    print(list(KnowHow(text1).lemmatize())[0])
    print(in_one_of(list(KnowHow(text1).lemmatize())[0], text2, limitWeight=10))
    # text_list = ['место проведение мероприятие не соответствовать адрес объект контроль']
    # Архангельская обл, г Вельск, ул Дзержинского, д 42
    # print(in_one_of(text1, text_list))
