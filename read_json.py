import json

path = "C:\\Users\zaitsev_ad\Desktop\мелкие записи и напоминалки\ERKNM regions domains.json"

with open(path, encoding="utf8") as file:
    # print(file)
    list_domains = json.load(file)

    for domain in list_domains:
        print(domain)
