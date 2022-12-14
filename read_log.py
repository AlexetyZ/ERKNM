import re
import json
import ast

exceptions = []
with open('C:\\Users\zaitsev_ad\PycharmProjects\ERKNM\logging\\14.12.2022.log', 'rb') as file:

    for line in file:
        find = re.findall(r'new_insert_in_database.296.*- ({.*})', line.decode("utf-8", "ignore"))
        if find:
            exceptions.append(eval(find[0]))

print(exceptions)

with open("Exception_knm.json", 'w') as f:
    json.dump(exceptions, f)



