import requests
from bs4 import BeautifulSoup
import fake_useragent
from direct_pxl import Operation
from direct_egrul import Direct


class Contragents:

    def request(self, page: int = 1) -> list:
        session = requests.Session()
        user_agent = fake_useragent.UserAgent().random
        url = 'https://www.1cont.ru/contragent/by-region/kemerovskaya-oblast'
        headers = {
            "User-Agent": user_agent
        }
        data = {
            "page": f'{page}',
        }
        get = session.get(
            url=url,
            headers=headers,
            data=data
        )
        organization_list = BeautifulSoup(get.text, 'lxml').find_all('div', {'class': 'tr tbody-tr'})
        return organization_list

    def parse(self, organizations):
        info_list = []
        for organization in organizations:
            org = {}
            attributes = organization.find_all('div', {'class': 'td'})
            for n, attribute in enumerate(attributes):
                # print(attribute)
                if n == 0:
                    name = organization.find('div', {'class': 'td'}).text
                    org["name"] = name
                else:
                    key = str(attribute.find('div', {'class': 'td__caption'}).text).replace(':', '').replace('\xa0', ' ').strip()
                    value = str(attribute.find('div', {'class': 'td__text'}).text).replace(':', '').replace('\xa0', ' ').strip()
                    org[key] = value
            info_list.append(org)
        # print(info_list)
        return info_list


class RPN_site:

    def request(self, inn):
        object_list = []
        session = requests.Session()
        user_agent = fake_useragent.UserAgent().random
        url = f'https://risk.rospotrebnadzor.ru/risk2/index.html?data_type=activity&data_inn={inn}&data_ogrn=&data_name=&oper=search&xcvar__javascript_error=0'
        headers = {
            "User-Agent": user_agent
        }
        data = {
            'data_type': 'activity',
            'data_inn': f'{inn}',
            'data_ogrn': '',
            'data_name': '',
            'oper': 'search',
            'xcvar__javascript_error': '0'
        }
        get = session.get(
            url=url,
            headers=headers,
            data=data
        )

        try:
            objects = BeautifulSoup(get.text, 'lxml').find_all('tr', {'class': 'xc_table_view_last_tr'})
        except:
            return None

        obj_data = {}
        for obj in objects:
            attributes = obj.find_all('td')
            # print(attributes[0].text)
            obj_data['kind'] = attributes[0].text
            obj_data['name'] = attributes[1].text
            obj_data['ogrn'] = attributes[2].text
            obj_data['inn'] = attributes[3].text
            obj_data['address'] = attributes[4].text
            obj_data['risk'] = attributes[5].text
        object_list.append(obj_data)
        return object_list


if __name__ == '__main__':
    egrul = Direct(interactive=False)
    rpn_risk = RPN_site()
    cont = Contragents()
    o = Operation()

    dict_org = []
    for n in range(38, 43):   # 728
        organizations = cont.request(page=n)
        parse_result = cont.parse(organizations)
        dict_org.extend(parse_result)
    # print(dict_org)
    for org in dict_org:
        if org['Статус организации'] == 'Ликвидирована':
            inn = org['ИНН']
            liqv_inf = egrul.find_info_liquidate(inn)
            if liqv_inf != 'Информация о ликвидации отсутствует':

                objects = rpn_risk.request(inn)
                # print()
                if objects != [{}]:
                    print("есть неучтеныш")
                    last_row = o.detect_last_row()
                    o.change_value_in_cell(last_row, 2, value=org['name'], saving=False)
                    o.change_value_in_cell(last_row, 3, value=org['ОГРН'], saving=False)
                    o.change_value_in_cell(last_row, 4, value=org['ИНН'], saving=False)
                    o.change_value_in_cell(last_row, 5, value=liqv_inf, saving=False)

                o.save_document(path="C:\\Users\zaitsev_ad\Desktop\проверка риск Кемеровская область")

