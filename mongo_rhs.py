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
from private_config import net_address


class WorkMongo:
    def __init__(self, collection_name: str = 'rhs'):
        client = MongoClient(net_address, 27018)

        db = client['knm']
        self.collection = db[collection_name]

    def insert_many(self, knm_list):
        self.collection.insert_many(knm_list)

    def insertManyInspectInfo(self, inns, inspectionInfo):
        return self.collection.update_many({'inn': {"$in": inns}}, {"$set": {"lastInspected": inspectionInfo}})

    def getUninspectedObjects(self, objectsKind: list):

        return self.collection.aggregate([
            {
                '$match': {
                    "risk_scope_name": {
                        '$in': objectsKind
                    },
                    # "lastInspected": {'$ne': None}
                    "lastInspected": None

                }
            },
            {
                "$group": {
                    "_id": {
                        'risk': "$actual_risk_category_activities_name"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    'risk': "$_id.risk",
                    "count": "$count",
                }
            }
        ])

    def getSubjectsByObjectsKinds(self, objectsKinds: list, risks: list):
        return self.collection.find(
            {
                "risk_scope_name": {
                    "$in": objectsKinds
                },
                "actual_risk_category_activities_name": {
                    "$in": risks
                }
            },
            {'_id': 0, "inn": 1}
        )

        return self.collection.aggregate(pipline)

    def reportTuObjectsKindRisk(self):
        pipeline = [
            {
                "$match": {
                    "control_org_name": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": {'controllingOrganization': "$control_org_name", "lastInspected": "$lastInspected", 'objectsKind': "$risk_scope_name", "actualRisk": "$actual_risk_category_activities_name"},
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

    def getExponedPeople(self):
        """выборка объектов по числу экспонируемого населения в пределах одного ИНН с группировкой по муниципальным образованиям"""

        pipeline = [
            {
                "$match": {
                    "risk_scope_name": 'Деятельность по торговле пищевыми продуктами, включая напитки, и табачными изделиями'
                }
            },
            {
                "$project": {
                    "control_org_name": 1,
                    "affected_total": 1,
                    "inn": 1,
                    "address": "$address.full_address"
                }
            },
            {
                "$group": {
                    "_id": {
                        "control_org_name": "$control_org_name",
                        "affected_total": "$affected_total",
                        "inn": "$inn",
                        "address": "$address",
                        "guid": "$guid"
                    },
                      "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "control_org_name": "$_id.control_org_name",
                    "affected_total": "$_id.affected_total",
                    "inn": "$_id.inn",
                    "address": "$_id.address",
                    "guid": "$_id.guid"
                }
            }
        ]

        return self.collection.aggregate(pipeline)


if __name__ == '__main__':
    from Dictionary import group_kinds
    print(list(WorkMongo().getUninspectedObjects(group_kinds['Общественное питание населения'])))
