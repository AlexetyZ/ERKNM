from pymongo import MongoClient


class WorkMongo:
    def __init__(self):
        client = MongoClient('localhost', 27017)

        db = client['knm']
        self.collection = db['knm']

    def insert(self, knm):
        self.collection.insert_one(knm)


if __name__ == '__main__':
    wm = WorkMongo()
    wm.insert({'wtf': 'tfw'})

