from pyotp import TOTP
import time
from crypto import Crypto
from config import s_key
import os
from datetime import datetime


def getTheFuckUpAndBadBitchGO():
    secret = Crypto().unpack_password(s_key)
    interval = 30
    totp = TOTP(secret)
    current_timestamp = int(round(time.time()))
    otp = totp.now()
    return otp


def stopConteiners(*containers):
    for conteiner in containers:
        os.system(f'docker stop {conteiner}')


def startConteiners(*containers):
    for conteiner in containers:
        os.system(f'docker start {conteiner}')


def renameDir():
    now = datetime.now().strftime('%d.%m.%Y')
    path = "C:\\Users\zaitsev_ad\Documents\Базы данных"
    name = 'mongo'
    new_name = os.path.join(path, f'{name} 2024 от {now}')
    os.rename(os.path.join(path, name), new_name)


if __name__ == '__main__':
    print(getTheFuckUpAndBadBitchGO())
