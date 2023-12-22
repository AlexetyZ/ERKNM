import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.999 (corp) Yowser/2.5 Safari/537.36'

def main(url):
    cookies = {
        '_ym_uid': '170316826259984830',
        '_ym_d': '1703168262',
        'BX_USER_ID': 'a6c68fbc4de716f6b207d6a712b59184',
        'last_login_u_id': '957306',
        'auth_token': 'fc2854cad0b48c578400e9698bf6e352ae567d41',
        '_ym_isad': '1',
        'xcuser_action': 'cc001088-a0dd-11ee-b60c-003048bddde7',
        'xcuser_sess': 'cc002cfb-a0dd-11ee-b60c-003048bddde7',
        'xcuser_sess_session': 'cc0030b7-a0dd-11ee-b60c-003048bddde7',
        'PHPSESSID': '529kQNXUOxZ26Oqb256Ql5RC5SFwjpQV',
        'sputnik_session': '1703258666246|1',
    }

    headers = {
        'authority': '23.rospotrebnadzor.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '_ym_uid=170316826259984830; _ym_d=1703168262; BX_USER_ID=a6c68fbc4de716f6b207d6a712b59184; last_login_u_id=957306; auth_token=fc2854cad0b48c578400e9698bf6e352ae567d41; _ym_isad=1; xcuser_action=cc001088-a0dd-11ee-b60c-003048bddde7; xcuser_sess=cc002cfb-a0dd-11ee-b60c-003048bddde7; xcuser_sess_session=cc0030b7-a0dd-11ee-b60c-003048bddde7; PHPSESSID=529kQNXUOxZ26Oqb256Ql5RC5SFwjpQV; sputnik_session=1703258666246|1',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.999 (corp) Yowser/2.5 Safari/537.36',
    }

    response = requests.get('https://23.rospotrebnadzor.ru/', cookies=cookies, headers=headers, verify=False)
    soup0 = BeautifulSoup(response.text, 'lxml').find_all('a')
    for a in soup0:
        print(a)
        # print(re.search(r'https://.*', str(a.get('href'))).string if not None else '-')

    return [re.search(r'https://.*', str(a)).string for a in soup0 if not None]
    # return None

if __name__ == '__main__':
    url = 'https://23.rospotrebnadzor.ru/'
    print(main(url))
