import schedule
import keypass
from main import load_knm
from main_cubes import loadCube
from sql_cubes import Database
from datetime import datetime
import time
from Bot_telegram import send_message_to_terr_upr


def reload():
    keypass.stopConteiners(
        'mongo'
    )
    keypass.renameDir()
    keypass.startConteiners(
        'mongo'
    )
    popit = 40
    while True:
        try:
            load_knm(2024)
            break
        except Exception as ex:
            popit -= 1
            if popit == 0:
                error = f'ОШИБКА! {datetime.now()} - предприняты все возможные попытки обновить сведения, необходим дебаг autoloader.py (22)!'
                send_message_to_terr_upr(f'{error=},\n {ex=}')
                # raise Exception(f'{error} {ex}')
            continue
    Database().deleteCurrentYearValues()
    loadCube()
    frase = f'{datetime.now()} - произошло запланированное обновление данных'
    print(frase)
    send_message_to_terr_upr(frase)


if __name__ == '__main__':
    timeX = "11:14"
    print(f'{datetime.now()} - запушено. следующее обновление в {timeX}')
    schedule.every().day.at(timeX).do(reload)
    while True:
        schedule.run_pending()
        time.sleep(1)
