from mongo_database import WorkMongo
from pprint import pprint
from Dates_manager import getListDaysFromYear


def makeObjectsKindTuDateSet(year: int):
    # datesYear = getListDaysFromYear(year)
    # print(datesYear)

    wm_knm = WorkMongo('knm')
    #
    date = f'{year}-07-01'
    knms = wm_knm.reportFromAcceptKNMObjectCategoryByDate(f'{year}-07-01')
    pprint(list(knms))


if __name__ == '__main__':
    year = '2024'
    resultSet = makeObjectsKindTuDateSet(int(year))
    print(resultSet)

