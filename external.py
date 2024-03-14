from mongo_database import WorkMongo
from main_ERKNM import erknm
from pprint import pprint
from tqdm import tqdm



def main():
    wm = WorkMongo()
    list_id = wm.indic()
    listId = [i['id'] for i in list_id]
    knms = getKnm(listId)
    wmi = WorkMongo('wmiall')
    wmi.insert_many(knms)
    print('завершено')


def getKnm(listId):
    e = erknm()
    e.autorize()
    for i in tqdm(listId):
        yield e.get_knm_by_true_id(i)


def getDicts(dicts):
    e = erknm()
    e.autorize()
    for d in tqdm(dicts):
        yield e.getDictionnary(
            '1afc36ea-ba6b-11eb-8529-0242ac130003', d
        )


def main2():
    from Dictionary import indicatorList
    from xl import writeResultsInXL

    wm = WorkMongo('wmiall')
    _list = wm.dewIndic()
    list1 = [i['knmErknm']['reasons'][0]['riskIndikators']['dictVersionId'] for i in _list]

    list2 = getDicts(list1)
    writeResultsInXL(list2)


if __name__ == '__main__':
    main2()
    