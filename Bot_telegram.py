import datetime
import time

import config
import telebot
from pprint import pprint
from keypass import getTheFuckUpAndBadBitchGO
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['add'])
def start_message(message):
    your_variable = message
    print(your_variable)

@bot.message_handler(commands=['getotp'])
def getotp(message):
    if message.from_user.id == config.chat_id_knm:
        bm = send_message_to_terr_upr(getTheFuckUpAndBadBitchGO())
        time.sleep(10)
        bot.delete_messages(chat_id=message.chat.id, message_ids=[message.id, bm.id])




def send_message_to_terr_upr(text):
    return bot.send_message(chat_id=config.chat_id_knm, text=text)


if __name__ == '__main__':
    bot.polling()
    send_message_to_terr_upr(f'Бот завершил работу {datetime.datetime.now()}')


