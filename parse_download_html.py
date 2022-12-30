from bs4 import BeautifulSoup
import requests


with open("C:\\Users\zaitsev_ad\Desktop\регионы.html", 'r', encoding='utf-8') as file:
    content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    all_href = soup.find_all('a', {'target': '_blank'})

    for href in all_href:
        print(href.text, ';', str(href['href']).split('//')[1].split('.rospotrebnadzor.ru/')[0])