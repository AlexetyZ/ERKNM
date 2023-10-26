from pymongo import MongoClient
from multiprocessing import Pool
import pprint
import openpyxl
from tqdm import tqdm
from datetime import datetime
from pprint import pprint


class WorkMongo:
    def __init__(self):
        client = MongoClient('localhost', 27017)

        db = client['knm']
        self.collection = db['knm']

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
        return self.collection.aggregate([{"$match": filters}, {"$unwind": "$objectsKind"}, {"$group": {"_id": "$objectsKind", "count": {"$sum": 1}}}])

    def reportByRisk(self, **filters):
        return self.collection.aggregate(
            [{"$match": filters}, {"$unwind": "$riskCategory"}, {"$group": {"_id": "$riskCategory", "count": {"$sum": 1}}}])

    def free_command(self, request):
        return self.collection.find(request)

    def countKnmWhereisObjectsKind(self, *objectsKinds):
        return self.collection.count_documents({'objectsKind': {'$in': [*objectsKinds]}})

    def reportByAggreedProcessKNM(self):
        return self.collection.aggregate([{'$group': {'_id': {'tu': "$controllingOrganization", 'status': "$status"}, 'totalCount': {'$sum': 1}}}])

    def reportByRiskIndicatorKNM(self):
        return self.collection.find({'reasons': {'$in': [315, 341, 3]}, 'status': {'$in': ['Завершено']}}, {'_id': 0, 'controllingOrganization': 1, 'supervisionType': 1, 'erpId': 1, 'reasonList': 1})

    def reportByAggreedProcessObjects(self):
        return self.collection.aggregate([{"$unwind": "$objectsKind"}, {'$group': {'_id': {'tu': "$controllingOrganization", 'status': "$status"}, 'totalCount': {'$sum': 1}}}])

    def reportFromDeniedKNMComment(self):
        return self.collection.find({'status': 'Исключена'}, {'_id': 0, 'controllingOrganization': 1, 'comment': 1, 'erpId': 1, 'id': 1, 'organizationsInn': {'$slice': 1}})

    def reportFromDeniedKNMObjectCategory(self):
        return self.collection.aggregate([{'$unwind': "$objectsKind"}, {'$match': {'status': "Исключена"}}, {'$group': {'_id': {'tu': "$controllingOrganization", 'kind': "$objectsKind"}, 'totalCount': {'$sum': 1}}}])

    def reportFromDeniedKNMObjectCategoryKNM(self):
        return self.collection.aggregate([{'$project': {'objectsKind': 1, 'status': 1, 'controllingOrganization': 1, 'countknm': {'$add': [1]}}}, {'$unwind': "$objectsKind"}, {'$match': {'status': "Исключена"}}, {'$group': {'_id': {'tu': "$controllingOrganization", 'kind': "$objectsKind"}, 'totalCount': {'$sum': '$countknm'}}}])

    def reportByProductionConsist(self):
        return self.collection.aggregate([{'$match': {'kind': 'Выборочный контроль', 'status': 'Ожидает проведения'}}, {'$unwind': '$objectsKind'}, {'$group': {'_id': {'production': '$objectsKind'}, 'totalCount': {'$sum': 1}}}])

    def getObjectsFromPlan(self):
        return self.collection.find({'status': "На согласовании", 'kind': {'$ne': 'Выборочный контроль'}}, {'_id': 0, 'inn': 1, 'addresses': 1, 'riskCategory': 1, 'objectsKind': 1}).limit(1)

    def convertForsaving(self, results: list[dict]) -> list:

        title = list(results[0].keys())
        values = [list(result.values()) for result in list(results)]
        return title, values


    def predosterezhenia(self):
        # xl_path = 'inns_predostereg.xlsx'
        # wb = openpyxl.Workbook()
        # sh = wb.worksheets[0]
        date_start = '01.01.2023'
        date_end = '31.03.2023'
        start_limit = datetime.strptime(date_start, '%d.%m.%Y')
        stop_limit = datetime.strptime(date_end, '%d.%m.%Y')

        dict_of_inns = []
        for res in tqdm(self.collection.find({'isPm': True, 'kind': 'Объявление предостережения'}, {'_id': 0, 'inn': 1, 'startDate': 1})):
            doc_date = datetime.strptime(res['startDate'], '%d.%m.%Y')
            if start_limit <= doc_date <= stop_limit:
                dict_of_inns.append(res['inn'])

        set_of_inns = set(dict_of_inns)
        more_than_2 = 0
        for inn in tqdm(set_of_inns):
            if dict_of_inns.count(inn) > 1:
                more_than_2 += 1

        print(more_than_2)


        # wb.save(xl_path)


if __name__ == '__main__':
    wm = WorkMongo()
    result = wm.getObjectsFromPlan()[0]
    inn = result['inn']
    for address, kind, risk in zip(result['addresses'], result['objectsKind'], result['riskCategory']):
        print(address, kind, risk)



