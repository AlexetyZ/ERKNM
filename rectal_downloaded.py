import json
import os
import pprint
from tqdm import tqdm
import openpyxl


mainList = []




def addFileToMainList(path):
    with open(path, 'r', encoding='utf-8') as file:
        mainList.extend(json.load(file))


def loadAllJsonsIndir(dir_path):
    for file in os.listdir(dir_path):
        addFileToMainList(os.path.join(dir_path, file))


def analizeProcecutorApprovmentByRegions(path):
    """анализирует проверки и дает информацию по регионам, сколько подано на согласование прокуратуры, исколько из них отказано - АНАЛИЗИРОВАТЬ ТОЛЬКО ВНЕПЛАНОВЫЕ ПРОВЕРКИ, ТРЕБУЮЩИЕ СОГЛАСОВАНИЯ (APPROVED TRUE OR FALSE, NOT NULL)"""
    result = {}
    total_counter = 0
    denied_counter = 0

    for knm in tqdm(mainList, desc='Обработка проверок'):
        org = knm['controllingOrganization']
        if org not in result:
            result[org] = {'sended': 0, 'denied': 0}

        result[org]['sended'] += 1
        result[org]['denied'] += 1 if knm['approved'] is False else 0

    print(f'total_counter: {total_counter}, denied_counter: {denied_counter}')
    wb = openpyxl.Workbook()
    sh = wb.worksheets[0]
    sh.append(('ТУ', 'отправлено на согласование в прокуратуру', 'отказано прокуратурой'))
    for region, info in result.items():

        sh.append((region, info['sended'], info['denied']))
    wb.save(os.path.join(path, "Анализ направленных и согласованных прокуратурой проверок по регионам.xlsx"))



if __name__ == '__main__':
    path = "C:\\Users\zaitsev_ad\Documents\ЕРКНМ\выгрузка согласованные и несогласованные прокуратурой внеплан 2023 на август"
    loadAllJsonsIndir(path)
    analizeProcecutorApprovmentByRegions(path)

