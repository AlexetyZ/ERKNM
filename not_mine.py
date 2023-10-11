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


def merge_both(string1: str, string2: str, lastetski: bool = False):
    string1 = standartingString(string1)
    string2 = standartingString(string2)
    fuzz_ratio = fuzz.token_sort_ratio(string1, string2)
    if fuzz.token_sort_ratio(string1, string2) >= 90:
        return True
    if lastetski:
        # print(f'{string1}  not equal  {string2}')
        return False
    if 70 <= fuzz_ratio <= 90:
        return merge_both(string1[:7], string2[:7], lastetski=True)
    return False

def in_one_of(string, _list):

    for elem in _list:
        if merge_both(string, elem):
            return elem
    return False


def get_weight(string1: str, string2: str):
    string1 = standartingString(string1)
    string2 = standartingString(string2)
    return fuzz.token_sort_ratio(string1, string2)


def merge_both_addresses(string1: str, string2: str, lastetski: bool = False) -> bool:
    string1 = standartingString(string1)
    string2 = standartingString(string2)

    return False


if __name__ == "__main__":
    # text1 = 'rfrf'
    text1 = 'место проведение мероприятие не соответствовать адрес объект контроль'
    text2 = 'место проведение мероприятие не соответствовать адрес объект'
    # print(get_weight(text1, text2))
    text_list = ['место проведение мероприятие не соответствовать адрес объект контроль']
    # Архангельская обл, г Вельск, ул Дзержинского, д 42
    print(in_one_of(text1, text_list))
