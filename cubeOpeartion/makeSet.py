import datetime

from mongo_database import WorkMongo as wmKNM, unpac_idAggregation, convertForsaving
from mongo_rhs import WorkMongo as wmRHS
from pprint import pprint
from Dates_manager import getListDaysFromYear
from tqdm import tqdm
from Dictionary import getActualTuName, sortObjectKindInGroup, tu_iso, tuCodeRegion, group_kinds
import uuid
from Dates_manager import differenceCalendaryDays, reformDateToEn


def makeObjectsKindTuDateSet(statusGroup: str = 'accepted'):
    wm_knm = wmKNM('knm')
    if statusGroup == 'accepted':
        function = wm_knm.reportFromAcceptKNMObjectCategoryByDate
    else:
        function = wm_knm.reportFromDeniedKNMObjectCategoryByDate
    knms = function()
    knms = unpac_idAggregation(knms)
    for knm in knms:
        if knm['controllingOrganization'] == 'Федеральная служба по надзору в сфере защиты прав потребителей и благополучия человека':
            continue
        actualName = getActualTuName(knm['controllingOrganization'])
        if not actualName or actualName == 'Федеральная служба по надзору в сфере защиты прав потребителей и благополучия человека':
            continue
        knm['controllingOrganization'] = actualName
        knm['codeRegion'] = tuCodeRegion[actualName]
        knm['iso'] = tu_iso[actualName]
        knm['groupKind'] = sortObjectKindInGroup(knm['objectsKind'])
        knm['month'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').month
        knm['year'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').year
    return knms


def makeKnmTypeTuDateSet(statusGroup: str = 'accepted'):
    wm_knm = wmKNM('knm')
    if statusGroup == 'accepted':
        function = wm_knm.reportFromAcceptKNMTypeKindReasonByDate
    else:
        function = wm_knm.reportFromDeniedKNMTypeKindReasonByDate
    knms = function()
    knms = unpac_idAggregation(knms)
    for knm in knms:
        actualName = getActualTuName(knm['controllingOrganization'])
        if not actualName:
            continue
        knm['controllingOrganization'] = actualName
        knm['codeRegion'] = tuCodeRegion[actualName]
        knm['iso'] = tu_iso[actualName]
        knm['month'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').month
        knm['year'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').year
    return knms


def makeKNMByObjectsKind(groupName, kinds, risks, notIn: bool = False):
    wm_knm = wmKNM('knm')
    knms = wm_knm.reportKNM_by_kind_objects(kinds, risks, notIn=notIn)
    knms = unpac_idAggregation(knms)
    for knm in knms:
        actualName = getActualTuName(knm['controllingOrganization'])
        if not actualName:
            continue
        knm['controllingOrganization'] = actualName
        if not tuCodeRegion[actualName]:
            raise Exception(knm['controllingOrganization'])
        knm['codeRegion'] = tuCodeRegion[actualName]
        knm['iso'] = tu_iso[actualName]
        knm['groupName'] = groupName
        knm['risk'] = risks

        knm['month'] = knm['month'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').month
        knm['year'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').year
    return knms


def makeKNMByOrdinary():
    wm_knm = wmKNM('knm')
    knms = wm_knm.reportKNM_by_ordinary()
    knms = unpac_idAggregation(knms)
    _dictAppReq = [

    ]
    for knm in knms:
        actualName = getActualTuName(knm['controllingOrganization'])
        if not actualName:
            continue
        knm['controllingOrganization'] = actualName
        if not tuCodeRegion[actualName]:
            raise Exception(knm['controllingOrganization'])
        knm['codeRegion'] = tuCodeRegion[actualName]
        knm['iso'] = tu_iso[actualName]
        # knm['approveRequired'] = _dictAppReq[knm['approveRequired']] if knm['approveRequired'] in _dictAppReq else "Не требует согласования"
        knm['month'] = knm['month'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').month
        knm['year'] = datetime.datetime.strptime(knm['startDateEn'], '%Y-%m-%d').year
    return knms


def makeKNMAByObjectsAllKind():
    for groupName, kinds in group_kinds.items():
        yield makeKNMByObjectsKind(groupName, kinds)


def make_prosecutor_apply_period():
    """
    Делаем агрегацию и приводим каждую ее запись к стандарту ТУ, время согласования прокуратуры, количество КНМ, год
    @return:
    """
    wm_knm = wmKNM('knm')
    _set = wm_knm.reportPeriodApplyingProsecutors()
    _set = unpac_idAggregation(_set)
    result = []
    for _obj in _set:
        difference = differenceCalendaryDays(_obj['orderDate'], _obj['responceDate'])
        if difference < -30 or difference > 14:
            continue
        normalCalculation = differenceCalendaryDays(_obj['orderDate'], _obj['responceDate']) * _obj['objectsCount']
        actualName = getActualTuName(_obj['controllingOrganization'])
        if not actualName:
            continue
        _obj['controllingOrganization'] = actualName
        _obj['codeRegion'] = tuCodeRegion[actualName]
        _obj['iso'] = tu_iso[actualName]
        _obj['avgsumdate'] = normalCalculation if normalCalculation >= 0 else 1
        _obj['orderDate'] = reformDateToEn(_obj['orderDate'])
        _obj['difference'] = difference
        _obj['responceDate'] = reformDateToEn(_obj['responceDate'])
        result.append(_obj)

    return result




def makeRHStuobjectsKindriskSet():
    wm_rhs = wmRHS()
    rhsObjs = wm_rhs.reportTuObjectsKindRisk()
    rhsObjs = unpac_idAggregation(rhsObjs)

    for _obj in rhsObjs:
        actualName = getActualTuName(_obj['controllingOrganization'])
        _obj['controllingOrganization'] = actualName
        _obj['codeRegion'] = tuCodeRegion[actualName]
        _obj['iso'] = tu_iso[actualName]
        _obj['groupKind'] = sortObjectKindInGroup(_obj['objectsKind'])
    return rhsObjs


def makeEffIndicSet(indicatorName, query):
    results = []
    for tu, indicatorValue, comment in query:
        actualName = getActualTuName(tu)
        results.append({
            'controllingOrganization': actualName,
            'codeRegion': tuCodeRegion[actualName],
            'iso': tu_iso[actualName],
            'indicatorName': indicatorName,
            'indicatorValue': indicatorValue,
            'comment': comment
        })
    return results



def makeRHStuOkvedKindriskSet():
    wm_rhs = wmRHS()
    rhsObjs = wm_rhs.reportTuOkvedRisk()
    rhsObjs = unpac_idAggregation(rhsObjs)
    # pprint(rhsObjs)
    for _obj in rhsObjs:
        actualName = getActualTuName(_obj['controllingOrganization'])
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
    resultSet = makeKNMByOrdinary()
    # resultSet = findBySetQuery()
    pprint(list(resultSet))
