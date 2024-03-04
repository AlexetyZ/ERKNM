from pyotp import TOTP
import time
from crypto import Crypto
from config import s_key


def getTheFuckUpAndBadBitchGO():
    secret = Crypto().unpack_password(s_key)
    interval = 30
    totp = TOTP(secret)
    current_timestamp = int(round(time.time()))
    otp = totp.now()
    return otp


if __name__ == '__main__':
    from main_ERKNM import erknm
    e = erknm()
    e.autorize()
