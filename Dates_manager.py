import calendar
import datetime
import math



def period_between_month(year: int = 2023, month: int = 1):
    month_last_day = calendar.monthrange(year, month)[1]
    start = datetime.date(year, month, 1).strftime('%Y-%m-%d')
    end = datetime.date(year, month, month_last_day).strftime('%Y-%m-%d')
    result = ({'start': str(start), 'end': str(end)})
    return result


def differenceCalendaryDays(date1: str, date2: str):
    """
    Все даты в формате дд.мм.ГГГГ
    @param date1: Дата начала
    @param date2: Дата окончания
    @return: Разница в календарных днях
    """
    date1 = datetime.datetime.strptime(date1, '%d.%m.%Y')
    date2 = datetime.datetime.strptime(date2, '%d.%m.%Y')
    return (date2 - date1).days


def reformDateToEn(date: str):
    """

    @param date: date format dd.mm.YYYY
    @return: date format YYYY-mm_dd
    """
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')



def periods_into_month(year: int = 2023, month: int = 1, parts: int = 2):
    month_last_day = calendar.monthrange(year, month)[1]
    start = datetime.date(year, month, 1).strftime('%Y-%m-%d')
    part_month = math.floor(month_last_day/parts)
    # print(part_month)
    result = []
    day = 1
    for part in range(parts):
        start_part = datetime.date(year, month, day).strftime('%Y-%m-%d')
        if part == range(parts)[-1]:
            result.append({'start': start_part, 'end': datetime.date(year, month, month_last_day).strftime('%Y-%m-%d')})
        else:
            end_part = datetime.date(year, month, day+part_month).strftime('%Y-%m-%d')
            result.append({'start': start_part, 'end': end_part})

            day = day+part_month
            day += 1

    return result


def split_period(date_start, date_end, parts: int = 2) -> list:
    start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    delta = (end - start).days + 1 - parts

    len_part = math.floor(delta/parts)
    # print(len_part)


    result = []

    for part in range(parts):

        if part == range(parts)[-1]:
            result.append({'start': start.strftime('%Y-%m-%d'), 'end': end.strftime('%Y-%m-%d')})
        else:
            end_part = start + datetime.timedelta(days=len_part)
            result.append({'start': start.strftime('%Y-%m-%d'), 'end': end_part.strftime('%Y-%m-%d')})
            start += datetime.timedelta(days=len_part+1)

    return result


def split_year_for_periods(year: int, parts: int = 50) -> list:
    return split_period(date_start=f'{year}-01-01', date_end=f'{year}-12-31', parts=parts)


def getListDaysFromYear(year: int):
    periods = split_year_for_periods(year=year, parts=366 if calendar.isleap(year) else 365)
    return [period['start'] for period in periods]


def sortWeek(date: str):   # Формат ГГГГ-ММ-ДД
    year = int(date.split("-")[0])
    weeks = split_year_for_periods(year=year, parts=52)

    for week in weeks:
        if week['start'] <= date <= week['end']:
            return week
    raise Exception(f"Can't find date {date} in period")


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


if __name__ == '__main__':
    print([p['start'] for p in split_period(date_start='2024-05-01', date_end='2024-05-10', parts=10)])
    # dates = split_period(date_start='2022-01-01', date_end='2022-12-31', parts=52)
    # print(dates)
