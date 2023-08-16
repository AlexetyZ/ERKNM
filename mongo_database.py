from pymongo import MongoClient
from multiprocessing import Pool
import pprint
import openpyxl
from tqdm import tqdm
from datetime import datetime


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
    wm.predosterezhenia()



