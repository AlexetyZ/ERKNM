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


if __name__ == '__main__':
    curDate()
    # main()
    # result = mergeDatesByWeeks({
    #     '2024-05-12': 5,
    #     '2024-05-06': 3,
    #     '2024-05-13': 7,
    #     '2024-05-11': 7
    # })
    # pprint(result)

