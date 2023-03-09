from bs4 import BeautifulSoup
import os

with open("C:\\Users\zaitsev_ad\Desktop\\fp.rospotrebnadzor.ru.txt", 'r', encoding='utf8') as file:
    html_page = file.read()


def parse_reestr():
    print(html_page)
    soup = BeautifulSoup(html_page, 'lxml').find_all()


def main():
    parse_reestr()


if __name__ == '__main__':
    main()