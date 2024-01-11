import re

import xl
from Dates_manager import *
from pymongo import MongoClient
import openpyxl
from tqdm import tqdm
from datetime import datetime
from pprint import pprint
import Dictionary as d
from mongo_database import unpac_idAggregation, convertForsaving


class WorkMongo:
    def __init__(self, collection_name: str = 'rhs'):
        client = MongoClient('localhost', 27018)

        db = client['knm']
        self.collection = db[collection_name]

    def insert_many(self, knm_list):
        self.collection.insert_many(knm_list)

    def reportTuObjectsKindRisk(self):
        pipeline = [
            {
                "$match": {
                    "control_org_name": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {'controllingOrganization': "$control_org_name", 'objectsKind': "$risk_scope_name", "actualRisk": "$actual_risk_category_activities_name"},
                    'objectsCount': {"$sum": 1}
                }
            }
        ]
        return self.collection.aggregate(pipeline)

    def reportTuOkvedRisk(self):
        pipeline = [
            {
                "$match": {
                    "control_org_name": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {'controllingOrganization': "$control_org_name", 'okvedName': "$okved_name",
                            "actualRisk": "$actual_risk_category_activities_name"},
                    'objectsCount': {"$sum": 1}
                }
            }
        ]
        return self.collection.aggregate(pipeline)


if __name__ == '__main__':
    print(WorkMongo().reportTuObjectsKindRisk())
