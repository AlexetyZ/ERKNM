import datetime

from bs4 import BeautifulSoup
from requests import Session
import json
import re
import datetime

class Egrul:
    def __init__(self):
        self.session = Session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.765 Yowser/2.5 Safari/537.36"  # UserAgent().random
        self.header = {'User-Agent': self.user_agent}
        link = 'https://egrul.nalog.ru/index.html'

        self.session.get(link, headers=self.header)

    def find_in_egrul(self, cell, row: int = 0):

        # get request for first page

        # soup = BeautifulSoup(get1.text, 'lxml')

        # post request for "t"
        link_post_t = 'https://egrul.nalog.ru/'
        data_post_t = {
            'vyp3CaptchaToken': '',
            'page': '',
            'query': cell,

            # 'Адрес': str(ipaddress.IPv4Address(random.randint(0, 2 ** 32))),
            'PreventChromeAutocomplete': ''

        }
        post_t = self.session.post(link_post_t, headers={'User-Agent': self.user_agent}, data=data_post_t)
        soup_post_t = BeautifulSoup(post_t.text, 'lxml')
        p_post_t = json.loads(soup_post_t.find('p').text)
        # print(p_post_t)

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

            info = datas_dict['rows'][row]
            return info
        except Exception as ex:
            # print(soup_post_t)
            return f'Возникла ошибка: {ex}'


if __name__ == '__main__':
    print(datetime.datetime.now())
    Egrul().find_in_egrul('7716154981')
    print(datetime.datetime.now())
