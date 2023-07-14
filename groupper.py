from itertools import groupby
set_1 = (('value_1', 'key_1'), ('value_1', 'key_2'), ('value_2', 'key_3'), ('value_2', 'key_4'))



def group(set_1):
    set_2 = {}
    for v in groupby(set_1, key=lambda x: x[0]):
        set_2[v[0]] = [i[1] for i in v[1]]
    return set_2


print(group(set_1))

