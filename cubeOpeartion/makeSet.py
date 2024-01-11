from mongo_database import WorkMongo as wmKNM, unpac_idAggregation, convertForsaving
from mongo_rhs import WorkMongo as wmRHS
from pprint import pprint
from Dates_manager import getListDaysFromYear
from tqdm import tqdm
from Dictionary import getActualTuName, sortObjectKindInGroup, tu_iso, tuCodeRegion
import uuid


def makeObjectsKindTuDateSet(year: int, statusGroup: str = 'accepted'):
    datesYear = getListDaysFromYear(year)
    wm_knm = wmKNM('knm')
    result = []
    if statusGroup == 'accepted':
        function = wm_knm.reportFromAcceptKNMObjectCategoryByDate
    else:
        function = wm_knm.reportFromDeniedKNMObjectCategoryByDate
    # dates = ['2024-05-01', '2024-05-02', '2024-05-03', '2024-05-04', '2024-05-05', '2024-05-06', '2024-05-07', '2024-05-08', '2024-05-09', '2024-05-10']
    for date in tqdm(datesYear, desc='Сбор по дням...'):
        knms = function(date)
        knms = unpac_idAggregation(knms)
        for knm in knms:
            actualName = getActualTuName(knm['controllingOrganization'])
            knm['id'] = uuid.uuid4()
            knm['controllingOrganization'] = actualName
            knm['codeRegion'] = tuCodeRegion[actualName]
            knm['iso'] = tu_iso[actualName]
            knm['groupKind'] = sortObjectKindInGroup(knm['objectsKind'])
            knm['startDateEn'] = date
        result.extend(knms)
    return result


def makeRHStuobjectsKindriskSet():
    wm_rhs = wmRHS()
    rhsObjs = wm_rhs.reportTuObjectsKindRisk()
    rhsObjs = unpac_idAggregation(rhsObjs)

    for _obj in rhsObjs:
        actualName = getActualTuName(_obj['controllingOrganization'])
        _obj['id'] = uuid.uuid4()
        _obj['controllingOrganization'] = actualName
        _obj['codeRegion'] = tuCodeRegion[actualName]
        _obj['iso'] = tu_iso[actualName]
        _obj['groupKind'] = sortObjectKindInGroup(_obj['objectsKind'])
    return rhsObjs


def makeRHStuOkvedKindriskSet():
    wm_rhs = wmRHS()
    rhsObjs = wm_rhs.reportTuOkvedRisk()
    rhsObjs = unpac_idAggregation(rhsObjs)
    # pprint(rhsObjs)
    for _obj in rhsObjs:
        actualName = getActualTuName(_obj['controllingOrganization'])
        _obj['id'] = uuid.uuid4()
        _obj['controllingOrganization'] = actualName
        _obj['codeRegion'] = tuCodeRegion[actualName]
        _obj['iso'] = tu_iso[actualName]

    return rhsObjs





def findBySetQuery():
    """
    найти по обратным параметрам
    """
    wm = wmKNM('knm')
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
    resultSet = makeRHStuobjectsKindriskSet()
    # resultSet = findBySetQuery()
    pprint(list(resultSet))
