import datetime

start = '08.06.2023'
stop = '15.06.2023'

start_limit = datetime.datetime.strptime(start, '%d.%m.%Y')
stop_limit = datetime.datetime.strptime(stop, '%d.%m.%Y')
if start_limit < datetime.datetime.now() < stop_limit:
    print('в диапозоне')
else:
    print('не в диапозоне')
