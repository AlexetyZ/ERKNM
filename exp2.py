from Dictionary import tuList
from pprint import pprint
from Dates_manager import split_year_for_periods
from datetime import datetime
import re


def shakePeriods(date):
    periods = split_year_for_periods(year=2024, parts=52)

    for period in periods:
        if period['start'] <= date <= period['end']:
            return period
    return None


def stringToDatetime(string):
    res = datetime.strptime(string, '%Y-%M-%d')
    # print(res)
    return string


def main():
    string = "https://rospo"
    print(re.search(r'https://.*', string).string)


if __name__ == '__main__':
    main()
    # result = shakePeriods('2024-05-12')
    # pprint(result)

