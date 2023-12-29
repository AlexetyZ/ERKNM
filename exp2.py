from Dictionary import tuList
from pprint import pprint
from Dates_manager import split_year_for_periods
from datetime import datetime, date
import re


def mergeDatesByWeeks(dates: dict):
    """
    dict should be like "date: int(value)"
    this function sum values while sort dates by weeks
    the date in returning like key is start day of the week
    """
    weeksStart = list(_mergeDatesByWeeks(dates))
    keys = set(list(n)[0] for n in weeksStart)
    totals = {unique_key: sum(v for k, v in weeksStart if k == unique_key) for unique_key in keys}
    return totals


def _mergeDatesByWeeks(dates: dict):   # dates format yyyy-mm-dd
    for date, val in dates.items():
        yield shakePeriods(date, val)


def shakePeriods(date, value):
    year = int(str(date).split('-')[0])
    periods = split_year_for_periods(year=year, parts=52)

    for period in periods:
        if period['start'] <= date <= period['end']:
            return period['start'], value
    return None


def stringToDatetime(string):
    res = datetime.strptime(string, '%Y-%M-%d')
    # print(res)
    return string


def main():
    string = "https://rospo"
    print(re.search(r'https://.*', string).string)


def curDate():
    print(date.today())

def zipLists():
    addresses = [
        '423877, Республика Татарстан (Татарстан), ТУКАЕВСКИЙ, НИЖНЕСУЫКСИНСКОЕ, УЛ МАГИСТРАЛЬНАЯ, Д. 1, 23',
        ' Республика Башкортостан, г.Уфа, ул. Академика Ураксина, 2',
        'Республика Башкортостан, г.Уфа, ул. Города Галле, 34',
        'Республика Башкортостан, г.Уфа, ул. Баязита Бикбая, 40/1',
        'Республика Башкортостан, г.Уфа, ул. Ферина, 22а',
        'Республика Башкортостан, г.Уфа, ул.  Центральная, 33/9',
        'Республика Башкортостан, г.Уфа, ул. Левитана, 26/2',
        '452755, Республика Башкортостан, г. Туймазы,  ул. 70 лет Октября,  д. 12А',
        '452755, Республика Башкортостан, г. Туймазы,  ул. 70 лет Октября,  д. 12А',
        'Республика Башкортостан, г. Октябрьский, ул.Кортунова, 2В',
        'Республика Башкортостан, г. Октябрьский, ул. Кувыкина, 46/2',
        'Республика Башкортостан, г. Октябрьский, проспект Ленина, д. 87',
        '452755, Республика Башкортостан, г. Туймазы,  ул. Фабричная, 2 В',
        '452755, Республика Башкортостан, г. Туймазы,  ул. Фабричная, 2 В',
        '452490,Республика Башкортостан,Салаватский район,с.Малояз, ул.60 лет СССР,д.8/Е',
        '452530,Республика Башкортостан,Дуванский район, Месягутово, ул.Коммунистическая,92',
        '1. 43200,Республика Башкортостан, г.Ишимбай, ул.Стахановская , д.39/2.',
        ' 453250, Республика Башкортостан, г.Салават, ул.Ленина , д.24А',
        'Республика Башкортостан, г. Нефтекамск, ул. Дзержинского, 19а',
        '453020, Башкортостан Респ, р-н Кармаскалинский, с Кармаскалы, ул Кирова, д. 54Д.',
        '452170, Башкортостан Респ, р-н Чишминский, рп Чишмы, ул Революционная, 86.',
        '452711, Башкортостан Респ, р-н Буздякский, с Буздяк, ул Красноармейская, 18.',
        '453400, Башкортостан Респ, Давлеканово, г Давлеканово, ул. ул. Заводская 1-я, 7а',
        '452980, Республика Башкортостан, Балтачевский район, с. Старобалтачево, ул. Советская, д.74'
    ]

    riskCategory = [
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск',
        'высокий риск', 'высокий риск'
    ]
    objectsType = [
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Производственные объекты',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия',
        'Деятельность и действия'
    ]

    objectsKind = [
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями',
        'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями'
    ]


    return zip(addresses, riskCategory, objectsType, objectsKind)


if __name__ == '__main__':
    print(list(zipLists()))
    # curDate()
    # main()
    # result = mergeDatesByWeeks({
    #     '2024-05-12': 5,
    #     '2024-05-06': 3,
    #     '2024-05-13': 7,
    #     '2024-05-11': 7
    # })
    # pprint(result)

