import config
import telebot
from keypass import getTheFuckUpAndBadBitchGO
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['add'])
def start_message(message):
    your_variable = message.from_user
    print(your_variable)

@bot.message_handler(commands=['getotp'])
def getotp(message):
    if message.from_user.id == config.chat_id_knm:
        send_message_to_terr_upr(getTheFuckUpAndBadBitchGO())


def send_message_to_terr_upr(text):

    bot.send_message(chat_id=config.chat_id_knm, text=text)


if __name__ == '__main__':
    bot.polling()

