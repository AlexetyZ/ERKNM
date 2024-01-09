from mongo_database import WorkMongo
from pprint import pprint
from Dates_manager import getListDaysFromYear
from tqdm import tqdm
from Dictionary import getActualTuName, sortObjectKindInGroup, tu_iso


def makeObjectsKindTuDateSet(year: int, statusGroup: str = 'accepted'):
    datesYear = getListDaysFromYear(year)
    wm_knm = WorkMongo('knm')
    result = []
    if statusGroup == 'accepted':
        function = wm_knm.reportFromAcceptKNMObjectCategoryByDate
    else:
        function = wm_knm.reportFromDeniedKNMObjectCategoryByDate

    for date in tqdm(datesYear, desc='Сбор по дням...'):
        knms = function(date)
        knms = wm_knm.unpac_idAggregation(knms)
        for knm in knms:
            actualName = getActualTuName(knm['controllingOrganization'])
            knm['controllingOrganization'] = actualName
            knm['iso'] = tu_iso[actualName]
            knm['groupKind'] = sortObjectKindInGroup(knm['objectsKind'])
            knm['startDateEn'] = date
        result.extend(knms)
    return result

def findBySetQuery():
    """
    найти по обратным параметрам
    """
    wm = WorkMongo('knm')
    knms = wm.free_command(
        request={
            'controllingOrganization': 'Управление Роспотребнадзора по Мурманской области',
            'status': 'Ожидает проведения',
            'objectsKind': 'Предоставление социальных услуг с обеспечением проживания',
            'startDateEn': '2024-12-28'
        },
        fields={
            '_id': 0,
            'erpId': 1
        }
    )
    return knms

if __name__ == '__main__':
    year = '2024'
    resultSet = makeObjectsKindTuDateSet(int(year))
    # resultSet = findBySetQuery()
    pprint(list(resultSet))
