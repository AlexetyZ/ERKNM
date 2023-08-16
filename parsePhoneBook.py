import requests
from bs4 import BeautifulSoup
import json


class Request:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',

            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'phone.rpn.int',
            'Origin': 'http://phone.rpn.int',
            'Referer': 'http://phone.rpn.int/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def get_book(self):
        data = {
            'method': 'parent_0',
            'pattern': '% ФБУЗ %'
        }
        response = self.session.post("http://phone.rpn.int/xhr/xhr_phonebook.php", data=json.dumps(data), headers=self.headers)

        print(response.json())


if __name__ == '__main__':
    Request().get_book()
