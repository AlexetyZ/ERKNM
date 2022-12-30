
list_1 = [{'key_1': "value_1"}, {'key_2': "value_2"}, {'key_3': "value_3"}, {'key_4': "value_4"}]

object_1 = {'key_1': "value_1"}
inn = 'key_1'

list_1.remove([obj for obj in list_1 if inn == list(obj.keys())[0]][0])

print(list_1)