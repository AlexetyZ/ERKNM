from tqdm import tqdm

import datetime
import re
from typing import Dict
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import os
from Dictionary import riskCategoryById
from mongo_rhs import WorkMongo



def formater(text: str):
    text = text.replace('"', ' ').replace("'", "").replace("  ", " ").replace("«", "").replace("»", "").replace('\\', '').replace("\n", " ").replace('/', '').strip()
    return text


def formatter_for_addresses(text: str):

    text = text.replace('"', ' ').replace("'", "").replace("  ", " ").replace("«", "").replace("»", "").replace("\n", " ").strip()
    return text


class Eias:
    def __init__(self):
        self.session = requests.Session()
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.999 (corp) Yowser/2.5 Safari/537.36'
        self.authorize()

    def authorize(self):
        url = 'https://eias.rospotrebnadzor.ru/auth/master/oauth/auth'
        self.cookies = {
            'last_login_u_id': '957306',
            '_ym_uid': '1705405856636899637',
            '_ym_d': '1705405856',
            '_clck': 'gd5iim%7C2%7Cfig%7C0%7C1476',
            '_ga_GYKLT1ZMTB': 'GS1.1.1705405928.1.1.1705405936.0.0.0',
            'xcuser_sess': '7198b486-bac1-11ee-ab55-003048bddde7',
            'xcuser_action': '3de425d8-bac5-11ee-ab55-003048bddde7',
            'metabase.DEVICE': '9d4841f3-ef7f-4c99-bba5-b67a0e827610',
            '_ga': 'GA1.2.1617587542.1705405929',
            '_gid': 'GA1.2.364273186.1707148477',
            'employee_guid': '95c50716%2Da840%2D11ed%2D8444%2D005056958e11',
            'name': '%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B9',
            'patronymic': '%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B5%D0%B2%D0%B8%D1%87',
            'regions': '1%7C4%7C22%7C28%7C30%7C29%7C99%7C2%7C31%7C32%7C3%7C33%7C34%7C35%7C36%7C5%7C93%7C79%7C90%7C75%7C37%7C6%7C38%7C7%7C39%7C8%7C40%7C41%7C9%7C10%7C42%7C43%7C11%7C44%7C23%7C24%7C91%7C45%7C46%7C47%7C48%7C94%7C49%7C12%7C13%7C77%7C50%7C51%7C52%7C83%7C53%7C54%7C55%7C56%7C57%7C58%7C59%7C25%7C60%7C61%7C62%7C63%7C78%7C64%7C65%7C14%7C66%7C92%7C15%7C26%7C67%7C68%7C69%7C16%7C70%7C71%7C17%7C18%7C72%7C73%7C27%7C19%7C86%7C95%7C74%7C20%7C21%7C87%7C89%7C76%7C100%7C101%7C102%7C103%7C104%7C105%7C106%7C107',
            'surname': '%D0%97%D0%B0%D0%B9%D1%86%D0%B5%D0%B2',
            'user_id': 'c24e3f41%2D7f46%2D4e3e%2D8ade%2Dd1c8de06eecf',
            'roles': 'gov%2Dservices%5Fui%2Cgu%5Fspecialist%5Felmk%2Cknd%5Ffederal%5Fspecialist%2Crhs%5Ffederal%5Fspecialist%2Crhs%5Fui%2Crole%5Fuser%5Ffcgie',
            'employee': '95c50716%2Da840%2D11ed%2D8444%2D005056958e11',
            'position': '%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D0%BD%D0%B8%D0%BA',
            'email': 'zaitsev%5Fad%40rospotrebnadzor%2Eru',
            'SESSION_master': 'IjM2YWNiN2UwLWE4OTQtNDViZS1hOTg4LTEwMmNiYWNkZTcyZSI%3D%2E75z7JLrNkt48b3nEtM4oVjXtOnDwBqKgO6SUSvCux6w%3D',
        }
        data = {
            'redirect_uri': 'http://eias.rospotrebnadzor.ru/',
            'client_id': '742d2887-9769-4468-98ee-3610b01e75af',
            'response_type': 'gateway',
            'state': '',
            'flow_type': 'browser_flow',
            'scope': '',
            'username': 'aldzaytsev',
            'password': 'U4f7lhXi0g3B',
        }
        self.headers = {
            'sec-ch-ua': '"Chromium";v="118", "YaBrowser";v="23", "Not=A?Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://eias.rospotrebnadzor.ru/rhs/register-industrial-objects',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.807 YaBrowser/23.11.1.807 (corp) Yowser/2.5 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        params = {
            'redirect_uri': 'http://eias.rospotrebnadzor.ru/',
            'client_id': '742d2887-9769-4468-98ee-3610b01e75af',
            'response_type': 'gateway',
            'flow_type': 'browser_flow',
        }

        response = requests.post(
            'https://eias.rospotrebnadzor.ru/auth/master/oauth/auth',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
            # verify=False
        )
        # print(response.text)

    def getSubjectByOGRN(self, ogrn):
        url = f'https://eias.rospotrebnadzor.ru/api/households/employee/subject_entities_attributes/v2?limit=50&sort=created_at&region=in::1|4|22|28|29|30|2|31|32|3|33|34|35|36|5|93|79|75|90|37|6|38|7|39|8|40|41|9|10|42|43|11|44|23|24|91|45|46|47|48|94|49|12|13|77|50|51|83|52|53|54|55|56|57|58|59|25|60|61|62|63|78|64|14|65|66|92|15|67|26|68|16|69|70|71|17|72|18|73|27|19|86|95|74|20|21|87|89|76&ogrn={ogrn}&is_liquidated=false&supervised_status=in::supervised'

        request = self.session.get(url, headers={'User-Agent': self.userAgent}, cookies=self.cookies)
        return request.json()['subjects'][0]

    def loadAllObjects(self, limit=2000):
        firstUrl = f'https://eias.rospotrebnadzor.ru/api/households/industrial_objects/v2?limit={limit}&sort=created_at&region=in::1|4|22|28|29|30|2|31|32|3|33|34|35|36|5|93|79|75|90|37|6|38|7|39|8|40|41|9|10|42|43|11|44|23|24|91|45|46|47|48|94|49|12|13|77|50|51|83|52|53|54|55|56|57|58|59|25|60|61|62|63|78|64|14|65|66|92|15|67|26|68|16|69|70|71|17|72|18|73|27|19|86|95|74|20|21|87|89|76&has_liquidated_date=false&supervised_status=in::supervised'
        wm = WorkMongo(collection_name='rhs')
        print(f'started {datetime.datetime.now()}')
        if os.path.exists('cursor.txt'):
            with open('cursor.txt', 'r', encoding='UTF-8') as file:
                cursor = file.read()
        else:
            firstRequest = self.session.get(
                firstUrl,
                headers=self.headers,
                cookies=self.cookies,
            )
            # print(firstRequest.json())
            try:
                cursor = firstRequest.json()['cursor']
            except:
                raise Exception(firstRequest.json())
            firstObjects = firstRequest.json()['industrial_objects']
            print(f'get responce {datetime.datetime.now()}')
        # guids = [obj['guid'] for obj in firstRequest.json()['industrial_objects']]
            wm.insert_many(firstObjects)
        len_obj = limit
        n = 0
        while True:
            url = f'https://eias.rospotrebnadzor.ru/api/households/industrial_objects/v2?cursor_down={cursor}'
            request = self.session.get(url, headers=self.headers, cookies=self.cookies, timeout=30)
            try:
                cursor = request.json()['cursor']
            except:
                with open('cursor.txt', 'w', encoding='UTF-8') as file:
                    file.write(cursor)
                raise Exception(request.json())
            objects = request.json()['industrial_objects']
            wm.insert_many(objects)
            n += 1
            print(f'{n} - {datetime.datetime.now()}')
            if len_obj > len(objects):
                os.remove('cursor.txt')
                break

    def getMassObjectsByGuids(self, guids_list):
        for guid in tqdm(guids_list, desc='обработка гуидов и загрузка'):
            yield self.getObjectByGuid(guid)

    def getObjectByGuid(self, object_guid):
        headers = {
            'User-Agent': self.userAgent,
        }
        params = {
            'guid': object_guid,
        }
        popit = 50
        while True:
            url = 'https://eias.rospotrebnadzor.ru/api/households/industrial_object'
            request = self.session.get(
                url,
                headers=headers,
                params=params,
                cookies=self.cookies
            )
            try:
                return request.json()
            except:
                popit -= 1
                if popit == 0:
                    raise Exception(f'{object_guid} {request}')
                continue

    def getObjectsByinn(self, inn, region: str = None) -> list:
        if not region:
            region = '1|4|22|28|29|30|2|31|32|3|33|34|35|36|5|93|79|75|90|37|6|38|7|39|8|40|41|9|10|42|43|11|44|23|24|91|45|46|47|48|94|49|12|13|77|50|51|83|52|53|54|55|56|57|58|59|25|60|61|62|63|78|64|14|65|66|92|15|67|26|68|16|69|70|71|17|72|18|73|27|19|86|95|74|20|21|87|89|76'

        url = f"https://eias.rospotrebnadzor.ru/api/households/industrial_objects/v2?limit=5000&sort=created_at&region=in::{region}&inn={inn}&supervised_status=in::supervised"
        request = self.session.get(url, headers={'User-Agent': self.userAgent})
        return request.json()['industrial_objects']

    def getSubjectByGuid(self, subject_guid, region):
        popit = 50
        while True:
            url = f'https://eias.rospotrebnadzor.ru/api/households/employee/subject_entity?guid={subject_guid}&region={region}'
            request = self.session.get(url, headers={'User-Agent': self.userAgent})
            try:
                return request.json()
            except:
                popit -= 1
                if popit == 0:
                    raise Exception(f'{subject_guid} {request}')
                continue

    def getSubjectByObjectGuid(self, object_guid):
        popit = 50
        while True:
            object_data = self.getObjectByGuid(object_guid)
            try:
                subject_guid = object_data['subject_guid']
                region = object_data['common_info']['address']['region']['region_code']
                return {'object_data': object_data,
                        'subject_data': self.getSubjectByGuid(subject_guid=subject_guid, region=region)}
            except Exception as ex:
                popit -= 1
                if popit == 0:
                    raise Exception(f'{object_guid} {object_data} {ex}')
                continue

    def prepareForERVK(self, object_guid) -> dict:
        object_subject_info = self.getSubjectByObjectGuid(object_guid)
        dict_for_ERVK = {}
        subject_data = object_subject_info['subject_data']
        object_data = object_subject_info['object_data']

        dict_for_ERVK['guid'] = object_data['guid']
        dict_for_ERVK['object_name'] = formatter_for_addresses(object_data['common_info']['name'])
        try:
            dict_for_ERVK['ervk_number'] = str(object_data['knd']['ervk_id'])
        except:
            dict_for_ERVK['ervk_number'] = '0'
        try:
            dict_for_ERVK['object_address'] = formatter_for_addresses(object_data['common_info']['address']['full_address'])
        except:
            dict_for_ERVK['object_address'] = formatter_for_addresses(object_data['common_info']['additional_address_info'])
        try:
            dict_for_ERVK['risk'] = formatter_for_addresses(object_data['risk_info']['actual_risk_category_activities_name']).lower()
        except:
            try:
                dict_for_ERVK['risk'] = formatter_for_addresses(object_data['risk_info']['risk_category_activities_name']).lower()
            except:
                dict_for_ERVK['risk'] = riskCategoryById[object_data['historical_risk_info']['risk_category_id']]

        dict_for_ERVK['object_category'] = object_data['common_info']['separate_object']['name'] if object_data['common_info']['separate_object'] else object_data['risk_info']['risk_scope_name']
        if subject_data['common_info']['entity_type'] == 'ip':
            entity_type = 'Индивидуальные предприниматели'
            isIp = True
        else:
            entity_type = 'Юридические лица'
            isIp = False
        dict_for_ERVK['isIp'] = isIp
        dict_for_ERVK['entity_type'] = entity_type

        if isIp:
            ipFio = str(subject_data['short_name']).split(' ')
            dict_for_ERVK['ipName'] = ipFio[1]
            dict_for_ERVK['ipFamily'] = ipFio[0]
            dict_for_ERVK['ipSurname'] = ' '.join(ipFio[2:]) if len(ipFio) > 2 else ''
        else:
            short_name = subject_data['short_name']
            full_name = subject_data['common_info']['full_name']
            dict_for_ERVK['ur_address'] = subject_data['common_info']['full_address']
            dict_for_ERVK['full_name'] = full_name
            dict_for_ERVK['short_name'] = short_name if short_name else full_name
        dict_for_ERVK['inn'] = str(subject_data['common_info']['inn'])
        dict_for_ERVK['ogrn'] = str(subject_data['common_info']['ogrn'])
        dict_for_ERVK['ogrn_date'] = subject_data['registration_date']
        dict_for_ERVK['region'] = object_data['common_info']['address']['region']['value']

        return dict_for_ERVK


if __name__ == '__main__':
    eias = Eias()
    # io = eias.loadAllObjects()
    # print(io)
    # rhs_object = eias.getObjectsByinn('5006004145')
    # pprint(rhs_object)
    # direct_mysql.enterFromFullRhsObject(object_data=rhs_object)

    # pprint(eias.getObjectByGuid('c251cd3a-e140-48d4-9881-34c107e0157e'))
    pprint(eias.prepareForERVK('2c7c847e-ee28-47d7-bc48-78a3c2bca7f8'))

    # objects = eias.getObjectsByinn('7701984274')
    # addresses = []
    # for _object in objects:
    #     if re.search('очис', str(_object['name']).lower()):
    #         addresses.append(f"{_object['name']} ({_object['address']['full_address'].strip()})")
    #
    #         print(_object['name'], _object['risk_category_activities_name'])
    # else:
    #     pprint(_object)
    # print(len(addresses))
    # print()
    # print(', '.join(addresses).replace('Город', "город").replace(' г ', ' г. ').replace(' ул ', ' ул. ').replace(' п ', ' п. ').replace(' с ', ' с. ').replace(' д ', ' д. '))
