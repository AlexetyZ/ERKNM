import re
import json
import ast
from sql import Database

exceptions = []
with open('C:\\Users\zaitsev_ad\PycharmProjects\ERKNM\logging\\18.01.2023.log', 'rb') as file:

    for line in file:
        find = re.findall(r'new_insert_in_database.268.*- ({.*})', line.decode("utf-8", "ignore"))
        # print(find)
        if find:
            exceptions.append(eval(find[0]))

# print(exceptions)
for result in exceptions:
    print(result)
    Database().ultra_create_handler(result)

# with open("Exception_knm.json", 'w') as f:
#     json.dump(exceptions, f)



