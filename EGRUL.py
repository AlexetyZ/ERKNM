from bs4 import BeautifulSoup
from requests import Session
import fake_useragent
import json
import re


class Egrul:
    def __init__(self):
        self.session = Session()
        self.user_agent = fake_useragent.UserAgent().random  # UserAgent().random
        self.header = {'User-Agent': self.user_agent}

    def find_in_egrul(self, cell, region='52'):

        # get request for first page
        link = 'https://egrul.nalog.ru/index.html'

        get1 = self.session.get(link, headers=self.header)
        # soup = BeautifulSoup(get1.text, 'lxml')

        # post request for "t"
        link_post_t = 'https://egrul.nalog.ru/'
        data_post_t = {
            'vyp3CaptchaToken': '',
            'page': '',
            'query': cell,
            'region': region,
            # 'Адрес': str(ipaddress.IPv4Address(random.randint(0, 2 ** 32))),
            'PreventChromeAutocomplete': ''

        }
        post_t = self.session.post(link_post_t, headers=self.header, data=data_post_t)
        soup_post_t = BeautifulSoup(post_t.text, 'lxml')
        p_post_t = json.loads(soup_post_t.find('p').text)
        # print(p_post_t['t'])

        # get request for datas
        try:
            link_get_datas = f"https://egrul.nalog.ru/search-result/{p_post_t['t']}"
            get_datas = self.session.get(link_get_datas, headers=self.header)
            soup_get_datas = BeautifulSoup(get_datas.text, 'lxml')
            while soup_get_datas.find('p').text == '{"status":"wait"}':
                link_get_datas = f"https://egrul.nalog.ru/search-result/{p_post_t['t']}"
                get_datas = self.session.get(link_get_datas, headers=self.header)
                soup_get_datas = BeautifulSoup(get_datas.text, 'lxml')
                # print(soup_get_datas)

            datas_dict = json.loads(soup_get_datas.find('p').text)

            info = datas_dict['rows'][0]
            return info
        except:
            print(soup_post_t)
            return 'Возникла ошибка'
