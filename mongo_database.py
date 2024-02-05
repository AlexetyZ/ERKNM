import re

import xl
from Dates_manager import *
from pymongo import MongoClient
from multiprocessing import Pool
import pprint
import openpyxl
from tqdm import tqdm
from datetime import datetime
from pprint import pprint
import Dictionary as d


def unpac_idAggregation(_list):
    result = []
    for record in _list:
        new_record = {}
        for key, value in record.items():
            if key == "_id":
                for kv, vv in value.items():
                    new_record[kv] = vv
            else:
                new_record[key] = value
        result.append(new_record)
    return result


def convertForsaving(results: list[dict]) -> list:
    title = list(results[0].keys())
    values = [list(result.values()) for result in list(results)]
    return title, values


class WorkMongo:
    def __init__(self, collection_name: str = 'knm'):
        client = MongoClient('localhost', 27017)

        db = client['knm']
        self.collection = db[collection_name]

    def insert(self, knm):
        self.collection.insert_one(knm)

    def multiple_insert(self, processes, knm_list):
        pool = Pool(processes)
        pool.map(self.insert, knm_list)

    def insert_many(self, knm_list):
        self.collection.insert_many(knm_list)

    def count_objects(self, **filters):
        pipeline = [{"$match": filters}, {"$group": {"_id": 1, "count": {"$sum": {"$size": "$addresses"}}}}]
        return list(self.collection.aggregate(pipeline))[0]['count']

    def reportByObjects(self, **filters):
        return self.collection.aggregate([{"$match": filters}, {"$unwind": "$objectsKind"},
                                          {"$group": {"_id": "$objectsKind", "count": {"$sum": 1}}}])

    def reportByRisk(self, **filters):
        return self.collection.aggregate(
            [{"$match": filters}, {"$unwind": "$riskCategory"},
             {"$group": {"_id": "$riskCategory", "count": {"$sum": 1}}}])

    def free_command(self, request=None, fields=None):

        if fields is None:
            fields = {}
        if request is None:
            request = {}

        return self.collection.find({**request}, {**fields})

    def getZPPInspections(self):
        request = {
            "supervisionType": "Федеральный государственный контроль (надзор) в области защиты прав потребителей",

        }
        responce = {
            "_id": 0,
            "approveDocOrderDate": 1,
            "comment": 1,
            "controllingOrganization": 1,
            "erpId": 1,
            "inn": 1,
            "kind": 1,
            "knmType": 1,
            "organizationName": 1,
            "reasonsList": 1,
            "requirements": 1,
            "startDate": 1,
            "status": 1,
            "stopDate": 1,
            "supervisionType": 1,
        }
        return self.collection.find(request, responce)

    def getRhsObjectsByTu(self, objectsKind: list, objectsRisk: list = None):
        """
        только если collection_name задан rhs!!!!!!!
        @return:
        """
        if not objectsRisk:
            objectsRisk = d.risk_categories
        pipline = [
            {
                '$match': {
                    "risk_scope_name": {"$in": objectsKind},
                    "$or": [
                        {"risk_category_name": {"$in": objectsRisk}},
                        {"actual_risk_category_activities_name": {"$in": objectsRisk}},
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$control_org_name",
                    "count": {"$sum": 1}
                }
            }
        ]
        return self.collection.aggregate(pipline)

    def getRhsObjectsTuRiskKind(self, kinds):
        """
        только если collection_name задан rhs!!!!!!!
        Возвращает аггрегацию по ТУ и категориям риска в разрезе видов деятельности
        Используется для построения сводной таблицы и выяснения сколько объектов указанной категории риска имеется в ТУ
        @return:
        """
        pipline = [
            {
                "$match": {"risk_scope_name": {"$in": kinds}}
            },

            {
                "$group": {
                    "_id": {"tu": "$control_org_name", "risk": "$actual_risk_category_activities_name"},
                    'count': {"$sum": 1}
                }
            }
        ]

        return self.collection.aggregate(pipline)

    def findChildCampings(self):
        return self.collection.find(
            {'status': {'$in': ['Завершено', 'Ожидает проведения', 'Ожидает завершения', 'Есть замечания']},
             'objectsKind': {
                 '$in': ['организации отдыха детей и их оздоровления, в том числе лагеря с дневным пребыванием',
                         'Деятельность по организации отдыха детей и их оздоровления, в том числе лагеря с дневным пребыванием',
                         'Деятельность детских лагерей на время каникул']}},
            {'_id': 0, 'id': 1, 'controllingOrganization': 1, 'organizationName': 1})

    def countKnmWhereisObjectsKind(self, *objectsKinds):
        return self.collection.count_documents({'objectsKind': {'$in': [*objectsKinds]}})

    def reportByAggreedProcessKNM(self):
        return self.collection.aggregate([{'$match': {'planId': {'$ne': None}}}, {
            '$group': {'_id': {'tu': "$controllingOrganization", 'status': "$status"}, 'totalCount': {'$sum': 1}}}])

    def reportByRiskIndicatorKNM(self):
        return self.collection.find({'reasons': {'$in': [315, 341, 3]}, 'status': {'$in': ['Завершено']}},
                                    {'_id': 0, 'controllingOrganization': 1, 'supervisionType': 1, 'erpId': 1,
                                     'reasonList': 1})

    def reportByAggreedProcessObjects(self):
        return self.collection.aggregate([{'$match': {'planId': {'$ne': None}}}, {"$unwind": "$objectsKind"}, {
            '$group': {'_id': {'tu': "$controllingOrganization", 'status': "$status"}, 'totalCount': {'$sum': 1}}}])

    def reportFromDeniedKNMComment(self):
        return self.collection.find({'status': 'Исключена', 'planId': {"$ne": None}},
                                    {'_id': 0, 'controllingOrganization': 1, 'comment': 1, 'erpId': 1, 'id': 1,
                                     'organizationsInn': {'$slice': 1}})

    def reportFromDeniedKNMObjectCategory(self):
        return self.collection.aggregate(
            [{'$unwind': "$objectsKind"}, {'$match': {'status': "Исключена", 'planId': {"$ne": None}}}, {
                '$group': {'_id': {'tu': "$controllingOrganization", 'kind': "$objectsKind"},
                           'totalCount': {'$sum': 1}}}])

    def reportFromAcceptKNMObjectCategory(self):
        return self.collection.aggregate([
            {'$unwind': "$objectsKind"},
            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},
            {'$match': {'planId': {"$ne": None}, 'status': {
                '$in': ['Ожидает проведения', 'Есть замечания', 'Ожидает завершения', 'Завершено']}}}, {'$group': {
                '_id': {'tu': "$controllingOrganization", 'kind': "$objectsKind"}, 'totalCount': {'$sum': 1}}}])

    def reportFromAcceptKNMObjectCategoryByDate(self):
        return self.collection.aggregate([
            {'$unwind': "$objectsKind"},
            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},

            {'$match': {'status': {
                '$in': ['Ожидает проведения', 'Есть замечания', 'Ожидает завершения', 'Завершено']}}}, {'$group': {
                '_id': {'controllingOrganization': "$controllingOrganization", 'knmtype': "$knmType", 'kind': "$kind", 'startDateEn': '$startDateEn', 'objectsKind': "$objectsKind",
                        "status": "$status"}, 'objectsCount': {"$sum": 1}}}])

    def reportFromDeniedKNMObjectCategoryByDate(self):
        return self.collection.aggregate([
            {'$unwind': "$objectsKind"},
            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},

            {'$match': {'status': {
                '$in': ['Исключена']}}}, {'$group': {
                '_id': {'controllingOrganization': "$controllingOrganization", 'knmtype': "$knmType", 'kind': "$kind", 'startDateEn': '$startDateEn', 'objectsKind': "$objectsKind",
                        "status": "$status"}, 'objectsCount': {"$sum": 1}}}])



    def reportFromAcceptKNMTypeKindReasonByDate(self):
        return self.collection.aggregate([

            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},

            {'$match': {'status': {
                '$in': ['Ожидает проведения', 'Есть замечания', 'Ожидает завершения', 'Завершено']}}},
            {'$unwind': '$reasonsList'},
            {'$group': {
                '_id': {'controllingOrganization': "$controllingOrganization", 'knmtype': "$knmType",
                        "status": "$status", 'startDateEn': '$startDateEn',
                        'kind': "$kind", 'reason': "$reasonsList.text"}, 'objectsCount': {"$sum": 1}}}])

    def reportFromDeniedKNMTypeKindReasonByDate(self):
        return self.collection.aggregate([

            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},

            {'$match': {'status': {
                '$in': ['Исключена']}}},
            # {'$unwind': '$reasonsList'},
            {'$group': {
                '_id': {'controllingOrganization': "$controllingOrganization",
                        # 'knmtype': "$knmType",
                        # "status": "$status",
                        # 'startDateEn': '$startDateEn',
                        # 'kind': "$kind",
                        # 'reason': "$reasonsList.text"
                        }, 'objectsCount': {"$sum": 1}}}])

    def reportFromDeniedKNMObjectCategoryKNM(self):
        return self.collection.aggregate(
            [{'$project': {'objectsKind': 1, 'status': 1, 'controllingOrganization': 1, 'countknm': {'$add': [1]}}},
             {'$unwind': "$objectsKind"}, {'$match': {'planId': {"$ne": None}, 'status': "Исключена"}}, {
                 '$group': {'_id': {'tu': "$controllingOrganization", 'kind': "$objectsKind"},
                            'totalCount': {'$sum': '$countknm'}}}])

    def reportByProductionConsist(self):
        return self.collection.aggregate(
            [{'$match': {'kind': 'Выборочный контроль', 'status': 'Ожидает проведения'}}, {'$unwind': '$objectsKind'}, {
                '$group': {'_id': {'tu': "$controllingOrganization", 'production': '$objectsKind'},
                           'totalCount': {'$sum': 1}}}])

    def reportForInspectSite(self):
        return self.collection.find({
            '$or': [
                {'status': {'$in': ['Ожидает проведения', 'Ожидает завершения', "Завершено", "Есть замечания"]}},
                {'$and': [{'status': 'Исключена'}, {'approved': True}]}
            ],
            'planId': {'$ne': None}
        },
            {
                '_id': 0,
                'controllingOrganization': 1,
                'organizationName': 1,
                'ogrn': 1,
                'inn': 1,
                'addresses': 1,
                'startDate': 1,
                'directDurationDays': 1,
                'durationDays': 1,
                'durationHours': 1,
                'kind': 1,
                'collaboratingOrganizations': 1,
                'id': 1,
                'erpId': 1,
                'mspCategory': 1,
                'status': 1
            }
        )

    def getObjectsFromPlan(self):
        return self.collection.find({'status': "На согласовании", 'kind': {'$ne': 'Выборочный контроль'}},
                                    {'_id': 0, 'inn': 1, 'addresses': 1, 'riskCategory': 1, 'objectsKind': 1}).limit(1)

    def predosterezhenia(self):
        # xl_path = 'inns_predostereg.xlsx'
        # wb = openpyxl.Workbook()
        # sh = wb.worksheets[0]
        date_start = '01.01.2023'
        date_end = '31.03.2023'
        start_limit = datetime.strptime(date_start, '%d.%m.%Y')
        stop_limit = datetime.strptime(date_end, '%d.%m.%Y')

        dict_of_inns = []
        for res in tqdm(self.collection.find({'isPm': True, 'kind': 'Объявление предостережения'},
                                             {'_id': 0, 'inn': 1, 'startDate': 1})):
            doc_date = datetime.strptime(res['startDate'], '%d.%m.%Y')
            if start_limit <= doc_date <= stop_limit:
                dict_of_inns.append(res['inn'])

        set_of_inns = set(dict_of_inns)
        more_than_2 = 0
        for inn in tqdm(set_of_inns):
            if dict_of_inns.count(inn) > 1:
                more_than_2 += 1

        print(more_than_2)

    def getKNMWithoutBudjets(self):
        """

        @return: КНМ без объектов, подлежащих исключению по 336 ПП
        """
        municipal = [
            re.compile('муницип', re.IGNORECASE),
            re.compile('государ', re.IGNORECASE),
            re.compile('областн', re.IGNORECASE),
            re.compile('казенн', re.IGNORECASE),
            re.compile('бюджетн', re.IGNORECASE),
            # re.compile('', re.IGNORECASE),
            # re.compile('', re.IGNORECASE),

        ]
        return self.collection.aggregate(
            [
                {'$unwind': '$objectsKind'},
                {'$match':
                    {
                        'status': {'$in': ['Ожидает проведения', 'Есть замечания']},
                        'organizationName': {'$in': [*municipal]},
                        'objectsKind': {'$in': [
                            *d.children_meal_kinds,
                            *d.child_camps_kinds,
                            *d.health_care_kinds,
                            *d.professional_education,
                            # *d.education,
                            *d.children_social_services,
                            *d.school_kinds,
                            *d.preschool_kinds,
                        ]},
                        'objectsKind': {'$in': [
                            *d.public_catering_kind
                        ]},

                    }
                },
                {'$group': {'_id': "$controllingOrganization", 'totalCount': {'$sum': 1}}}
            ]
        )

    def getKnmFromDate(self, date: str):  # дата формата YYYY-MM-DD

        return self.collection.aggregate([
            {"$match": {
                "startDateEn": date,
                "status": {
                    "$in": [
                        "Ожидает проведения",
                        "Ожидает завершения",
                        "Завершено",
                        "Есть замечания"
                    ]
                }
            }
            },
            {
                "$group": {
                    "_id": "$controllingOrganization",
                    'count': {'$sum': 1}
                }
            }
        ])


    def reportPeriodApplyingProsecutors(self):
        """
        Агрегация для вычисления по годам срока согласования внеплановых проверок прокуратурой
        @return:
        агрегация с уникальными ТУ, дата направления, дата ответа, год
        """
        pipline = [
            {'$match': {
                'planId': None,
                'approveDocOrderDate': {'$ne': None},
                'approveDocRequestDate': {'$ne': None},
                # 'objectsKind': {'$in': [*d.public_catering_kind, *d.children_meal_kinds]}
            }
             },

            {
                "$group": {
                    '_id': {
                        'controllingOrganization': "$controllingOrganization",
                        'orderDate': "$startDate",
                        'responceDate': "$approveDocRequestDate",
                        'year': "$year"
                    },
                    'objectsCount': {"$sum": 1}

                }
            }
        ]

        return self.collection.aggregate(pipline)

    def reportFromDeniedKNMTypeKindReasonByDate(self):
        return self.collection.aggregate([
            {'$unwind': "$objectsKind"},
            # {"$project": {"planId": 1, "status": 1, "controllingOrganization": 1, "objectsKind": 1, "erpId": 1}},

            {'$match': {'planId': {"$ne": None}, 'status': {
                '$in': ['Исключена']}}},
            {'$unwind': '$reasonsList'},
            {'$group': {
                '_id': {'controllingOrganization': "$controllingOrganization", 'knmtype': "$knmType",
                        "status": "$status",  "startDateEn": "$startDateEn",
                        'kind': "$kind", 'reason': "$reasonsList.text"}, 'objectsCount': {"$sum": 1}}}])

    # def getKNMByRiskIndicators
    def reportKNM_by_kind_objects(self, kinds, risks, notIn: bool = False):
        if not isinstance(risks, list):
            risks = [risks]
        if not isinstance(kinds, list):
            kinds = [kinds]
        pipline = [
            {"$match": {
                "objectsKind": {"$nin": kinds} if notIn else {"$in": kinds},
                # "supervisionTypeId": "004",
                "riskCategory": {"$in": risks}
            }
             },
            {"$group": {
                "_id": {"controllingOrganization": "$controllingOrganization",
                        "supervisionType": "$supervisionType",
                        "kind": "$kind",
                        "knmType": "$knmType",
                        "startDateEn": "$startDateEn",
                        "status": "$status"
                        },
                "objectsCount": {"$sum": 1}
            }
             }
        ]
        return self.collection.aggregate(pipline)


def objects_kind_tu_count_by_dates(dates: list):  # date format yyyy-mm-dd
    wm = WorkMongo()
    # objects_kind_tu_count = wm.getKnmFromDate("2024-07-12")
    # pprint(list(objects_kind_tu_count))


if __name__ == '__main__':
    wm = WorkMongo()
    # date = '2024-05-01'
    unpacked = unpac_idAggregation(list(wm.reportFromDeniedKNMTypeKindReasonByDate()))
    summ = 0
    for u in unpacked:
        if u['controllingOrganization'] == 'Управление Роспотребнадзора по Московской области':
            summ += u['objectsCount']
            print(u)

    print(summ)

    # objects_kind_tu_count = wm.getKnmFromDate("2024-07-12")
    # pprint(list(objects_kind_tu_count))

    # results = [r for r in wm.getKNMWithoutBudjets()]
    # for r in results:
    #     pprint(r)
    # print(len(results))
    # result = wm.getObjectsFromPlan()[0]
    # inn = result['inn']
    # for address, kind, risk in zip(result['addresses'], result['objectsKind'], result['riskCategory']):
    #     print(address, kind, risk)
